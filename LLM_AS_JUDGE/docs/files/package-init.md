# File Guide: `src/llm_judge/__init__.py`

Actual file: [`src/llm_judge/__init__.py`](../../src/llm_judge/__init__.py)

## Purpose

This file defines the package's public interface. It lets users import important
objects directly from `llm_judge`.

Without the exports:

```python
from llm_judge.contracts import EvaluationInput
```

With the exports:

```python
from llm_judge import EvaluationInput
```

## What `__all__` means

`__all__` lists the names intentionally exposed as public project features. It
also helps readers distinguish supported objects from internal implementation
details.

## When to update it

Add an object here when another module should be able to use it through a simple
`from llm_judge import ...` statement. Do not export every helper automatically.

The current public API includes the evaluation contracts, rubric, dataset loader,
prompt builder, Azure transport, response parser, Terra/Luna judge, and dataset
runner and reliability-report types.
It also exposes the Step 10 stability runner, observations, summaries, and swap
helpers.
Step 11 exports its report models, confusion-matrix types, analysis target enum,
and `calculate_error_analysis` function.
Step 12 exports the versioned thresholds, gate report types, gate evaluator, and
saved-result loaders needed to reproduce the release decision.
