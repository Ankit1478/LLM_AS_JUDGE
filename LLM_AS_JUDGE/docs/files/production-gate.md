# File Guide: `src/llm_judge/production_gate.py`

Actual file: [`src/llm_judge/production_gate.py`](../../src/llm_judge/production_gate.py)

## Purpose

Step 12 reads the measurements created in earlier steps and gives one final
answer: `PASSED` or `FAILED`. It does not ask Terra or Luna to judge anything and
does not make Azure calls.

```text
Step 8 results ──→ Step 9 reliability ─┐
        │                              │
        └────────→ Step 11 errors ─────┼──→ Step 12 gate ──→ PASSED / FAILED
Step 10 stability results ─────────────┘
```

## What the default policy checks

- Step 8 and Step 10 contain the same case IDs.
- No dataset label is still marked `draft`.
- At least 100 cases completed.
- Step 8 failure rate is at most 1%.
- Human-review rate is at most 20%.
- Terra/Luna disagreement is at most 10%.
- Aggregate Cohen's Kappa is at least 0.80.
- PASS/FAIL accuracy's 95% lower bound is at least 90%.
- False-pass rate's 95% upper bound is at most 5%.
- False-fail rate's 95% upper bound is at most 10%.
- Pairwise accuracy's 95% lower bound is at least 90%.
- Aggregate score correlation is at least 0.80.
- Terra and Luna mean repeat consistency are each at least 95%.
- Terra and Luna position-flip rates are each at most 5%.
- Terra and Luna stability-call failure rates are each at most 1%.

Every check records its source, observed value, comparison, threshold, pass/fail
status, and plain-language explanation. Missing required evidence is a failure.

## Why confidence bounds are checked

Suppose measured accuracy is 92%, but its 95% confidence interval is 80%–99%.
The gate checks the conservative lower value, 80%, against the 90% requirement.
It fails because the dataset has not shown enough evidence that true accuracy is
at least 90%.

For harmful error rates, the direction reverses. If false-pass rate is 3% with an
interval of 0%–9%, the gate checks the conservative upper value, 9%, against the
5% maximum and fails.

## Threshold policy

The built-in values are learning-oriented starting points, not universal safety
standards. The editable example is
[`config/production_thresholds.example.json`](../../config/production_thresholds.example.json).
Domain owners should set thresholds according to business harm, legal needs, and
human escalation capacity, then version and review the policy.

## Run it

```bash
.venv/bin/llm-judge-production-gate \
  --runner-results results/evaluation_results.jsonl \
  --stability-results results/stability_results.jsonl \
  --thresholds config/production_thresholds.example.json \
  --output results/production_gate_report.json
```

The command prints the complete JSON report and optionally saves it. Use
`--overwrite` only when intentionally replacing an older decision.

## Important limitation

A pass applies only to the exact tested model deployments, prompt, rubric, and
data distribution. Re-run Steps 8–12 after any of them changes. A gate cannot
prove that unrepresented production scenarios are safe.
