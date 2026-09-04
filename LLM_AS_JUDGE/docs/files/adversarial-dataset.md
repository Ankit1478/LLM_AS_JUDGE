# File Guide: Step 14 adversarial datasets

Machine file: [`datasets/adversarial_cases.example.jsonl`](../../datasets/adversarial_cases.example.jsonl)

Readable file: [`datasets/adversarial_cases.example.json`](../../datasets/adversarial_cases.example.json)

## Purpose

These files contain the same eight draft attacks. JSONL is used by the runner;
the indented JSON array is easier for humans to review.

Each case includes normal evaluation fields, a human expected decision, attack
category and location, a description, expected safe behavior, and whether the
lightweight detector should recognize it.

## Before production

Humans must verify the factual reference, expected decision, attack category, and
safe behavior. Then set `review_status` to `human_reviewed`, set `reviewer_count`
to at least 1, and record meaningful review notes. Add domain-specific attacks
from real production incidents; the eight examples are not complete coverage.
