#!/usr/bin/env python3
"""
Pilot: security-bearing filter over the Zenodo corpus
"A Dataset of Agentic AI Coding Tool Configurations" (DOI 10.5281/zenodo.19375881).

Usage:
    python3 scripts/01_filter_security_bearing.py data/raw/   [--out results/pilot]

Expects the unpacked Zenodo files in data/raw/: context_files.csv, skills.csv,
subagents.csv, rules.csv, commands.csv (any subset is fine). The script finds the
column holding file content automatically (first column named like content/text/body,
else the longest string column) and the repository column (repo/repository/full_name).

Outputs (to --out):
    summary.json         headline numbers for the RR, Sec. V-C
    per_term.csv         hits per keyword term and per artefact type
    flagged_files.csv    one row per flagged file: repo, artefact type, path, hit terms, #units
    sample_for_precision.csv   100 random flagged files to annotate for filter precision
    sample_for_recall.csv      200 random NON-flagged files to annotate for filter recall

Keyword set = Table II of the registered report (standards-derived, case-insensitive).
"""
import argparse, csv, json, os, random, re, sys
from collections import Counter, defaultdict

csv.field_size_limit(sys.maxsize)
random.seed(20261130)

# Table II of the RR. (regex, source, fp_risk)
TERMS = [
    # ASVS V2/V6 + agent-conduct seed  -- secrets
    (r"\bsecrets?\b", "secret", "ASVS V2/V6", "low"),
    (r"\bcredentials?\b", "credential", "ASVS V2/V6", "low"),
    (r"\bapi[ _-]?keys?\b", "api key", "ASVS V2/V6", "low"),
    (r"\btokens?\b", "token", "ASVS V2/V6", "med"),
    (r"\bpasswords?\b", "password", "ASVS V2/V6", "low"),
    (r"\.env\b", ".env", "agent-conduct seed", "low"),
    # ASVS V5 / CWE  -- injection & validation
    (r"\binjection\b|\binject\b", "injection", "ASVS V5; CWE-79/89", "low"),
    (r"\bsaniti[sz](e|ing|ation)\b", "sanitise", "ASVS V5", "low"),
    (r"\bescap(e|ing)\b.*\b(html|sql|input|output|user)\b", "escape", "ASVS V5", "med"),
    (r"\bparameteri[sz]ed\b", "parameterised", "ASVS V5; CWE-89", "low"),
    (r"\bxss\b|\bcross[- ]site scripting\b", "xss", "CWE-79", "low"),
    (r"\bcsrf\b", "csrf", "CWE-352", "low"),
    (r"\bssrf\b", "ssrf", "CWE-918", "low"),
    # ASVS V3/V4 -- authn/authz
    (r"\bauthenticat(e|ion|ed)\b", "authentication", "ASVS V3", "med"),
    (r"\bauthori[sz](e|ation|ed)\b", "authorization", "ASVS V4", "med"),
    (r"\bsessions?\b.*\b(secure|expire|token|cookie)\b", "session", "ASVS V3", "med"),
    (r"\brbac\b", "rbac", "ASVS V4", "low"),
    (r"\bpermissions?\b", "permission", "ASVS V4", "med"),
    # ASVS V6/V9 -- crypto/transport
    (r"\bencrypt(ion|ed)?\b", "encrypt", "ASVS V6", "med"),
    (r"\btls\b|\bssl\b", "tls", "ASVS V9", "med"),
    (r"\bhttps\b", "https", "ASVS V9", "med"),
    (r"\bhash(ing|ed)?\b.*\b(password|secret|bcrypt|argon|sha)\b", "hash", "ASVS V6", "med"),
    (r"\bcrypto(graph(y|ic))?\b", "crypto", "ASVS V6", "med"),
    # SSDF PW.4 / RV -- dependencies & vulns
    (r"\bcve-\d{4}-\d+\b|\bcves?\b", "cve", "SSDF RV", "low"),
    (r"\bvulnerab(le|ility|ilities)\b", "vulnerability", "SSDF RV", "low"),
    (r"\badvisor(y|ies)\b", "advisory", "SSDF RV", "low"),
    (r"\bdependabot\b|\brenovate\b", "dependabot", "SSDF PW.4", "low"),
    (r"\b(npm|pip|cargo|security) audit\b", "audit", "SSDF PW.4", "low"),
    (r"\bsbom\b", "sbom", "SSDF PS", "low"),
    # standards named explicitly
    (r"\bowasp\b", "owasp", "standard", "low"),
    (r"\bcwe-?\d*\b", "cwe", "standard", "low"),
    (r"\basvs\b", "asvs", "standard", "low"),
    (r"\bnist\b", "nist", "standard", "low"),
    (r"\bgdpr\b", "gdpr", "standard", "low"),
    (r"\bpii\b|\bpersonal(ly identifiable)? (data|information)\b", "pii", "standard", "low"),
    # OWASP LLM Top-10 (excessive agency) + agent-conduct seed
    (r"\b(never|do not|don't|must not|avoid) (ever )?commit(ting)?\b", "never commit", "agent-conduct", "low"),
    (r"\b(never|do not|don't|must not) (ever )?(read|open|cat|print|log|expose|leak)\b", "never read/expose", "agent-conduct", "med"),
    (r"\b(never|do not|don't|must not) (ever )?(run|execute)\b", "never run", "agent-conduct", "med"),
    (r"\bdestructive\b", "destructive", "agent-conduct", "low"),
    (r"\brm -rf\b", "rm -rf", "agent-conduct", "low"),
    (r"\bforce[- ]push\b|\bpush --force\b|\b--force\b", "force push", "agent-conduct", "low"),
    (r"--no-verify\b", "--no-verify", "agent-conduct", "low"),
    (r"\bprompt injection\b", "prompt injection", "OWASP LLM01", "low"),
    (r"\buntrusted\b", "untrusted", "OWASP LLM", "low"),
    (r"\bsandbox(ed|ing)?\b", "sandbox", "OWASP LLM", "med"),
    (r"\bsecurity\b", "security (generic)", "generic", "med"),
]
COMPILED = [(re.compile(rx, re.I | re.S), name, src, fp) for rx, name, src, fp in TERMS]

