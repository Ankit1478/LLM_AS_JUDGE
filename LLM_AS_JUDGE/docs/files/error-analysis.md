# File Guide: `src/llm_judge/error_analysis.py`

Actual file: [`src/llm_judge/error_analysis.py`](../../src/llm_judge/error_analysis.py)

## Purpose

Step 9 says how often the judges agree. Step 11 shows the kinds of mistakes they
make and how uncertain the measured rates are. It reads saved Step 8 results and
does not call Azure.

## PASS and FAIL confusion matrix

The human label is treated as the answer key. `PASS` is the positive class.

| Name | Meaning |
|---|---|
| True positive | Human says PASS and judge says PASS |
| True negative | Human says FAIL and judge says FAIL |
| False positive / false pass | Human says FAIL but judge says PASS |
| False negative / false fail | Human says PASS but judge says FAIL |

A false pass can let a bad answer through. A false fail can reject a good answer.
The report includes the case IDs for both, so a developer can inspect the actual
examples and improve the rubric, dataset, or prompt.

## Rates and their denominators

- Accuracy asks: out of all evaluated cases, how many were correct?
- Precision asks: out of all predicted PASS cases, how many truly passed?
- Recall asks: out of all human PASS cases, how many did the judge pass?
- F1 balances precision and recall.
- False-pass rate asks: out of all human FAIL cases, how many were incorrectly passed?
- False-fail rate asks: out of all human PASS cases, how many were incorrectly failed?

Every `MetricEstimate` stores its numeric denominator and a plain-language
description. A metric is `null` when its denominator is zero instead of inventing
a misleading value.

## Pairwise evaluation

Pairwise cases have three possible labels: `A_WINS`, `B_WINS`, and `TIE`. The
report creates a 3×3 confusion matrix. Rows are human labels and columns are judge
predictions. It reports precision, recall, and F1 separately for every label,
plus overall accuracy and macro F1.

## Terra, Luna, and aggregate

The same analysis is calculated independently for Terra, Luna, and the combined
decision. When Terra and Luna disagree on a binary or pairwise case, the aggregate
has no decision. Step 11 counts this as an abstention and excludes it from the
aggregate metric denominator.

PASS/FAIL results are reported overall and separately for binary and score modes.
Pairwise results remain separate because their three labels have different
meanings.

## Confidence intervals

The code uses percentile bootstrap sampling:

1. Resample the evaluated cases with replacement.
2. Recalculate the metric on the resampled cases.
3. Repeat this 2,000 times by default.
4. Use the middle 95% of those values as the default interval.

The random seed defaults to 42, so the same inputs and settings reproduce the
same report. Wide intervals mean the estimate is imprecise. Bootstrap intervals
only describe sampling uncertainty; they do not catch bad human labels, missing
production scenarios, data drift, or rubric defects.

## Run it

```bash
.venv/bin/llm-judge-error-analysis \
  --input results/evaluation_results.jsonl \
  --output results/error_analysis_report.json
```

Useful optional arguments are `--bootstrap-iterations`, `--confidence-level`,
`--seed`, and `--overwrite`.

## Production interpretation

Use human-reviewed cases that represent production traffic. Inspect false-pass
and false-fail examples, not only headline accuracy. Draft labels and fewer than
30 completed cases generate warnings. Later production gates should be chosen
from business risk—for example, a safety use case may require a much lower
false-pass rate than a writing-style evaluator.
