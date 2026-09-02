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

`RUBRIC_V1` preserves the original reference-based pointwise rubric. `RUBRIC_V2`
is the active rubric and extends the same 1–5 score anchors with:

- score, binary, and pairwise mode instructions;
- required, optional, and reference-free guidance;
- precise `A_WINS`, `B_WINS`, and `TIE` meanings;
- explicit position, identity, length, confidence, formatting, style, and
  concreteness bias controls; and
- six human-labelled examples covering good, bad, borderline, A-wins, B-wins,
  and tie cases.

The old rubric remains available for reproducibility. New evaluations use
`ACTIVE_RUBRIC`, currently version `2.0.0`.

## Step 3: evaluation dataset

`datasets/evaluation_cases.example.jsonl` contains 12 representative draft cases
in machine-friendly JSONL. `datasets/evaluation_cases.example.json` contains the
same cases as an indented JSON array for easy human reading. They cover good, bad,
borderline, A-wins, B-wins, pairwise ties, all evaluation modes, and both
reference-based and reference-free evaluation.

`dataset.py` loads JSONL, validates mode-specific human labels, rejects duplicate
IDs, checks minimum category coverage, and blocks draft cases from production.
The included labels are examples only; humans must confirm them and change
`review_status` before the file becomes trusted gold data.

Inspect the example dataset:

```bash
PYTHONPATH=src python3 -c \
  'from llm_judge import load_jsonl; print(load_jsonl("datasets/evaluation_cases.example.jsonl").kind_counts)'
```
