# File Guide: `src/llm_judge/rubric_approval.py`

Actual file: [`src/llm_judge/rubric_approval.py`](../../src/llm_judge/rubric_approval.py)

## Purpose

Reliability asks whether the judge follows the rubric. This module asks whether
humans approved the rubric itself for the intended product.

```text
Rubric structure valid
        ↓
Human scenario testing passed
        ↓
Domain expert approves meaning
        ↓
Product owner approves intended use
        ↓
Version + fingerprint + dates match
        ↓
Rubric is valid for the production gate
```

## Approval contents

`RubricApproval` records:

- the exact rubric name, semantic version, and SHA-256 fingerprint;
- intended and prohibited uses;
- known limitations;
- a fingerprinted human-validation report and case count;
- named, dated reviewer attestations and decisions;
- approval and expiration dates; and
- decision notes.

The default policy requires at least 30 human-reviewed cases plus separate domain
expert and product owner approvals. A safety-owner role is available when the
application's risk requires it.

## Why the fingerprint matters

The fingerprint covers the complete Pydantic rubric: criteria, weights expressed
through definitions, instructions, score anchors, examples, bias controls, name,
and version. Editing one sentence changes the fingerprint, so an approval for the
old content cannot silently authorize the new content.

## Template safety

[`config/rubric_approval.example.json`](../../config/rubric_approval.example.json)
matches the current rubric identity but is deliberately `draft`. Its evidence
hashes and report location are placeholders, its validation has not passed, and
it contains no reviewer attestations. It cannot pass the production gate.

## Validate an approval

```bash
.venv/bin/llm-judge-rubric-approval \
  --approval config/rubric_approval.json
```

The output lists every control and its explanation. The production-gate command
requires the same approval file through `--rubric-approval`.

## Human responsibility

Code validates evidence and approval metadata; it cannot decide whether a domain
expert performed a thoughtful review. Organizations should protect approval and
evidence files with access controls, code review, and an auditable change process.
