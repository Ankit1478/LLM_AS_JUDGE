# File Guide: `src/llm_judge/calibration.py`

Actual file: [`src/llm_judge/calibration.py`](../../src/llm_judge/calibration.py)

## Purpose

Step 16 lets developers improve the judge repeatedly without accidentally tuning
it to the final test cases.

```text
Human-labelled dataset
       │
       ├── calibration cases → baseline → developer change → candidate → compare
       │                                                        │
       │                                                 accept or reject
       │                                                        │
       └── protected held-out cases ───────────────────── locked version only
```

The module never rewrites prompts or human labels. A developer owns the change,
provides a summary, and must add their reviewer name before a non-regressing
candidate can move to held-out testing.

## Split

`split_evaluation_dataset` assigns cases deterministically using a seed and
stratifies by binary, score, and pairwise mode. It attempts to preserve both
partitions for every mode that has at least two cases.

The manifest stores exact case IDs, requested fraction, mode counts, and SHA-256
fingerprints for the source and both partitions. The same dataset and seed always
produce the same split.

## Compare

`compare_calibration_runs` requires baseline and candidate result files to contain
exactly the calibration IDs. It also rejects changes to human decisions, scores,
modes, or review status.

It compares:

- aggregate human agreement and Cohen's Kappa;
- PASS/FAIL accuracy, false-pass rate, and false-fail rate;
- human-review and evaluation-failure rates;
- pairwise accuracy; and
- aggregate score correlation.

The report shows the numeric before/after delta and lists fixed and newly created
false passes, false fails, and pairwise mismatches. A regression beyond the
documented tolerance rejects the candidate. With no regression but no named
reviewer, the result remains `needs_developer_review`.

## Verify

`verify_heldout_run` requires the saved accepted comparison, its matching candidate
configuration version, and the exact protected held-out IDs. It calculates the
final Step 9 and Step 11 reports for the locked configuration. Do not use
held-out errors to make another change; doing so turns them into calibration data
and requires a new untouched test partition.

## Commands

The complete commands are documented in the root
[`README.md`](../../README.md#step-16-calibration-and-held-out-testing).

The split, comparison, and verification commands are local. Only Step 8 calls
Azure when generating baseline, candidate, or held-out results.

## Statistical caution

Fewer than 30 cases produces an explicit warning. A change on a calibration set
is not final evidence, and several compared metrics increase the chance of finding
an apparent improvement by chance. Practical risk—especially false passes—must
remain more important than a small headline accuracy increase.
