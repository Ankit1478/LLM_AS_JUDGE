# LLM-as-a-Judge Documentation

This folder explains the project one file at a time. It is written for someone
learning LLM-as-a-Judge and Python data validation.

## Start here

The current evaluation flow is:

```text
EvaluationInput (question-paper format)
                  ↓
RUBRIC_V1 (teacher's marking guide)
                  ↓
Future LLM judge call
                  ↓
EvaluationResult (validated result sheet)
```

The model call is intentionally not implemented yet. The project currently defines
and tests the evaluation contract and scoring rubric.

## File-by-file guide

| Project file | What it does | Detailed guide |
|---|---|---|
| `README.md` | Project introduction and quick start | [Root README guide](files/root-readme.md) |
| `pyproject.toml` | Python package and dependency configuration | [pyproject guide](files/pyproject.md) |
| `src/llm_judge/__init__.py` | Public package imports | [Package init guide](files/package-init.md) |
| `src/llm_judge/contracts.py` | Input/output formats and evaluation policy | [Contracts guide](files/contracts.md) |
| `src/llm_judge/rubric.py` | Rules for assigning scores | [Rubric guide](files/rubric.md) |
| `src/llm_judge/dataset.py` | Loads and validates labelled cases | [Dataset module guide](files/dataset-module.md) |
| `src/llm_judge/prompt_builder.py` | Builds safe, mode-specific judge prompts | [Prompt builder guide](files/prompt-builder.md) |
| `datasets/evaluation_cases.example.jsonl` | Draft cases awaiting human review | [Example dataset guide](files/example-dataset.md) |
| `datasets/evaluation_cases.example.json` | Pretty human-readable copy of draft cases | [Example dataset guide](files/example-dataset.md) |
| `tests/test_contracts.py` | Tests contract behavior and validation | [Contract tests guide](files/test-contracts.md) |
| `tests/test_rubric.py` | Tests rubric completeness and validation | [Rubric tests guide](files/test-rubric.md) |
| `tests/test_dataset.py` | Tests dataset loading and readiness checks | [Dataset tests guide](files/test-dataset.md) |
| `tests/test_prompt_builder.py` | Tests prompt content and schemas | [Prompt builder tests guide](files/test-prompt-builder.md) |

## Useful commands

Run all tests from the project root:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Inspect the task configuration:

```bash
PYTHONPATH=src python3 -c \
  'from llm_judge import TASK_DEFINITION; print(TASK_DEFINITION.model_dump_json(indent=2))'
```

## How to keep these documents current

When a source file changes, update its matching guide in `docs/files/`. Describe
why the behavior changed, not only the new class or field name.
