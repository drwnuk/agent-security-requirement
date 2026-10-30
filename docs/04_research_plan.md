---
title: "Research Plan — What Makes a Good Security Requirement for a Coding Agent?"
subtitle: "An MSR study of security requirements in agent instruction files (AGENTS.md, CLAUDE.md, .cursorrules, copilot-instructions.md, SKILL.md)"
author: "Draft for Krzysztof Wnuk (BTH) — 29 October 2026 — v0.1"
---

# 1. One-paragraph summary

Agent instruction files are now the de-facto requirements documents that developers write *for* AI coding agents. Four 2025–26 studies have measured what these files contain and consistently find that security is rare — 8.7% of CLAUDE.md files (Chatlatanagulchai et al. 2025), 14.8% of 2,303 context files (Agent READMEs, Hassan/Iida group 2025/26) — but none has analysed the security content itself: what is asked for, how it is phrased, whether it is verifiable, where it comes from, and whether it is associated with anything observable in the repository. This study fills that gap by applying the "What makes a good X?" methodology from Lu et al. (JSEP 2026, with David Lo) — platform-scale sampling, closed/thematic coding with reported agreement, practitioner survey plus expert rating to define quality, multi-classifier prediction, feature-importance with effect sizes, and survival analysis against an outcome — to security requirements for coding agents. It needs no GPU; the main costs are annotation time and a modest API budget for an optional behavioural validation. Because the MSR 2027 technical deadline (23 Oct 2026) has passed, the plan targets the **MSR 2027 Registered Report track (13 Nov 2026)** for stage-1 acceptance, with the full paper going to **MSR 2028 / ICSME 2027 / ESEM 2027** and the dataset to the **MSR 2027 Data & Tool Showcase (10 Nov 2026)**.

# 2. Positioning: what exists and what is open

| Prior work | Data | What they did | What they did *not* do |
|---|---|---|---|
| Chatlatanagulchai et al., *Agentic Coding Manifests* (arXiv 2509.14744, Sep 2025) | 253 CLAUDE.md files / 242 repos | 15-category content taxonomy; structure analysis | Security = one label at 8.7%; no analysis of the content |
| Chatlatanagulchai, Li, Kashiwa, Reid, … Adams, Hassan, Iida, *Agent READMEs* (arXiv 2511.12884, v2 Aug 2026) | 2,303 context files / 1,925 repos | 16 instruction types; evolution "like configuration code"; security 14.8%, performance 14.5% | No security taxonomy, no quality notion, no outcomes |
| Galster, Abubakar, Mohsenimofidi, Treude, Lulla, Baltes, *Configuring Agentic AI Coding Tools* (Feb 2026 snapshot) | 32,564 engineered repos → 2,926 with agent config; **scripts + data on Zenodo** | 8 configuration mechanisms (context files, skills, subagents, hooks, MCP, rules…) and adoption | No content analysis of security; hooks/MCP security "not examined" |
| Treude & Baltes, *Context Rot* (arXiv 2606.09090, Jun 2026) | 612 files / 356 repos (Galster subset) | Stale code references in 23% of repos via DOCER | The word "security" does not appear |
| Lulla et al., *Impact of AGENTS.md on Efficiency* (ICSE JAWs 2026) | 124 PRs / 10 repos, Codex | −28.6% median runtime with AGENTS.md | Correctness/security of output not evaluated; security files filtered out |
| Xu & Yan, *Agent Skills* survey (arXiv 2602.12430) | survey | 26.1% of community skills vulnerable; scripts ≈2.1× odds | Skills as attack surface, not as requirement carriers |
| Lu et al., *What Makes a Good Model Card?* (JSEP 2026, D. Lo) | 758 HF model cards | **The method template**: coding → survey+expert quality definition → 13 classifiers → determinants → survival analysis | Different artefact |
| Chen et al., *Insecure Coding Preferences in Long-Term Memory* (ISSTA 2026, D. Lo) | 4 LLMs × 5 languages | Security requirements in prompt/memory cut vulnerabilities 19.7–33.6 pp, cost ≤15.9 pp Pass@k | Lab prompts only; no in-the-wild requirements |

**Open questions this study answers.** (1) What security requirements do practitioners actually write for agents, and how do they map to standards (ASVS, CWE, OWASP LLM Top-10, SSDF)? (2) Are they *good* requirements by RE criteria (unambiguous, verifiable, atomic, rationale-bearing) and by practitioner judgement? (3) Does the presence/quality of security requirements co-vary with observable security signals in the repository? (4) Can quality be predicted, and what do maintainers want from tooling? Optionally (5): does the quality of a real-world security requirement change agent behaviour?

