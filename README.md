# Security Requirements for Coding Agents

What developers write in agent instruction files (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`,
`copilot-instructions.md`, `SKILL.md`, subagents, hooks), how good it is as a requirements
artefact, and whether it relates to repository security outcomes.

Target: **MSR 2027 Registered Report** (Stage 1: abstract 13 Nov 2026, report 20 Nov 2026) ->
Stage 2 in *Empirical Software Engineering* (30 Sep 2027).

## Layout
```
paper/msr2027-rr/     Stage-1 registered report (IEEEtran 10pt). Upload folder to Overleaf.
docs/                 Background analysis, research plan, precedent comparison
data/schema/          Coding/extraction schema (OSS corpus and industrial sample use the same codebook)
scripts/              Mining and analysis scripts (to be added)
```

## Data sources
- OSS corpus: *A Dataset of Agentic AI Coding Tool Configurations* (Galster et al., AIware 2026),
  Zenodo DOI 10.5281/zenodo.19375881, CC BY 4.0. Not committed here; download and place under `data/raw/`.
- Industrial sample: coded sheets only (no file contents), produced with `data/schema/extraction_schema.xlsx`.

## Status
- [x] Corpus analysis and research plan
- [x] Stage-1 draft v0.2
- [ ] Pilot numbers (filter over Zenodo corpus) -> paper Sec. V-C
- [ ] Co-authors fixed; ethics application filed
- [ ] HotCRP abstract (13 Nov) / report (20 Nov)
