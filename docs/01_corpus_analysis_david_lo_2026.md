---
title: "From David Lo's 2026 Corpus to an AI × Security × Requirements Engineering Paper"
subtitle: "Analysis of 20 papers (Oct 2025 – Oct 2026) and three concrete paper proposals"
author: "Prepared for Krzysztof Wnuk — 29 October 2026"
---

# 1. Executive summary

The 20 papers co-authored by David Lo in the project folder span EMNLP (3), ISSTA/PACMSE (5), ASE (6), one journal (JSEP) and four arXiv preprints (two cs.CR). **Nine of the twenty are security- or privacy-relevant; none is a requirements-engineering (RE) paper.** The RE angle appears only implicitly: requirements show up as prompts, inline instructions, comments, reasoning traces, or "hardened" security prompts that the models are supposed to honour — and several of these papers show that they do *not* honour them reliably.

That is the opening. Lo's group has built, in the last twelve months, almost every component needed for a strong paper on *security requirements as first-class inputs to AI coding* — benchmarks of insecure generations (P18), model-level hardening and its trade-offs (P03), instruction-aware completion (P07), evidence that NL context helps only when its *content* is correct (P02), reasoning-trace interventions (P15), privacy-preserving question formulation (P20), security knowledge graphs (P01), and the "what makes a good X" MSR template (P08). What nobody in that corpus has done is treat the *requirement* — its form, specificity, provenance and traceability — as the independent variable. That is where RE expertise is the differentiator, and it is the paper proposed in Section 5.

Three proposals are given in increasing cost: (A) an MSR study of security requirements in agent instruction files (cheap, 4–6 months, no GPU); (B) an empirical study plus lightweight tool on security-requirement fidelity in LLM/agentic code generation (the flagship; 8–12 months); (C) a security-knowledge-graph retrieval layer that decides *which* security requirement applies to a task (a natural follow-up to A+B and to Athena/SafeEdit).

# 2. The corpus at a glance

