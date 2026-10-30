---
title: "MSR Registered Reports 2023–2025 compared with our Stage-1 draft v0.1"
author: "Prepared for Krzysztof Wnuk — 29 October 2026"
---

# 1. What was accepted (as far as the public programme pages show)

The track pages are long and the fetch was truncated, so this is the set I could confirm; the track typically accepts 2–5 reports per year.

| Year | Accepted report | Type | Data / design in one line |
|---|---|---|---|
| 2023 | Hennig, Schulte, Herbold, Kulyk, Mayer — *Understanding issues related to personal data and data protection in OSS projects on GitHub* (arXiv 2304.06367) | Exploratory | Keyword search (30 terms) over GitHub issues 2016–22 → 21,608 candidate issues; random sample of 650 (n = 100 + 50·k rule); two coders, κ ≥ 0.7 on 20%; χ², multinomial logit, CART, random forest |
| 2023 | Choetkiertikul et al. — *Mining the characteristics of Jupyter notebooks in data-science projects* | Exploratory | (programme listing only) |
| 2023 | Qasse, Hamdaqa, Jónsson — *Smart contract upgradeability on Ethereum: an exploratory study* | Exploratory | (programme listing only) |
| 2023 | Schröder, Cito — *An exploratory study of ad hoc parsers in Python* | Exploratory | (programme listing only) |
| 2023 | Schulte, Mojica-Hanke, Linares-Vásquez, Herbold — *An exploratory study of bug-introducing changes* | Exploratory | (programme listing only) |
| 2024 | Recupito, Giordano, Ferrucci, Di Nucci, Palomba — *When code smells meet ML: lifecycle of ML-specific smells* (arXiv 2403.08311) | **Mixed** (confirmatory + exploratory) | NICHE dataset (572 projects) → 337 sampled (95%/5%); build a detector (CodeSmile) validated by external engineers with κ; H0–H2 on prevalence by size/CI tested with Wilcoxon/Friedman + Cliff's δ; survival of smells |
| 2024 | Schneider, Scandariato, Bakhtin, Li, Soldani, Brogi, Cerny, Taibi — *Comparison of static-analysis architecture-recovery tools for microservices* | (tool comparison) | (programme listing only) |
| 2025 | Campos, Martins, Guglielmi, Tucci, Di Pompeo, Scalabrino, Cortellessa, Di Nucci, Oliveto — *Identifying and replicating code patterns driving performance regressions* | (not stated) | (programme listing only) |
| 2025 | Guglielmi, Arnaoudova, Bavota, Oliveto, Scalabrino — *How do Copilot suggestions impact developers' frustration and productivity?* (arXiv 2504.06808) | Confirmatory (crossover experiment) | 32–50 participants, 6 hypotheses, variables table, Wilcoxon + Bonferroni + Cliff's δ, HRV wristband |
| 2025 | Koohjani, Costa — *Lifecycle and maintenance practices of pre-trained models in OSS repositories* (arXiv 2504.06040) | Exploratory | PeaTMOSS subset (790/887 repos); 5 RQs; PageRank centrality, Kaplan–Meier survival of PTMs, Coverage.py, open coding with κ |

Also relevant: the EMSE paper that evaluated the track's first editions (Ernst & Baltes, *Registered reports in software engineering*, EMSE 2022) lists the recurring reasons for rejection or "continuity acceptance": too little detail for the page budget (especially with no pilot), ill-defined constructs, qualitative plans that do not address coding reliability, and **exploratory mining plans with no confirmatory hypotheses** — plus authors who did not change their approach after reviews.

# 2. Patterns across the accepted reports

