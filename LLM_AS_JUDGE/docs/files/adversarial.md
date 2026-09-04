# File Guide: `src/llm_judge/adversarial.py`

Actual file: [`src/llm_judge/adversarial.py`](../../src/llm_judge/adversarial.py)

## Purpose

This is the Step 14 red-team runner. It sends every attack case through the same
Terra/Luna prompt, parsing, and aggregation pipeline used by normal evaluations.

## Outcomes

- `resisted`: Terra, Luna, and the aggregate all match the human-approved result.
- `compromised`: at least one judge changed to an unsafe or incorrect result.
- `error`: evaluation failed or returned an invalid result.

Disagreement is treated as compromised and sent for human review. Provider error
details and full candidate payloads are not copied into the public result file.

## Report

The report shows overall, Terra, and Luna resistance rates; results by attack
category; detector misses; compromised case IDs; errors; and interpretation
warnings. A small attack suite is useful for learning but cannot prove complete
security.

## Run safely

First estimate the paid call count:

```bash
.venv/bin/llm-judge-adversarial \
  --dataset datasets/adversarial_cases.example.jsonl \
  --output results/adversarial_results.jsonl --dry-run
```

Run the included draft learning cases:

```bash
.venv/bin/llm-judge-adversarial \
  --dataset datasets/adversarial_cases.example.jsonl \
  --output results/adversarial_results.jsonl \
  --allow-drafts --max-calls 16
```

The runner refuses accidental file replacement unless `--overwrite` is supplied.
Production runs reject draft cases.
