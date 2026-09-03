# File Guide: `src/llm_judge/stability.py`

Actual file: [`src/llm_judge/stability.py`](../../src/llm_judge/stability.py)

## Purpose

This module performs Step 10 with Terra and Luna:

```text
Every case → repeat the unchanged prompt N times → consistency
Pairwise case → repeat original and swapped orders N times → position sensitivity
```

## Repeat consistency

For each case and model, the most common successful decision is counted:

```text
repeat consistency = runs with the most common decision ÷ successful runs
```

For `PASS, PASS, FAIL`, consistency is `2 / 3 = 0.6667`. The report also records
stable, unstable, failed, and insufficient cases. Score-mode runs include mean,
median, population standard deviation, minimum, maximum, and range for every
rubric criterion.

## Position-flip testing

Pairwise cases run in both orders. A swapped `A_WINS` is mapped to original
`B_WINS`, and swapped `B_WINS` is mapped to original `A_WINS`. `TIE` remains
`TIE`. Each original run is compared with the swapped run having the same repeat
number:

```text
position-flip rate = canonical mismatches ÷ successful original/swapped pairs
```

The report also counts first-position preference, second-position preference,
tie consistency, and case IDs requiring investigation.

## Failures and auditability

- Every successful judgment retains model, request, usage, evidence, and result.
- Every failed call is recorded without storing sensitive exception text.
- One failed repeat does not stop later repeats or cases.
- The exact same prompt object is reused for every repeat of an order.
- Results are flushed to JSONL after each case/model combination.
- Draft datasets require the explicit `--allow-drafts` learning flag.

## Cost-safe usage

Check the paid request count without loading credentials or calling Azure:

```bash
.venv/bin/llm-judge-stability \
  --dataset datasets/evaluation_cases.example.jsonl \
  --output results/stability_results.jsonl \
  --repeats 3 \
  --dry-run
```

Run the included draft dataset only after reviewing the estimate:

```bash
set -a
source .env
set +a

.venv/bin/llm-judge-stability \
  --dataset datasets/evaluation_cases.example.jsonl \
  --output results/stability_results.jsonl \
  --repeats 3 \
  --max-calls 108 \
  --allow-drafts
```

For this dataset, three repeats require 108 Azure requests: 72 original-order
requests plus 36 swapped-order pairwise requests. The CLI has a default safety
limit of 200 calls and refuses runs above the limit.
