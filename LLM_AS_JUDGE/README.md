# LLM-as-a-Judge Learning Project

This project builds a production-oriented LLM judge one small step at a time.

For beginner-friendly, file-by-file explanations, start with
[`docs/README.md`](docs/README.md).

## Step 1: evaluation contract

The judge can score one answer, make a binary decision, or compare two blinded
answers with an explicit tie option. Each case declares whether reference evidence
is required, optional, or intentionally unavailable. Pairwise comparison is the
preferred mode, while pointwise scoring remains available for diagnostics.

Step 1 also defines the human evaluation procedure, task-complexity categories,
required example types, position-swap policy, and reliability metrics. Reliability
thresholds are configured only after measuring a human-labelled baseline rather
than assuming a universal target.

Pointwise mode scores correctness, relevance, completeness, and clarity from 1 to
5. The application calculates the final `PASS` or `FAIL` decision.

An answer passes when:

- its weighted score is at least `3.5`;
- correctness is at least `3`; and
- relevance is at least `3`.

The judge must not use model identity, response length alone, personal style
preferences, cost, or latency in its decision.

Run the Step 1 tests:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Azure integration and the judge prompt intentionally belong to later steps.

## Step 2: scoring rubric

`RUBRIC_V1` defines concrete score anchors from 1 to 5 for correctness,
relevance, completeness, and clarity. It also records critical-failure rules and
instructions that prevent length, confidence, formatting, or model identity from
influencing scores by themselves.

The rubric is versioned as `1.0.0`. Future changes must create a new version so
stored evaluation results can always be traced to the exact rules used.
