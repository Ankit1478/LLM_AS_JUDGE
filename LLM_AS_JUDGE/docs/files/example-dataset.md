# File Guide: `datasets/evaluation_cases.example.jsonl`

Actual file: [`datasets/evaluation_cases.example.jsonl`](../../datasets/evaluation_cases.example.jsonl)

Pretty version: [`datasets/evaluation_cases.example.json`](../../datasets/evaluation_cases.example.json)

## Purpose

This file demonstrates the Step 3 dataset format with 12 representative cases.
JSONL means each line is one complete JSON evaluation case.

Two equivalent formats are provided:

- `.jsonl`: Compact, one case per line, used by the Python loader.
- `.json`: Indented JSON array, intended for comfortable human reading and review.

When labels change, keep the two versions synchronized. The `.jsonl` version
remains the executable source used by the current tests.

## Coverage

The file includes two examples of every category:

- Good
- Bad
- Borderline
- Candidate A wins
- Candidate B wins
- Pairwise tie

It also demonstrates score, binary, pairwise, required-reference, and
reference-free cases.

## Important: this is not gold data yet

Every case contains:

```json
"review_status": "draft",
"reviewer_count": 0
```

The expected labels are suggested learning examples. Do not change the status
until a real human reviewer checks the question, reference, candidates, and label.

After review, a case may use:

```json
"review_status": "human_reviewed",
"reviewer_count": 1
```

For a resolved disagreement involving multiple humans:

```json
"review_status": "adjudicated",
"reviewer_count": 2
```

For a real project, copy this structure into a separate `gold_cases.jsonl` and
replace the learning examples with representative cases from the target product.
