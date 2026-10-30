---
title: "Part 2 — Additional David Lo papers and what to reuse from the SRAP/SCAFFOLD application"
author: "Prepared for Krzysztof Wnuk — 29 October 2026"
---

# 0. What this document adds

Part 1 analysed the 20 papers in the project folder. This part (a) extends the corpus with further 2025–2026 papers by David Lo and by others that bear directly on an AI × security × requirements-engineering paper, and (b) maps the already-written SRAP/SCAFFOLD application (BTH–NTU, submitted May 2026) onto the three paper proposals from Part 1, section by section, so that text, RQs and infrastructure are reused rather than rewritten.

**Access caveat.** Google Scholar, DBLP and the arXiv API all refuse automated access from this session, and Chrome was not connected, so I could not pull the full "last 100 papers" list. What follows is what web search surfaced and I verified by reading each paper's arXiv page or PDF; author lists and numbers are from the papers themselves. For the complete list, opening the Scholar page in your browser remains necessary — the SMU CV (Feb 2026) stops at 2025 entries.

# 1. Additional papers to add to the corpus

## 1.1 David Lo co-authored (verified)

| # | Paper | Venue | Why it matters for the AI×Sec×RE paper |
|---|---|---|---|
| A1 | **SecureVibeBench** (Chen, Huang, Lyu, An, Shi, Yang, Zhang, Tian, Li, Li, Zhou, Hu, **Lo** — last). arXiv 2509.22097v5, ACL 2026 long. | ACL 2026 | 105 C/C++ memory-safety tasks from 41 OSS-Fuzz/ARVO projects, multi-file edits, real vulnerability-introduction points; functional + static + dynamic checks. Best agent+LLM pair is correct *and* secure in only **23.8%**. This is the repository-level benchmark Proposal B needs beyond CWEval/SecCodeBench; tasks ask only for functionality — i.e. the security requirement is absent by design, which is exactly the L0 condition of the specificity ladder. |
| A2 | **Insecure Coding Preferences in Long-Term Memory** (Chen, Cheng, Xiao, Yang, Sun, Fang, Chen, Xu, **Lo**, Chen). arXiv 2607.17619, ISSTA 2026. | ISSTA 2026 | Memory-stored insecure preferences raise vulnerability rates by **2.7–50.3 pp**; models disclose that they used the memory in only 2.3–10.3% of outputs; **adding security requirements to prompts or memory cut vulnerability by 19.7–33.6 pp but cost up to 15.9 pp Pass@k**. Direct evidence that (i) persistent instructions are a requirements channel, (ii) security requirements trade off against functional ones, (iii) requirements can be silently overridden. This is the closest existing paper to Proposal B and must be cited and positioned against. |
| A3 | **Revisiting Vulnerability Patch Identification on Data in the Wild** (Irsan, Widyasari, Zhang, Huang, Thung, Li, Shar, Ouh, Kang, **Lo**). arXiv 2603.17266. | arXiv 2026 | NVD-trained detectors lose up to 90% F1 on silent in-the-wild fixes; zero-shot LLMs ≈ random. Shows Lo's group's "evaluate on realistic distribution" pattern; relevant to any traceability/compliance claim that depends on knowing a change is security-relevant. |
| A4 | **CoSA: Context-Aware Severity Assessment** (Jiang, Li, Yang, Zhang, Leow, Yin, Ouh, Shar, **Lo**). arXiv 2608.13928; GovTech co-authors. | arXiv 2026 | Repository-level CVSS prediction with code-property-graph pruning + LLM summaries; dataset of 6,816 CVSS-labelled instances. Relevant to Proposal C (knowledge graph) and to the "risk class" taxonomy of SCAFFOLD WP1. |
| A5 | **Towards Scalable and Cost-Efficient Vulnerability Detection: A Study on Automatic Query Generation** (Sep 2026, Lo co-author per aggregator; arXiv page not retrievable). | arXiv 2026 | LLM generation of CodeQL queries — the mechanism Proposal B's "requirement-to-check compiler" would use. Verify authorship when you have Scholar access. |
| A6 | **To Run or Not to Run: Cost-Effectiveness of Code Execution in LLM-Based Program Repair** (ISSTA 2026, listed on Lo's ISSTA profile). | ISSTA 2026 | Supports the "executable acceptance gate vs. LLM judgement" design choice. |
| A7 | **LLM for Verilog Code Generation: Literature Review and the Road Ahead** (Aug 2026). | arXiv 2026 | Only as a template: Lo's "literature review + road ahead" format (also used for vulnerability detection TOSEM 2025 and multi-agent systems TOSEM 2025) is a reliable high-citation vehicle — a "Security Requirements for AI-Assisted Development: Review and Road Ahead" would fit the same mould. |

## 1.2 Closely related work by others (needed for positioning, not by Lo)

| # | Paper | Relevance |
|---|---|---|
| R1 | **Last Secure Code Benchmark** (Wu et al., NUS; arXiv 2610.14766, Oct 2026) | 450 tasks / 150 real vulns / 7 languages / 24 CWEs / 3 vibe-coding scenarios; frontier agents pass function tests 73.6–91.3% but are functional *and* secure only 16.4–25.1%. Converging evidence with A1; use both as the "insecure-by-default" baseline. |
| R2 | **Don't Guess, Just Ask: ReqClarifyBench** (Chen et al., CUHK-SZ; arXiv 2610.13022, Oct 2026) | 341 repository-level tasks with vague intent + human-validated requirement documents + persona-based user simulators. Shows the RE community is moving to agentic clarification; it has no security dimension — an obvious extension for Proposal B (security requirements elicited through clarification). |
| R3 | **REA-Coder: Requirement Alignment for Code Generation** (Li et al., PKU; arXiv 2604.16198) | Identifies which parts of a requirement the LLM misreads and realigns; +8–30% on five benchmarks. Treats requirement misunderstanding as the root cause — Proposal B's "where do requirements get lost" RQ2 is the security-specific version. |
| R4 | **LLMs for RE: Cross-Task Empirical Evaluation** (Dąbrowski, Mallya, Ferrari, Zadenoori, Yu; arXiv 2608.21531) | Five RE activities incl. traceability identification/explanation; no model wins across tasks. Cite for RE-side baseline and for the traceability RQ3. |
| R5 | **Toward Secure LLM Agents** (Ling, Yu, Chen, Fang; arXiv 2606.10749; 247 studies) | Threat-surface taxonomy (user prompts, web content, tool outputs, retrieved content, files/code, planning loop, memory, inter-agent). "Files/code" and "memory" surfaces are where instruction files and stored preferences live — ties A2 and Proposal A together. |
| R6 | **Agent Skills for LLMs** (Xu & Yan, ZJU; arXiv 2602.12430) | 26.1% of community skills contain vulnerabilities; bundled scripts ≈2.1× odds. SKILL.md/AGENTS.md files are the artefact of Proposal A; this paper provides the security framing and prior numbers. |
| R7 | **Security in LLM-Assisted Coding: SLR** (Yuan et al., ACU; arXiv 2610.15482) | Gaps: contaminated benchmarks, no integrated static+dynamic+repo+human pipeline, agent autonomy under-studied. Good for related-work and for justifying the SCAFFOLD-style pipeline. |
| R8 | **Specification-Driven Code Generation: Study Design** (Rosa et al., URJC; arXiv 2601.03878) | Registered-report-style controlled experiment (spec → tests → code) — a format Proposal B's empirical half could adopt. |
| R9 | **One Is Not Enough: Multiple Security Patches per CVE** (Zhang et al., Nankai/NTU incl. Yang Liu; ASE 2026) | 20.6% of patched CVEs have multiple patches; relevant to NTU-side supply-chain work and to traceability of fixes to requirements. Yang Liu co-author = SCAFFOLD partner. |

## 1.3 What the additions change in the Part-1 conclusions

1. **The "nobody varies the requirement" gap is narrower than Part 1 stated, but still open.** A2 varies *where* the security requirement sits (prompt vs. memory) and finds a 19.7–33.6 pp effect with a functional-correctness cost. It does not vary specificity, verifiability, provenance or traceability, and it studies single-function prompts with four proprietary chat models. Proposal B must cite A2 as the starting point and move to (i) a specificity ladder, (ii) repository-level agentic tasks (A1, R1), (iii) open-weight models with trace access (P18), (iv) traceability of requirement → code → test (R4).
2. **Benchmarks exist; the independent variable does not.** A1 + R1 + CWEval + SecCodeBench give ~900 tasks across 7 languages. All of them *omit* the security requirement on purpose. Proposal B's cheapest version is to re-run these benchmarks with the requirement added at increasing specificity — no new benchmark construction needed for RQ1.
3. **Clarification is the RE frontier in agentic coding (R2).** A security-requirements clarification study (does the agent *ask* about auth, input validation, secrets?) is a natural RQ to add to Proposal B, and connects to P20 (UVA: asking without leaking).
4. **Proposal A's artefact (AGENTS.md/CLAUDE.md/.cursorrules/SKILL.md) is now security-salient (R6) and sits on two named threat surfaces (R5).** That strengthens the motivation and gives prior numbers to beat.

# 2. Reusing the SRAP / SCAFFOLD application

The SCAFFOLD proposal (Liu Yang, NTU-CYSREN + Wnuk, BTH; co-Is Xie, Zhang / Ma, Fucci) is a four-WP programme on *assurance-by-construction for AI-assisted development of critical software*. Its text is directly reusable because the three paper proposals are, in effect, the first deliverables of WP1 and WP3.

## 2.1 Section-by-section reuse map

| SRAP section | Reusable for | How |
|---|---|---|
| **A) Aims — Aim 1 "Trust foundations"**: "which SE tasks AI may take on, how risk classes should be defined across requirements, coding, testing, review, repair, and what evidence must accompany AI-produced artifacts, so that the trust model is machine-checkable" | Proposal B framing; Proposal A RQ2 | The phrase "machine-checkable" is the L4 rung of the specificity ladder. Reuse verbatim as the motivation: a security requirement that cannot be compiled into a check is not a trust boundary. |
| **Central hypothesis, prediction (i)** "lower post-merge vulnerability density" and **(iv)** "≤1.2× median baseline latency per commit/review/merge" | Proposal B RQ4 metrics | Secure-and-correct@1 + tokens/latency overhead are the paper-sized versions of predictions (i) and (iv). Report both, as SCAFFOLD commits to. |
| **B) Background — three risk surfaces** (generated artifacts; AI-assisted supply chain; LLM/agent toolchain incl. "prompt or instruction integrity failures") | Related-work structure for all three proposals | Map Lo's corpus onto the three surfaces: P03/P18/A1/A2 → artifacts; P01/A3/A4/R9 → supply chain; P16/P19/P20/R5/R6 → toolchain. "Instruction integrity" is the SCAFFOLD name for what Proposal A studies. |
| **WP1 RQ1.1** "Which SE tasks (requirements, coding, testing, review, repair) can be responsibly delegated… what delegation semantics preserve accountability?" | Proposal A RQ1–RQ2 | The instruction-file study answers RQ1.1 empirically: it is the first catalogue of what practitioners *actually* delegate and forbid. Reuse RQ1.1 wording in the paper's introduction and cite the proposal's framing (NIST SSDF / AI RMF / EU AI Act Art. 15). |
| **WP1 RQ1.3** "What evidence forms and approval checkpoints should be required for AI-produced artifacts, expressed as machine-checkable rules instead of organisational guidance?" | Proposal B RQ4 (ReqGuard/SecSpec) | This is literally the requirement-to-check compiler. The OPA/Rego policy-as-code framing from WP1 Methods gives the tool a deployment story (policy bundle evaluated at commit/review/merge). |
| **WP1 Methods**: risk-class taxonomy grounded in NIST SSDF, NIST AI RMF, EU AI Act Art. 15; evidence model composing PROV-DM, in-toto, SLSA | Proposal C (knowledge graph) | The taxonomy + standards mapping is the node/edge schema of the security-requirements KG. Extend with ASVS, CWE/CAPEC, and EU CRA (which the proposal explicitly left out of scope — a paper can add it). |
| **WP2 Methods**: IDE telemetry (LSP interception, Git hooks, agent-trace recording), policy-evaluation middleware at commit/review/merge, grounded-theory coding of developer traces, SESAM/ThreMoLIA infrastructure | Proposal B RQ2 (where requirements get lost); in-the-wild validation | Agent-trace recording is exactly what P18 and P15 do offline; WP2's middleware would let Proposal B's tool run in-stream in a real pipeline, giving the "ecological validation" Lo's papers always add. |
| **WP3 RQ3.1** "How effective are generated-artifact analysis pipelines (static analysis, symbolic execution, LLM-guided fuzzing, mutation-adequacy) when applied to AI-authored code as distinct from hand-written code?" | Proposal B oracle design | Reuse the oracle stack (CodeQL + Semgrep custom rules + property-based tests). SecReason (P18) already showed generic Semgrep registry rules cover 13/20 CWEs at F1 45.5% while corpus-calibrated rules reach 98.9% — RQ3.1 can be answered partly from that. |
| **WP3 RQ3.3** jailbreak / prompt-injection / tool-misuse on SE agent toolchains; Garak/PyRIT/Promptfoo | Proposal A threat framing; future paper | Instruction files are an injection vector (R6). A follow-up "requirements-level prompt injection" paper fits WP3 and Jie Zhang's (A*STAR) red-teaming role. |
| **D) Preliminary work** — Fucci: Policy-Driven SBOM (PROFES 2025), Augmenting SBOMs with Vulnerability Descriptions (FSE 2025), Privacy-by-Design RE for GDPR (IST 2025), Systematic Mapping on RE for Regulatory Compliance (IST 2025); Ma: MazeBreaker (ICSE 2026), CKGFuzzer (ICSE 2025 best paper), iAudit (ICSE 2025) | Author team and related work for all three | The BTH side already has the RE-for-compliance lineage (Fucci) and the LLM-security lineage (Ma). Proposal B is the paper that makes those two lineages meet; cite [9]–[11] and [5]–[7] from the SRAP reference list. |
| **E) Novelty — "from output evaluation to assurance-by-construction"** | Positioning paragraph for Proposal B's tool | Reuse: existing secure-code-generation work (CoSec, SafeEdit, SecReason, benchmarks A1/R1) evaluates or repairs *outputs*; Proposal B's compiler constrains generation by the *requirement* before and during generation. This is the same shift SCAFFOLD argues at programme level. |
| **F) Competitors** list (NIST AI RMF, SSDF, EU AI Act, SLSA, V-SPELLS, vendor guardrails) | Related-work "standards" paragraph | Reuse the one-line characterisations; add OWASP ASVS and OWASP LLM Top-10, which the proposal omits. |
| **G) PhD roles** WP1-S1 (trust models, risk classes), WP1-S2 (delegation policies, approval boundaries, assurance obligations), WP3-S5 (security of AI-generated code/tests) | Who writes the papers | Proposal A = S1/S2 first-year paper; Proposal B = S5 + S2 joint; Proposal C = S1 + S6. If SRAP is funded (award July 2026 per the form), these are year-1 deliverables ("initial risk-class taxonomy", "static-analysis rule packs for AI-generated code"). |
| **H) Milestones Year 1**: "Initial risk-class taxonomy and executable trust policies… aligned with NIST SSDF and EU AI Act Article 15 (WP1)"; "Static-analysis rule packs for AI-generated code (CodeQL, Semgrep); LLM-guided fuzzing harness (WP3)"; "First joint publications" | Proposal A and B are those publications | Nothing new needed: Proposal A *is* the taxonomy milestone; Proposal B's compiler *is* the rule-pack milestone. |
| **Part 4 — collaboration**: Ma–Liu–Xie publication record; "Prof Krzysztof Wnuk anchors WP1 (delegation policies, review obligations) and WP2 (workflow governance, escalation design)" | Authorship/venue strategy | Proposal B's author list should mirror this (Wnuk, Ma, Fucci, Xie, Liu) and, if desired, add SMU's Lo group (Zhensu Sun, Lwin Khin Shar) — Xie is already at SMU, so the bridge exists. |