**The RE contribution** — the differentiator from the Treude/Baltes and Hassan/Iida groups, both of which are better placed to do more general content studies — is treating the instruction file as a requirements specification and applying 30 years of requirement-quality criteria (IEEE 830/ISO 29148, Génova et al., Femmer et al. "requirements smells") to an artefact read by a machine.

# 3. Research questions

| RQ | Question | Output |
|---|---|---|
| **RQ1 — What** | Which security requirements do developers write for coding agents, and how are they distributed across tools, ecosystems and project types? | Security-requirement taxonomy (2 levels), mapped to ASVS/CWE/OWASP-LLM/SSDF; prevalence per category |
| **RQ2 — How** | How are these requirements written: specificity, verifiability, modality (MUST/SHOULD/never), rationale, scope (file/dir/global), position in file, and provenance (copied from a standard, template, or vendor doc)? Which RE quality criteria and requirement smells do they satisfy/violate? | Quality rubric; quality-score distribution; smell catalogue with examples |
| **RQ3 — Why/How-well** (quality definition) | What do practitioners consider a good security requirement for an agent, and which of their criteria agree with RE criteria? | Survey (n≈60–100) + expert rating of themes → operational definition of "high-quality security requirement" (as in Lu et al.: a card is high-quality if it has Overview+Evaluation+Usage) |
| **RQ4 — Outcomes** | Are presence and quality of security requirements associated with repository security signals, controlling for size, age, popularity, language and security-maturity confounders? | Regression + survival analysis |
| **RQ5 — Prediction & tooling** | Can quality be detected automatically from file features, and which features are the strongest determinants? What tooling do maintainers want? | Classifier comparison (classical, BERT-family, zero-shot LLM); feature importance with Cliff's δ; survey open-ended coding |
| **RQ6 (optional, behavioural)** | Does a high-quality vs. low-quality real-world security requirement change what an agent produces on a security-sensitive task? | Small controlled replay (see §5.6) |

# 4. Data

## 4.1 Population and sampling