ARTEFACT_FILES = ["context_files.csv", "skills.csv", "subagents.csv", "rules.csv", "commands.csv"]

UNIT_SPLIT = re.compile(r"(?:\n\s*[-*+]\s+|\n\s*\d+[.)]\s+|(?<=[.!?])\s+(?=[A-Z])|\n{2,})")


def pick_col(header, candidates, rows=None):
    low = {h.lower(): h for h in header}
    for c in candidates:
        for h in low:
            if c in h:
                return low[h]
    if rows:  # longest string column
        best, bestlen = None, -1
        for h in header:
            l = sum(len(r.get(h) or "") for r in rows[:200])
            if l > bestlen:
                best, bestlen = h, l
        return best
    return None


def split_units(text):
    return [u.strip() for u in UNIT_SPLIT.split(text) if u and len(u.strip()) > 15]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("raw_dir")
    ap.add_argument("--out", default="results/pilot")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    per_term = Counter()
    per_term_type = defaultdict(Counter)
    flagged, nonflagged = [], []
    repos_all, repos_flagged = set(), set()
    files_all = Counter()
    units_per_flagged_file = []
    sec_units_total = 0

    for fname in ARTEFACT_FILES:
        path = os.path.join(a.raw_dir, fname)
        if not os.path.exists(path):
            print(f"[skip] {fname} not found", file=sys.stderr)
            continue
        atype = fname.replace(".csv", "")
        with open(path, newline="", encoding="utf-8", errors="replace") as f:
            rd = csv.DictReader(f)
            rows = list(rd)
        if not rows:
            continue
        hdr = rd.fieldnames
        ccol = pick_col(hdr, ["content", "text", "body", "file_content"], rows)
        rcol = pick_col(hdr, ["full_name", "repo", "repository", "project"])
        pcol = pick_col(hdr, ["path", "file", "name"])
        print(f"[{atype}] rows={len(rows)} content_col={ccol} repo_col={rcol} path_col={pcol}", file=sys.stderr)
        for r in rows:
            txt = r.get(ccol) or ""
            repo = r.get(rcol) or "?"
            pth = r.get(pcol) or ""
            repos_all.add(repo)
            files_all[atype] += 1
            hits = []
            for cre, name, src, fp in COMPILED:
                if cre.search(txt):
                    hits.append(name)
            # generic 'security' alone does not flag a file (too noisy); needs a second term
            strong = [h for h in hits if h != "security (generic)"]
            if strong:
                repos_flagged.add(repo)
                for h in hits:
                    per_term[h] += 1
                    per_term_type[atype][h] += 1
                units = split_units(txt)
                sec_units = [u for u in units if any(c.search(u) for c, n, s, f in COMPILED if n != "security (generic)")]
                units_per_flagged_file.append(len(sec_units))
                sec_units_total += len(sec_units)
                flagged.append({"repo": repo, "artefact_type": atype, "path": pth,
                                "hit_terms": "|".join(sorted(set(hits))), "n_units_total": len(units),
                                "n_security_units": len(sec_units), "chars": len(txt)})
            else:
                nonflagged.append({"repo": repo, "artefact_type": atype, "path": pth, "chars": len(txt),
                                   "generic_security_only": int("security (generic)" in hits)})

    n_files = sum(files_all.values())
    summary = {
        "repositories_total": len(repos_all),
        "repositories_flagged": len(repos_flagged),
        "repositories_flagged_pct": round(100 * len(repos_flagged) / max(1, len(repos_all)), 1),
        "files_total": n_files,
        "files_by_type": dict(files_all),
        "files_flagged": len(flagged),
        "files_flagged_pct": round(100 * len(flagged) / max(1, n_files), 1),
        "files_flagged_by_type": dict(Counter(x["artefact_type"] for x in flagged)),
        "security_units_total": sec_units_total,
        "security_units_per_flagged_file_mean": round(sum(units_per_flagged_file) / max(1, len(units_per_flagged_file)), 2),
        "security_units_per_flagged_file_median": sorted(units_per_flagged_file)[len(units_per_flagged_file) // 2] if units_per_flagged_file else 0,
        "files_with_only_generic_security_word": sum(x["generic_security_only"] for x in nonflagged),
        "top_terms": per_term.most_common(25),
    }
    with open(os.path.join(a.out, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    with open(os.path.join(a.out, "per_term.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["term", "source", "fp_risk", "files_hit"] + ARTEFACT_FILES)
        meta = {n: (s, fp) for _, n, s, fp in COMPILED}
        for t, c in per_term.most_common():
            w.writerow([t, meta[t][0], meta[t][1], c] + [per_term_type[a_.replace('.csv', '')][t] for a_ in ARTEFACT_FILES])
    for name, rows in [("flagged_files.csv", flagged)]:
        with open(os.path.join(a.out, name), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["repo"]); w.writeheader(); w.writerows(rows)
    random.shuffle(flagged); random.shuffle(nonflagged)
    for name, rows, k in [("sample_for_precision.csv", flagged, 100), ("sample_for_recall.csv", nonflagged, 200)]:
        with open(os.path.join(a.out, name), "w", newline="") as f:
            if rows:
                w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) + ["annotator_security_bearing(0/1)", "notes"]); w.writeheader()
                for r in rows[:k]:
                    w.writerow({**r, "annotator_security_bearing(0/1)": "", "notes": ""})
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