## 2.2 What the SRAP application does *not* give you (and the papers must add)

- **No measured gap.** The proposal argues from standards and risk; Lo's papers always open with a number. Use A1 (23.8% secure-and-correct), R1 (16–25%), A2 (+2.7–50.3 pp from memory), P18 (hardened prompt ≤66%) as the opening paragraph.
- **No requirement-quality variable.** SCAFFOLD treats policies as given (OPA/Rego). The papers' contribution is to show that the *form* of the requirement determines whether the policy is honoured — which then justifies WP1's machine-checkable design.
- **No benchmark or dataset.** The proposal promises a platform; reviewers at ICSE/FSE expect a dataset. Proposal A's instruction-file corpus and Proposal B's requirement-augmented task set are the datasets.
- **EU CRA is out of scope** in SRAP ("regulatory adaptation beyond NIST SSDF / AI RMF / EU AI Act Article 15 is out of scope"). Proposal C can take it as the European-funding differentiator (Horizon Europe / Vinnova paths named in "Bilateral opportunities").

## 2.3 Concrete reuse recipe (fastest path to a draft)

1. **Introduction** ← SRAP §B paragraphs 1–3 (three risk surfaces) + one sentence per number from A1/R1/A2/P18.
2. **Problem statement** ← SRAP Aim 1 + RQ1.1/RQ1.3 reworded as paper RQs (Part 1 §5B).
3. **Related work** ← SRAP §F standards list + Lo corpus tables (Part 1 §4) + §1.2 above.
4. **Method/oracles** ← SRAP WP3 Methods (CodeQL, Semgrep custom rules, property tests) + P18's in-stream mechanism + P20's replay gate.
5. **Validation** ← SRAP WP2 middleware/telemetry as the in-the-wild setting; SESAM OSS maintainer case studies as subjects.
6. **Threats/ethics** ← SRAP "Staged feasibility and risk handling" + Lo-style dual-use paragraph.
7. **Author list** ← SRAP Part 4 team.

