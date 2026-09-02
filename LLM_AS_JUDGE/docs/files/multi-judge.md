# File Guide: `src/llm_judge/multi_judge.py`

Actual file: [`src/llm_judge/multi_judge.py`](../../src/llm_judge/multi_judge.py)

## Purpose

This module evaluates the same case with two independent judges:

```text
                         ┌→ gpt-5.6-terra → validated result ┐
EvaluationInput → prompt ┤                                   ├→ combined result
                         └→ gpt-5.6-luna  → validated result ┘
```

`TwoModelJudge.from_settings()` uses the same Azure endpoint, API key, and API
version while selecting Terra and Luna separately.

## Combining decisions

- For binary and pairwise modes, both models must agree to produce a consensus.
- A 1–1 disagreement has no majority and is sent for human review.
- For score mode, each rubric dimension is averaged and Python calculates the
  weighted score and aggregate decision.
- Score-mode decision disagreement is still flagged for human review.
- Both original judgments are retained for auditing and later metrics.
