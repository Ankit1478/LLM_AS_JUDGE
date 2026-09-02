# File Guide: `src/llm_judge/dataset_runner.py`

Actual file: [`src/llm_judge/dataset_runner.py`](../../src/llm_judge/dataset_runner.py)

## Purpose

This module connects the full evaluation flow across a dataset:

```text
Human-labelled cases
        ↓
Terra + Luna
        ↓
Validated individual judgments
        ↓
Combined decision compared with human label
        ↓
One auditable JSON object per line
```

## Safety behavior

- Production mode rejects draft or insufficiently reviewed datasets before any
  model request is sent.
- `--allow-drafts` is an explicit learning-only override.
- Human expected labels are used after judging and are never placed in prompts.
- A failure on one case is recorded without stopping later cases.
- Public error records omit exception text that could contain sensitive data.
- Each result is flushed immediately so completed work survives interruption.
- Existing output is protected unless `--overwrite` is supplied.
- Terra and Luna token usage and response metadata are retained.

## Learning run

The included dataset contains draft labels. Load `.env`, then run:

```bash
set -a
source .env
set +a

.venv/bin/llm-judge-run \
  --dataset datasets/evaluation_cases.example.jsonl \
  --output results/evaluation_results.jsonl \
  --allow-drafts
```

This evaluates 12 cases with two models, producing 24 Azure requests.

## Production run

Remove `--allow-drafts`. The runner will proceed only after the dataset passes
the human-review and example-coverage gates.