# 3. Updated recommended order

| When | Paper | Primary SRAP WP | Lo-corpus papers to build on |
|---|---|---|---|
| Nov 2026 – Jan 2027 | **A. Security requirements in agent instruction files** (MSR 2027) | WP1 (RQ1.1), WP3 (RQ3.3) | P08 (method), P09 (taxonomy pipeline), R6, R5 |
| Jan – Sep 2027 | **B. Security-requirement fidelity in LLM/agentic coding + compiler** (FSE/ASE 2027) | WP1 (RQ1.3), WP3 (RQ3.1) | A2 (position against), A1/R1 (tasks), P18 (mechanism), P03 (trade-off score), P07 (channel), R2/R3 (RE side) |
| 2027–28 | **C. Security-requirements knowledge graph incl. EU CRA** | WP1 taxonomy, WP3 supply chain | P01 (KGC), A4 (CoSA), A3, R9 |

# 4. Sources

- SecureVibeBench — https://arxiv.org/abs/2509.22097
- Insecure Coding Preferences in Long-Term Memory — https://arxiv.org/pdf/2607.17619
- Revisiting Vulnerability Patch Identification on Data in the Wild — https://arxiv.org/html/2603.17266v1
- CoSA — https://arxiv.org/pdf/2608.13928
- Last Secure Code Benchmark — https://arxiv.org/abs/2610.14766
- Don't Guess, Just Ask (ReqClarifyBench) — https://arxiv.org/abs/2610.13022
- REA-Coder — https://arxiv.org/abs/2604.16198
- LLMs for RE: Cross-Task Evaluation — https://arxiv.org/abs/2608.21531
- Toward Secure LLM Agents — https://arxiv.org/html/2606.10749v1
- Agent Skills for LLMs — https://arxiv.org/html/2602.12430v1
- Security in LLM-Assisted Coding SLR — https://arxiv.org/html/2610.15482v1
- Specification-Driven Code Generation study design — https://arxiv.org/pdf/2601.03878
- One Is Not Enough (ASE 2026) — https://sen-chen.github.io/pdf/C66-ASE2026-One%20Is%20Not%20Enough%20The%20Untold%20Story%20of%20Multiple%20Security%20Patches%20for%20One%20Vulnerability.pdf
- David Lo ISSTA 2026 profile — https://conf.researchr.org/profile/issta-2026/davidlo
- David Lo CV (Feb 2026) — https://computing.smu.edu.sg/sites/scis.smu.edu.sg/files/2026-02/davidlo-CV.pdf
- SRAP/SCAFFOLD application — attached PDF (33 pp.)
