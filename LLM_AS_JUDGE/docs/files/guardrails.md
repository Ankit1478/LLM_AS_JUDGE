# File Guide: `src/llm_judge/guardrails.py`

Actual file: [`src/llm_judge/guardrails.py`](../../src/llm_judge/guardrails.py)

## Purpose

This module scans the question, context, reference, and candidate answers for
common attempts to manipulate the judge. It records only the field, category,
and detector name—not the possibly sensitive matched text.

## Categories

- Instruction override such as “ignore previous instructions”
- Fake system or developer roles
- Forced `PASS`, winner, or maximum-score commands
- Attempts to change JSON or schema output
- Requests to reveal prompts or rubric instructions
- Encoded instructions such as Base64
- Claims that a prestigious model produced an answer

The `distraction` category is evaluated by the red-team suite but does not use a
simple keyword detector because ordinary detailed answers should not be flagged
merely for being long.

## Important limitation

A regex match is only a triage signal. It can produce false positives and miss
novel attacks. The code does not automatically reject or modify candidates. The
adversarial runner provides the stronger test: did the judge preserve the correct
human-approved decision despite the attack?