- **Start from the Galster et al. Zenodo dataset** (32,564 engineered repositories; 2,926 with agent configuration; Feb 2026 snapshot). Reusing it saves ~1 month, makes results comparable, and follows Lo's "build on the community's benchmark" habit. Refresh with a GitHub search in Nov 2026 (the ecosystem roughly doubled in 2026) using the same filters: non-fork, ≥2 contributors, licence, "engineered" (same GPT-based README classifier or the Munaiah et al. reaper heuristics).
- **File types in scope**: AGENTS.md, CLAUDE.md, GEMINI.md, .cursorrules / .cursor/rules/*.mdc, .github/copilot-instructions.md, .windsurfrules, .clinerules, SKILL.md (Claude skills), .claude/agents/*.md (subagents), and hook/MCP configuration where it carries natural-language constraints.
- **Security-bearing subset**: keyword + embedding filter (ASVS/CWE vocabulary, "secret", "credential", "sanitis/ze", "inject", "auth", "CVE", "dependenc", "never commit", …) with a manually validated recall check on 200 random files (expect 10–20% of files to be security-bearing, i.e. ~400–900 files from the Zenodo set and 1,000–2,000 after refresh).
- **Annotation sample**: all security-bearing files if ≤1,000; else a stratified random sample of 800 (95% CI, ±3.5% as in Lu et al.), stratified by tool and language.
- **Unit of analysis**: the individual security requirement (a sentence or bullet), nested in file, nested in repository. Expect 3–8 requirements per security-bearing file → ~3,000–6,000 requirement units.

## 4.2 Repository-level outcome and control variables (RQ4)

Observable without repository admin rights:

| Signal | Source | Note |
|---|---|---|
| OpenSSF Scorecard (18 checks incl. Dependency-Update-Tool, SAST, Token-Permissions, Pinned-Dependencies, Vulnerabilities) | public API / run locally | primary composite outcome |
| CodeQL alert density | run CodeQL ourselves on the default branch at snapshot (JS/TS, Python, Java, Go, C/C++) | ~1–2 CPU-min/repo; 3,000 repos ≈ a few CPU-days |
| Secrets in history | gitleaks / trufflehog | count + first-commit date |
| Published advisories | GitHub Security Advisories (GHSA) API; OSV | public |
| Dependabot/Renovate config present; SECURITY.md present | file presence | security-maturity confounder, not outcome |
| Agent-authored PRs | PR author = copilot/codex/claude bots, or "Co-authored-by" trailers, or PR body signatures | lets us test whether *agent* commits differ |
| Controls | stars, forks, age, contributors, LOC, primary language, commits/month | standard |

Dependabot *alerts* require admin scope and are therefore replaced by Scorecard's Vulnerabilities check + OSV lookup on the lockfile; this is stated as a limitation.

## 4.3 Time dimension (survival analysis)

Every file version is available through Git history (Agent READMEs showed these files evolve through frequent small additions). We reconstruct, per repository: date the instruction file was introduced; date security content first appeared; subsequent edits. Survival models then use *time from file introduction to first security-relevant event* (first CodeQL high-severity alert introduced, first secret committed, first GHSA) and *time until the security section is first edited* (does it rot?), with security-requirement quality as covariate. Lu et al. used time-to-last-update as a proxy for longevity; we add the security-event clocks.

# 5. Method, per RQ

## 5.1 RQ1 — Taxonomy

1. **Pilot**: two annotators open-code 100 security requirement units; build codebook; third annotator adjudicates (pilot-then-split protocol from ReCite/Lo group).
2. **LLM-assisted pre-labelling** (as in Solana-bots P09): an LLM proposes category labels for all units; humans validate a stratified 10% (≥300 units) and report Cohen's κ; target κ ≥ 0.75 before trusting bulk labels.
3. **Mapping** each leaf category to ASVS v5 chapters, CWE Top-25, OWASP LLM Top-10 (for agent-specific items such as "never read .env", "do not call external URLs", "do not run destructive git commands"), and NIST SSDF practices. Expect a split between *product-security* requirements (what the code must do) and *agent-conduct* requirements (what the agent may do) — a distinction absent from all prior taxonomies and the first finding worth a figure.

## 5.2 RQ2 — Quality rubric

Rubric dimensions (each 0/1/2), derived from ISO/IEC/IEEE 29148 and the requirements-smells literature:

- **Specificity**: generic ("write secure code") → category ("prevent SQL injection") → standard-level ("parameterise all DB queries; ASVS 5.3.4").
- **Verifiability**: can a reviewer or tool decide compliance? (0 = no; 1 = human-checkable; 2 = machine-checkable / references a linter, test, or CI gate).
- **Modality / imperative strength**: MUST/NEVER vs. SHOULD vs. descriptive.
- **Rationale present** (the "why", which P02 showed matters for content correctness).
- **Scope precision**: global vs. path/glob-scoped (Cursor rules support globs).
- **Atomicity**: one requirement per sentence.
- **Smells** (count): vagueness terms, subjective language, negative framing without alternative, dangling references to non-existent files/tools (links to Treude & Baltes' context rot).
- **Provenance** (categorical): verbatim/near-verbatim from vendor docs or a public template (detect by n-gram match against a crawled template corpus: awesome-cursorrules, Anthropic/OpenAI docs, cursor.directory), from a standard, or project-specific.

Two annotators score 400 units; κ/ICC reported; the rest scored by an LLM judge calibrated on the human set (same protocol as P02's intent judge and P15's bias judge, with agreement reported).

## 5.3 RQ3 — Practitioner survey and expert rating

- **Survey** (target 60–100 responses, as in Lu et al.): maintainers of repositories in the sample (opt-in via issue/email per GitHub ToS and BTH ethics approval), plus a snowball through the BTH industry network (SESAM partners) and the SRAP consortium. Questions: which security instructions they wrote and why; what they expect the agent to do with them; whether they have observed compliance/violations; what makes an instruction effective; what tooling they want. Three open-ended questions coded thematically (as in Lu et al.).
- **Expert rating**: 8–10 security/RE experts rate the RQ1 categories and RQ2 dimensions for importance (1–5); ICC reported. Combine to an operational definition of a *high-quality security requirement set* (e.g. ≥1 product-security and ≥1 agent-conduct requirement, each at specificity ≥1 and verifiability ≥1).

## 5.4 RQ4 — Outcomes

- Repository-level regression (negative-binomial for alert counts; logistic for "any secret", "any GHSA") with the quality score and presence indicators as predictors and the §4.2 controls, plus a security-maturity index (SECURITY.md, Dependabot config, Scorecard SAST check) to avoid the obvious confound that security-conscious teams both write requirements and have cleaner repos.
- Kaplan–Meier + Cox models for the three clocks in §4.3; log-rank tests; report hazard ratios with CIs.
- Diff-in-diff style check where possible: alert density in the 90 days before vs. after the security requirement was added, using repositories that added security content *after* the file existed as their own controls.
- Agent-PR sub-analysis: do agent-authored PRs in repositories with high-quality requirements trigger fewer CodeQL alerts than those in repositories without?

All effects reported with Cliff's δ / HR and CIs; Wilcoxon or Mann–Whitney for pairwise comparisons; Holm correction across the outcome family.

## 5.5 RQ5 — Prediction and determinants

Replicate Lu et al.'s classifier grid on the file level: 15–20 features (word count, number of security units, specificity mean, verifiability mean, number of code blocks/links/tables, references to tools, update interval, file age, tool type) → LR, RF, XGBoost, SVM, fine-tuned CodeBERT/BERT, and zero-shot/few-shot LLM; stratified 10-fold CV; ROC-AUC / PR-AUC (class imbalance expected); Wilcoxon + Cliff's δ between classifiers; RF feature importance. Deliver a lightweight linter ("SecReqLint") that flags smells and suggests the ASVS mapping — the "actionable tool" Lu et al. list as future work.

## 5.6 RQ6 (optional) — Behavioural validation

Take 20 real security requirements at each quality level (low/high) from the corpus, insert them into the instruction file of a fixed repository, and run one open-weight agent (e.g. mini-swe-agent + Qwen3-Coder) on 30 security-sensitive tasks drawn from SecureVibeBench/CWEval where the requirement is applicable; measure secure-and-correct rate with the benchmark oracles. 2 levels × 30 tasks × 3 runs ≈ 180 runs; API cost ≈ USD 200–500 or a single 48 GB GPU for a week. Even a small, significant effect links the MSR findings to behaviour and pre-empts the "so what?" review. If omitted, it becomes the bridge to Proposal B.

# 6. Expected contributions (as they would appear in the paper)

1. The first taxonomy of security requirements written for AI coding agents, distinguishing product-security from agent-conduct requirements, mapped to ASVS/CWE/OWASP-LLM/SSDF, with prevalence figures.
2. A requirements-quality rubric and smell catalogue for machine-read instructions, with inter-rater reliability and an LLM-judge calibration.
3. A practitioner-grounded definition of a high-quality security requirement for agents, from a survey and expert rating.
4. Evidence on whether security requirements co-vary with repository security outcomes, including a survival analysis and an agent-PR sub-analysis.
5. A classifier/linter and an open dataset (requirement units, labels, rubric scores, repository outcomes) released on Zenodo.

# 7. Timeline (assumes start 3 Nov 2026; two people at ~50% + supervisor)

| Period | Activity | Milestone |
|---|---|---|
| **Wk 1–2 (3–13 Nov 2026)** | Write stage-1 Registered Report (RQs, hypotheses for RQ4, analysis plan, sample-size justification, pilot numbers from 100 files); secure Galster Zenodo data; ethics application for survey at BTH | **Submit MSR 2027 RR by 13 Nov**; optionally MSR Data Showcase short paper on the refreshed corpus by 10 Nov |
| Wk 2–5 (Nov) | GitHub refresh crawl; file extraction incl. history; security-bearing filter with recall check | Corpus v1 frozen (≈2,000–3,000 security-bearing files) |
| Wk 4–9 (Nov–Dec) | RQ1 pilot coding → codebook → LLM pre-labelling → validation (κ) | Taxonomy v1 |
| Wk 8–13 (Dec–Jan) | RQ2 rubric; 400 human-scored units; LLM-judge calibration; provenance matching | Quality scores for all units |
| Wk 10–16 (Jan–Feb 2027) | Survey launch (after ethics); expert rating | ≥60 responses; quality definition |
| Wk 12–18 (Jan–Mar) | Outcome extraction: Scorecard, CodeQL batch, gitleaks, GHSA/OSV, agent-PR detection; survival clocks | Outcome table |
| Wk 18–22 (Mar) | RQ4 models; RQ5 classifiers; SecReqLint | Results |
| Wk 20–24 (Mar–Apr) | Optional RQ6 | — |
| Wk 22–26 (Apr) | Writing; internal review; replication package | Full paper draft |
| **May–Jun 2027** | Submit full paper: ESEM 2027 (~Apr/May deadline) or ICSME 2027 (~Mar/Apr) if ready, else **MSR 2028 (Oct 2027)** as RR stage-2 | Submission |

Deadline sources: MSR 2027 technical track closed 23 Oct 2026; RR 13 Nov 2026; Data & Tool Showcase 10 Nov 2026; conference 26–27 Apr 2027, Dublin, co-located with ICSE. ESEM/ICSME 2027 dates were not yet published at the time of writing — verify.

# 8. Team and roles

| Role | Who (suggested) | Tasks |
|---|---|---|
| Lead / RE framing | K. Wnuk | RQ design, rubric, survey, writing; SRAP WP1 link |
| Security framing | W. Ma or D. Fucci (BTH) | ASVS/CWE mapping, CodeQL/Scorecard pipeline, threats |
| PhD/MSc student 1 | SRAP WP1-S1 candidate or BTH master thesis | crawling, extraction, outcome pipeline, classifiers |
| PhD/MSc student 2 | — | annotation lead, LLM-judge calibration, survey coding |
| External | Optional: SMU (Zhensu Sun / Lwin Khin Shar) or Treude/Baltes for the Galster dataset | dataset reuse courtesy, cross-validation of taxonomy |

The annotation load (≈400 rubric units + 300 taxonomy validations + 100 pilot) is ≈60–80 person-hours per annotator — suitable as a master-thesis component.

# 9. Resources and cost

- Compute: one 8–16 core server for CodeQL/Scorecard/gitleaks batch (no GPU); ≈ 1 CPU-week.
- API: LLM pre-labelling and judging ≈ 10k calls ≈ USD 100–300; RQ6 ≈ USD 200–500.
- Ethics: BTH ethical review for the survey (~4 weeks lead time — start in week 1).
- Data: Galster et al. Zenodo package; GitHub REST/GraphQL with a research token; OSV and Scorecard public APIs.

# 10. Threats and mitigations (to pre-register)

- **Confounding in RQ4** (security-mature teams write requirements *and* have cleaner repos): include maturity index as covariate; use within-repository before/after; state association, not causation.
- **Detection validity of security-bearing filter**: manual recall check on 200 random non-flagged files; report recall.
- **LLM-judge circularity**: human-scored calibration set with reported κ/ICC; sensitivity analysis with a second judge model (Lo-group practice).
- **Template copying inflating prevalence**: provenance detection; report results with and without near-duplicate templates.
- **Ecosystem drift**: file conventions change monthly; freeze snapshot date; release crawler.
- **Survey self-selection**: report response rate and respondent profile; triangulate with expert rating.
- **Outcome measurement**: CodeQL/Scorecard are proxies; Dependabot alerts unavailable without admin rights; agent-PR detection heuristics imperfect — validate on 100 PRs.
- **Generalisability**: open-source only; proprietary instruction files (which the SRAP WP2 telemetry could later access) are out of scope.

# 11. How this feeds the larger programme

- Delivers SRAP/SCAFFOLD Year-1 milestone "initial risk-class taxonomy… for AI-authored artifacts" and answers WP1 RQ1.1 empirically.
- The requirement units at specificity ≥2 / verifiability = 2 are the seed set for Proposal B's requirement-to-check compiler.
- The ASVS/CWE/SSDF mapping is the node schema for Proposal C's knowledge graph.
- A short follow-up on *context rot of security requirements* (does the security section go stale faster than build instructions?) is a natural joint paper with Treude & Baltes, who have asked exactly that question without the security lens.

# 12. Immediate next steps (this week)

1. Decide on the Registered Report submission (13 Nov). If yes, I can draft the stage-1 report (≈6 pages: intro, RQs/hypotheses, data, analysis plan, pilot) from this document.
2. Download the Galster et al. Zenodo package and run the security-bearing filter on the 2,926 repositories to get the pilot prevalence number for the RR.
3. File the BTH ethics application for the survey.
4. Identify the two annotators.

# Sources

- MSR 2027 technical track — https://2027.msrconf.org/track/msr-2027-technical-papers
- SE deadlines list — https://se-deadlines.github.io/
- Agent READMEs — https://arxiv.org/abs/2511.12884
- Agentic Coding Manifests (Claude.md) — https://arxiv.org/html/2509.14744v1
- Configuring Agentic AI Coding Tools — https://arxiv.org/html/2602.14690v1
- Context Rot — https://arxiv.org/html/2606.09090v1
- Impact of AGENTS.md on Efficiency — https://assets.empirical-software.engineering/pdf/jaws26-agents.md-efficiency.pdf
- Agent Skills survey — https://arxiv.org/html/2602.12430v1
- Insecure Coding Preferences in Long-Term Memory — https://arxiv.org/pdf/2607.17619
- What Makes a Good Model Card? (project file) and SecureVibeBench — https://arxiv.org/abs/2509.22097