1. **Almost all are MSR-native and reuse an existing curated dataset.** NICHE (2024), PeaTMOSS (2025), GitHub issues via keyword search (2023). A report that starts from someone else's dataset is the norm, not a weakness.
2. **Exploratory dominates, but the accepted exploratory reports are very concrete.** They specify the dataset size, sampling rule (95%/5% margin, or n = 100 + 50·k), the exact tools (PyDriller, Coverage.py, PageRank), the coders, the κ threshold, and the statistical test per RQ. The one mixed report (2024) states null hypotheses explicitly and names the test for each.
3. **Build-your-own-detector is accepted if validation is pre-specified.** Recupito et al. propose a new detector (CodeSmile) and pre-register how it will be validated (external annotators ≥3 years' experience, κ, majority vote, precision/recall). Our "security-bearing filter" and LLM judge sit in exactly this position.
4. **Keyword-based identification of a topic in text is accepted with an explicit false-positive handling plan.** Hennig et al. list their 30 keywords in a table, state which were excluded and why, and plan per-keyword false-positive rates. Reviewers accepted the construct "privacy issue" on that basis.
5. **Survival analysis is a recurring MSR-RR analysis.** Smell lifetime (2024), PTM longevity (2025) — Kaplan–Meier is familiar to this reviewer pool.
6. **Power analysis is present but light.** Hennig use a rule-of-thumb sample size; Guglielmi give a one-line power claim; Recupito use confidence/margin. Our MDE and Schoenfeld event counts are already more explicit than any of them.
7. **Related-work section is always present (2–3 columns).** Every accepted report has a Related Work or Background section; the 2027 CfP's required structure does not list one, but reviewers expect it.
8. **Threats sections are organised by validity type** (construct/internal/external/conclusion), and in 2024 each threat names a mitigation.
9. **Length.** 2023 reports were ~8 ACM pages; 2024–25 ~6 IEEE/ACM pages; Ernst & Baltes report 5–6 pages as typical. Ours is ~5 pages body — at the lower edge, which means room to add rather than cut.
10. **Pilot data is thin in all of them** — Hennig report only the keyword-search count (21,608 issues), Recupito only the number of projects and commits found. So a single prevalence number from running our filter would already put us above the median.
11. **Topic adjacency.** Hennig et al. 2023 (privacy/data-protection issues mined from GitHub with a keyword filter and manual coding) is the closest structural precedent to ours and was accepted; it had no outcome variable and no confirmatory part.

# 3. Draft v0.1 against those patterns

| Criterion | Accepted-report norm | Our draft | Verdict / action |
|---|---|---|---|
| Dataset reuse | Named public dataset | Galster et al. Zenodo corpus + refresh | ✔ matches |
| Sampling rule stated | Yes, always | 800 files at 95%/±3.5%; all if ≤1,000 | ✔ |
| Keyword list for topic filter | Full table, exclusions explained, per-keyword FP rate planned (Hennig) | Vocabulary described in prose; recall check on 200 non-flagged files | **Gap** — add a keyword table (with ASVS/CWE/LLM-Top-10 provenance of each term), state excluded terms, add per-keyword precision reporting |
| Coding reliability | Two coders, κ threshold, incremental re-coding until met | Pilot-then-split, κ ≥ 0.75 for taxonomy, κ ≥ 0.70 per rubric dimension, second LLM judge | ✔ stronger than norm; add the "continue coding in 5% increments until threshold" rule for the human part, as Hennig did |
| New detector/tool validated | External annotators, κ, P/R (Recupito) | LLM judge calibrated on 400 human-scored units; filter recall check | ✔ comparable; add precision/recall numbers to report for the filter, not just recall |
| Hypotheses for the mining part | Mixed reports state null hypotheses and tests (Recupito) | H1–H3 with model, direction, correction, support criterion | ✔ stronger than norm |
| Variables table | Confirmatory reports have one (Guglielmi) | Table I with scale and operationalisation | ✔ |
| Power | Light in all accepted reports | MDE and event counts computed | ✔ exceeds norm |
| Outcome-neutral / positive controls | Not seen in the accepted reports; required by 2027 CfP | Three controls specified | ✔ exceeds norm |
| Related Work section | Always present | Folded into Introduction | **Gap** — add a short "Background and Related Work" section (≈0.4 page) covering context-file studies, secure-code-generation evidence, RE quality/smells, and RR precedents |
| Pilot data | Thin but present (counts) | None (GitHub search unavailable from this environment) | **Gap** — run the filter on the 2,926 Galster repositories; report #security-bearing files, #units, top-10 categories from the 100-unit pilot, and filter precision on 100 flagged files |
| Threats by validity type with mitigations | Yes | Yes | ✔ |
| Survey component | Rare in MSR RRs (Hennig none; Koohjani none) | Survey + expert rating as RQ3 | Keep, but the ethics timeline must be in the report; make clear RQ4 does not depend on the survey (the default HQ definition guarantees that) — already stated |
| Scope size | 4–5 RQs | 5 RQs incl. a confirmatory block | Borderline large; Ernst & Baltes warn against protocols that "miss aspects that only emerge in Stage 2". Consider demoting RQ5 (classifier/linter) to "if time permits" or to a one-paragraph extension so reviewers do not judge feasibility on it |
| Reviewer pool expectations | Mining methods (PyDriller, Kaplan–Meier, κ) | Same toolbox; CodeQL at scale is the one heavy step | State CodeQL feasibility with a number (languages covered, CPU-time per repo from a 50-repo trial) — a trial run is cheap and pre-empts the main feasibility question |
| Qualitative plan reliability (a known rejection reason) | Must be explicit | Explicit for taxonomy and rubric; thematic coding of survey open answers lacks an agreement metric | **Gap** — add two coders + κ (or negotiated agreement) for survey open answers |
| Construct definition (a known rejection reason) | "Productivity" was flagged as hard | "Security requirement unit" and "quality" are defined operationally; "security event" is a composite | Add a sentence justifying the composite event and committing to report each event type separately |

# 4. Where the draft is stronger than the accepted precedents

- A confirmatory block with pre-specified models, direction, correction and support criteria — the accepted 2023–25 mining reports either had none or stated only null hypotheses.
- Explicit confounder strategy (pre-file maturity index, within-repository pre/post, template provenance) — none of the accepted reports handles confounding at this level.
- Computed power rather than a rule of thumb.
- Positive controls for the oracle (CodeQL on known-GHSA repos) and for the filter (reproducing the 14.8% of Agent READMEs).

# 5. Where it is weaker, in priority order

1. **No pilot numbers.** This is the single most common weakness Ernst & Baltes identify, and every accepted report has at least a count. Running the filter over the Galster Zenodo set is a one-day task and yields: number of security-bearing files, units per file, a first category distribution, filter precision on 100 flagged files. Put this in a half-page "Pilot" subsection with one table.
2. **No separate Related Work section.** Add ≈0.4 page.
3. **Keyword table missing.** Add as Table II (term, source standard, expected FP risk).
4. **CodeQL feasibility unquantified.** A 50-repository trial gives CPU-time per repo and language coverage; one sentence.
5. **Survey thematic coding lacks a reliability statement.** One sentence.
6. **Scope.** Demote RQ5 to a conditional extension or trim it to the classifier only (drop the linter from the protocol; it can appear in Stage 2 as an artefact).

With 1–5 added the body grows to ≈5.7–6.0 pages, which is exactly the budget; demoting RQ5 (item 6) buys the space back.

# 6. Two track-specific risks to plan for

- **Continuity acceptance instead of IPA.** The track reserves CA for studies whose analysis "depends heavily on the data" — typical for exploratory mining. The confirmatory H1–H3 block is our main defence; keep it prominent and make sure the exploratory RQs do not read as the main contribution.
- **Reviewer continuity and authorship lock.** The same four reviewers follow the report to EMSE; PC members who review it cannot later join as authors; authorship changes need a signed form. Fix the author list before 20 Nov.

# Sources

- MSR 2023 RR track — https://conf.researchr.org/track/msr-2023/msr-2023-registered-reports
- MSR 2024 RR track — https://2024.msrconf.org/track/msr-2024-registered-reports
- MSR 2025 RR track — https://2025.msrconf.org/track/msr-2025-registered-reports
- MSR 2027 RR track — https://2027.msrconf.org/track/msr-2027-registered-reports
- Hennig et al. 2023 — https://arxiv.org/html/2304.06367v2
- Recupito et al. 2024 — https://arxiv.org/html/2403.08311v1
- Guglielmi et al. 2025 — https://arxiv.org/html/2504.06808v1
- Koohjani & Costa 2025 — https://arxiv.org/html/2504.06040v1
- Ernst & Baltes, Registered reports in software engineering, EMSE 2022 — https://link.springer.com/article/10.1007/s10664-022-10277-5
