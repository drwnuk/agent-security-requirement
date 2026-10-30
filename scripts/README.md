# Scripts

## 01_filter_security_bearing.py  (pilot for RR Sec. V-C)
1. Download the Zenodo record 10.5281/zenodo.19375881 and unpack the CSVs into `data/raw/`
   (context_files.csv, skills.csv, subagents.csv, rules.csv, commands.csv; the .7z archives are not needed).
2. `python3 scripts/01_filter_security_bearing.py data/raw --out results/pilot`
3. Paste `results/pilot/summary.json` numbers into the paper; annotate
   `sample_for_precision.csv` (100 flagged) and `sample_for_recall.csv` (200 non-flagged).

Keyword set = Table II of the report. A file is flagged only if at least one term other than
the bare word "security" matches.

## Planned
- 02_split_units.py, 03_prelabel_llm.py, 04_outcomes/, 05_analysis/ (see docs/04_research_plan.md)
