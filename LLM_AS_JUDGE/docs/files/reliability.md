# File Guide: `src/llm_judge/reliability.py`

Actual file: [`src/llm_judge/reliability.py`](../../src/llm_judge/reliability.py)

## Purpose

This module reads Step 8 JSONL results and measures how trustworthy the judges
are:

```text
Dataset runner JSONL
        ↓
validated CaseRunResult objects
        ↓
human agreement + Cohen's Kappa + score correlation
        ↓
ReliabilityReport JSON
```

## Metrics

- Terra versus human exact agreement and Cohen's Kappa
- Luna versus human exact agreement and Cohen's Kappa
- Combined result versus human agreement, including abstention count
- Terra versus Luna agreement and disagreement rate
- Failure rate and human-review rate
- Pearson score correlation for Terra, Luna, and averaged scores
- The agreement metrics segmented by binary, pairwise, and score mode

## Interpretation safeguards

- An aggregate 1–1 model split is counted as an abstention, not a wrong answer.
- Kappa returns `null` when chance correction is mathematically undefined.
- Correlation returns `null` for too few observations or constant scores.
- Draft labels and fewer than 30 completed cases produce explicit warnings.
- Overall and per-mode metrics are both reported to prevent one mode from hiding
  weak performance in another.
- Metrics do not automatically approve production; reliability thresholds and a
  deployment gate are a later step.

## Run it

After creating the Step 8 result file:

```bash
.venv/bin/llm-judge-metrics \
  --input results/evaluation_results.jsonl \
  --output results/reliability_report.json
```

This command is local and makes no Azure requests. Add `--overwrite` only when
you intentionally want to replace an existing report.
