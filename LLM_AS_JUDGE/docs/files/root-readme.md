# File Guide: `README.md`

Actual file: [`README.md`](../../README.md)

## Purpose

The root README is the project's front page. It gives a new developer a quick
summary of what has been built and the command needed to run the tests.

## What it contains

- Steps 1–2: evaluation contracts and versioned rubric
- Step 3: human-labelled dataset format
- Steps 4–6: prompt building, Azure transport, and response validation
- Step 7: Terra and Luna aggregation
- Step 8: safe dataset runner and CLI
- Step 9: agreement, Kappa, correlation, and reliability reporting
- Step 10: repeat consistency, score variation, and position-flip testing
- Step 11: confusion matrices, error types, and bootstrap confidence intervals
- Step 12: threshold checks and the final production release decision
- Step 13: monitoring intentionally skipped
- Step 14: prompt-injection detection and adversarial judge testing
- Step 15: adversarial production-gate integration intentionally skipped
- Step 16: calibration comparison and protected held-out testing
- Commands for tests and learning runs

## README versus `docs/`

Use the root README for a quick start. Use this `docs/` folder when you want to
understand each class, decision, or file in more detail.

## When to update it

Update the root README whenever a major learning step becomes usable, such as:

- Adding the prompt builder
- Connecting Azure OpenAI
- Adding a dataset runner
- Adding reliability reports
- Adding error analysis or statistical confidence reports