| # | File | Short title | Venue | Lo's role | Security | RE |
|---|---|---|---|---|---|---|
| P01 | 2026.emnlp-main.2233 | Athena: affected-library identification via KG completion | EMNLP 2026 | 7th/8 | HIGH | LOW |
| P02 | 2026.findings-emnlp.916 | What makes comments help code generation | EMNLP Findings 2026 | 4th/5 | LOW | MED |
| P03 | 3832254 | Model editing for secure code generation (SafeEdit) | ISSTA 2026 | last | HIGH | LOW–MED |
| P04 | 3832102 | Delta: differential testing of DRL agents | ISSTA 2026 | last | LOW–MED | LOW |
| P05 | 3832162 | TestDecision: RL for sequential test generation | ISSTA 2026 | 6th/7 | LOW | LOW–MED |
| P06 | 3832262 | E2WR: WebAssembly binary reduction | ISSTA 2026 | 3rd/4 | MED | LOW |
| P07 | 2026.findings-emnlp.191 | IFIM: instruction-aware fill-in-the-middle | EMNLP Findings 2026 | last | LOW | **HIGH** |
| P08 | JSEP Lu 2026 | What makes a good model card? | JSEP 2026 | 7th/8 | LOW | MED |
| P09 | 3832783.3837522 | Demystifying Solana bots | ASE 2026 | 4th/8 | HIGH | LOW |
| P10 | 3832783.3837474 | ReCite: stale function references in Linux comments | ASE 2026 | last | MED | MED |
| P11 | 3832167 | Seeing is coding: VLMs for code understanding | ISSTA 2026 | 9th/10 | LOW | LOW |
| P12 | 3832783.3834369 | Optimo: multi-level code optimisation | ASE 2026 | 5th/6 | LOW | LOW |
| P13 | 3832783.3834339 | BinJudgeBench: LLM-as-judge for binary RE | ASE 2026 | last | HIGH | LOW |
| P14 | 3832783.3834355 | AgentExecutor: partial code execution | ASE 2026 | last | MED | LOW |
| P15 | 3832783.3834387 | Reasoning and social bias in generated code | ASE 2026 | last | MED | MED |
| P16 | 3832783.3837437 | AgentChaos: fault injection for agent systems | ASE 2026 | last/13 | MED | LOW |
| P17 | 2610.12569 | SWE-Duel: self-scaling arena for coding agents | arXiv (ICLR'27 sub.) | last | MED | LOW–MED |
| P18 | 2610.14453 | SecReason: in-stream vulnerability detection & repair | arXiv cs.CR | last | **HIGH** | LOW |
| P19 | 2610.25937 | RAGLeak: supply-chain privacy backdoors in RAG | arXiv cs.CR | 9th/10 | **HIGH** | LOW |
| P20 | 2610.24824 | Teaching code agents to ask without leaking code | arXiv cs.AI | 2nd-last | **HIGH** | MED |

Observations:

- **Position.** Lo is last author on 11/20 — the "lab head" position. In the other nine he is a mid-list author on papers led by partner labs (Nanjing, Zhejiang, HK PolyU, Fudan, Hangzhou City Univ.). The recurring SMU core is Zhensu Sun, Jieke Shi, Chengran Yang, Junda He, Weifeng Sun, plus Zhou Yang (now Alberta) and Lwin Khin Shar (security). For a security + AI paper the natural SMU contacts are Zhensu Sun (SecReason, SWE-Duel, IFIM, UVA) and Lwin Khin Shar.
- **Venues.** Throughput is driven by submitting the same recipe to ASE/ISSTA/FSE and, for anything with an NLP flavour, to EMNLP. Preprints go up on arXiv within weeks of submission.
- **Topic drift 2025→2026.** Of the four newest preprints (Oct 2026), three are security/privacy of *AI coding agents* (P18, P19, P20). That is the frontier Lo is moving toward, and it is exactly the frontier where RE has not yet been applied.

# 3. How a David Lo paper is built (patterns across the 20)

These are the recurring structural moves; a new paper that follows them will read as "from the same school".

1. **Open with a measured gap, not an opinion.** A pilot study or small empirical study quantifies the failure mode before any tool is proposed: 52% vs 52% coverage with/without feedback (P05); 13–61% insecure delivery despite passing tests (P18); 7% of model cards are high-quality (P08); only 24% of an external-comment lift is recoverable by prompting (P02).
2. **"First systematic study of X" → findings boxes → a lightweight tool that the findings motivate.** P03 (study → SafeEdit), P15 (study → ProbeDebias), P13 (meta-evaluation → BinJudge), P18 (pre-delivery window → SecReason). The tool is deliberately small (a LoRA probe, a regulariser, an MLP router, a serving-layer monitor), so the empirical part carries the contribution.
3. **Enumerate challenges C1–C3 and answer each with one technique** (P06, P12, P18). Reviewers can map contribution to challenge one-to-one.
4. **Build the benchmark yourself, with expert annotation and reported agreement.** Krippendorff α, Cohen κ, pilot-then-split protocols, external expert re-annotation (P07, P08, P09, P10, P13). Leak-free evaluation is a stated design goal: post-cutoff datasets, NoCtx baselines, temporal splits, "fresh repos" (P01, P05, P11, P17).
5. **Frame the contribution as a trade-off and measure both sides.** Security vs functional correctness (P03, P18), privacy vs utility (P20), stealth vs fidelity (P19), task difficulty vs author capability (P17). Harmonic-mean trade-off scores and "secure-and-correct" joint metrics are reused.
6. **Executable acceptance gates instead of judgement.** Replay gate (P20), trigger verification (P16), self-repair gate (P17), performance validation at every level (P12). The group distrusts LLM-only validation and always adds an execution oracle where possible.
7. **Statistics by default.** McNemar + Holm (P02), Wilcoxon + Cliff's δ (P03, P08, P15), Bradley–Terry + bootstrap (P17), Mann–Whitney (P04). Five repetitions are the norm.
8. **Ecological validation.** 50/75 kernel patches accepted (P10); 30 real 2026 CVEs (P01); 100 real TODO/FIXME instructions (P07); later-time-window validation (P09).
9. **Dual-use / ethics paragraph on every security paper** (P01, P07, P17, P18, P19) — increasingly expected at EMNLP and cs.CR.
10. **Replication package on Zenodo/GitHub, always.**

Taken together this yields a reusable 4-RQ skeleton: *RQ1 prevalence/feasibility → RQ2 what drives it (ablation/factors) → RQ3 does the proposed intervention help, against ≥3 baseline families → RQ4 cost/robustness/generalisation*, followed by implications per stakeholder and threats.

# 4. Where the corpus touches security and RE — and where it stops

## 4.1 Security cluster

| Paper | What it establishes | What it leaves open (their own words) |
|---|---|---|
| P18 SecReason | 13–61% of functionally correct generations are insecure; models draft code inside their reasoning; a "hardened prompt" never exceeds 66% secure and *72% of its insecure runs identified the flaw yet shipped it*. | Only unit-level tasks; no agentic pipelines; rules overfit to the corpus; no comparison with decoding-time defences. |
| P03 SafeEdit | Model editing injects security knowledge (+15–25% SR) but generalises poorly to unseen CWEs and costs functional correctness; CoSec vs editing are complementary. | "Hybrid hardening strategies"; which security knowledge to inject is not addressed. |
| P01 Athena | Structured (graph) security knowledge beats text-only matching; a 110M graph model beats a 7B generative one. | Apply KG completion to other supply-chain tasks; cross-ecosystem transfer. |
| P19 RAGLeak | Supply-chain backdoor in a fine-tuned generator leaks private RAG context at 58–100% ASR, undetected by similarity defences. | Adaptive detection, backdoor removal. |
| P20 UVA | A coding agent can be taught to ask a cloud expert *abstract* questions that preserve decision-relevant technical conditions while cutting leaked identifiers 3.7×. "Privacy by silence" is a measurement pitfall. | Inference-based leakage; necessity of consultation. |
| P17 SWE-Duel | 27% of frontier-authored PRs with hidden defects (incl. security vulnerabilities) pass frontier review. | Freshness policy; reviewer defences. |
| P16 AgentChaos | 22–66% of agent failures under API faults are *silent*; robustness depends on implementation, not model. | Defences: response validation, retry. |
| P13 BinJudgeBench | LLM-as-judge reaches 63–71% correlation with expert reverse engineers; no single judge config fits all tasks. | — |
| P09 Solana bots | Taxonomy + dependency-lag + on-chain fingerprints of MEV/sniping bots. | Cross-chain comparison. |

## 4.2 RE / intent cluster

| Paper | RE-relevant finding |
|---|---|
| P07 IFIM | Developer intent expressed as a structured instruction section raises Pass@1 from 88→95% and 15→21%; the *same* intent written as a plain comment is ignored or harmful. Form of the requirement channel matters. |
| P02 Comments | NL context helps only when its content describes a correct solution (+17.2%); wrong-topic context hurts (−20.8%); models cannot self-elicit the right content (≤24% recovered). |
| P15 ProbeDebias | NL prompts without a fairness constraint produce biased decision code; intervening on the intermediate reasoning (the model's own "specification") fixes 84% of it. Authors say security/privacy is the next target. |
| P20 UVA | The skill learned is writing a role/type-level problem description that keeps the conditions needed for a correct decision — essentially a good abstract specification. |
| P08 Model cards | A full "what makes a good X" methodology for documentation artefacts, with practitioner survey, classifier and survival analysis. |
| P10 ReCite | NL-to-code traceability maintained under code evolution, with LLM-based repair grounded in history. |

## 4.3 The gap

Across all 20 papers, "security requirement" is operationalised in exactly three ways: a CWE label in a benchmark, a one-line "hardened" system prompt, or a static-analysis rule. Nobody varies the *requirement itself* — its specificity (ASVS-level vs "write secure code"), its position (system prompt, instruction file, inline comment, issue text), its provenance (standard, regulation, team policy), or its traceability to the produced code and tests. Yet P02 and P07 show the channel and content of NL context are decisive, P18 shows models recognise security flaws they still ship, and P03 shows injected security knowledge does not transfer across CWEs. The missing variable is the one RE studies: **how the requirement is written, where it lives, and whether it can be verified.**

# 5. Three paper proposals

Each follows the Section 3 skeleton and names the Lo papers it reuses.

## Proposal A — "What Makes a Good Security Requirement for a Coding Agent?" (MSR/empirical, lowest cost)

**Idea.** Agent instruction files (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `.github/copilot-instructions.md`, `.windsurfrules`) are now the de-facto requirements documents for AI coding. They are public on GitHub in tens of thousands. Nobody has studied the security requirements inside them. This is P08's methodology applied to a new artefact, with P09's taxonomy pipeline.

**RQs.**
RQ1 — What security requirements do practitioners write for coding agents? (taxonomy via LLM-assisted open card sorting, κ reported; map to ASVS/CWE/OWASP LLM Top-10)
RQ2 — How are they written? (specificity, verifiability, imperative vs rationale, position in file; compare with classic requirement-quality criteria — unambiguous, verifiable, atomic)
RQ3 — Do repositories with (well-written) security requirements differ in outcome? (CodeQL/Dependabot alerts, secret leaks, time-to-fix; survival analysis as in P08)
RQ4 — Can quality be predicted/flagged automatically, and what do practitioners want? (classifier + survey of maintainers, as in P08)

**Data.** GitHub search + GH Archive; stratified random sample (≥1,000 files) for coding, full population for outcomes. Practitioner survey (target 60–100, as in P08).

**Why it fits Lo's pattern.** "What makes a good X" + "Demystifying X" templates; cheap; produces a dataset others will reuse; direct implications for tool vendors. **Venue:** MSR 2027 (deadline ~Dec 2026/Jan 2027) or ICSE-SEIP; journal extension in EMSE/TOSEM.

**RE contribution.** First empirical characterisation of requirements written *for* an AI developer rather than *by* one; tests whether 30 years of requirement-quality criteria predict agent behaviour.

## Proposal B — "Do Security Requirements Survive Code Generation? Security-Requirement Fidelity in LLM and Agentic Coding" (flagship)

**Idea.** Treat the security requirement as the independent variable and measure whether it is honoured, using P18's benchmarks and oracles. Then propose a small tool that closes the loop.

**Study design (RQ1–RQ3).**
- *Requirement specificity ladder* for each task: L0 none; L1 generic ("write secure code"); L2 category ("prevent injection"); L3 standard-level (ASVS item / CWE with remediation); L4 verifiable (acceptance test or Semgrep rule attached).
- *Requirement channel*: system prompt vs instruction file vs inline `#!` instruction (P07's IFIM section) vs issue text.
- *Subjects*: 173 tasks from CWEval + SecCodeBench (P18), extended with 50–100 repository-level tasks; 6–8 open-weight models plus 2 agent harnesses (mini-swe-agent, Codex CLI, as in P17/P20).
- *Oracles*: functional tests + Semgrep/CodeQL + exploit payloads from the benchmarks; "secure-and-correct@1" as primary metric (P03, P18).
- RQ1 — How much does requirement specificity/channel change secure-and-correct rate? (expected: large effect; P18's 66% ceiling for hardened prompts is the L1 baseline)
- RQ2 — Where do requirements get lost? Trace analysis of reasoning (P18, P15): is the requirement mentioned, mis-prioritised against functional requirements, or dropped at delivery? This is the RE "requirement erosion" question with execution-grounded evidence.
- RQ3 — Does traceability survive? Does generated code/tests reference the requirement (ID, comment, test name)? Can a reviewer or P10-style tool link them back?

**Tool (RQ4): ReqGuard / SecSpec.** Compile L3 requirements into L4 checks automatically (ASVS item → Semgrep rule or property test, generated by an LLM and validated on seed corpora), and enforce them (a) in-stream with P18's SecReason mechanism, or (b) as an acceptance gate with P20/P17-style replay. Baselines: raw, hardened prompt, post-hoc repair, SecReason with generic rules, SafeEdit (P03). Report tokens and latency, as the group always does.

**Expected headline.** "Security requirements written at standard level with an attached check are honoured at X%; the same requirement as a generic prompt at Y%; models recognise the requirement in Z% of traces where they still violate it."

**Venue:** ICSE 2028 / FSE 2027 / ASE 2027; an EMNLP version if the trace analysis dominates. **Cost:** 8–12 months, ~2 GPUs (open-weight 7–35B models), API budget ≈ USD 2–3k (P17 spent $2.1k).

## Proposal C — "A Security-Requirements Knowledge Graph for AI Coding" (follow-up)

**Idea.** P03's unsolved question is *which* security knowledge to inject and why it does not transfer across CWEs; P01 shows graph-structured security knowledge beats text. Build a KG linking requirement sources (ASVS, CWE, CAPEC, NIST SSDF, EU CRA articles) to code contexts (APIs, frameworks, languages) and use KG completion to retrieve the applicable requirements for a task, feeding Proposal B's compiler or SafeEdit's editing set. Evaluate by (i) retrieval precision against expert annotation, (ii) improvement in unseen-CWE generalisation when editing/hardening is driven by the graph. This is the regulatory/compliance angle (CRA, NIS2) that Lo's group does not have and that fits European funding.

# 6. Recommended sequencing

1. **Now–Jan 2027: Proposal A** to MSR 2027. Dataset + taxonomy are reusable in B.
2. **Jan–Sep 2027: Proposal B** — the empirical half can be written as a stand-alone registered report (ICSE/FSE RR tracks) while the tool matures.
3. **2027–28: Proposal C** as the funding-oriented extension (CRA compliance), possibly with SMU (Zhensu Sun, Lwin Khin Shar) as co-authors to inherit SecReason/SWE-Duel infrastructure.

# 7. Threats to this analysis

- Summaries for 17 of the 20 papers were produced from extracted PDF text by automated readers and spot-checked, not read line-by-line by one reviewer; numbers quoted above should be verified against the PDFs before being cited.
- "Last 10 years" in the project description is not covered — this corpus is 12 months. The patterns in Section 3 are consistent with Lo's earlier work but are inferred from 2026 papers only.
- Venue/deadline estimates for 2027 are from general knowledge, not checked.

# Appendix — per-paper summaries

See the accompanying file `paper_summaries.md` (20 structured summaries: title, venue, authors, problem, method, findings, future work, security/RE relevance, reusable pattern).
