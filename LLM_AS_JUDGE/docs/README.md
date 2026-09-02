# LLM-as-a-Judge Documentation

This folder explains the project one file at a time. It is written for someone
learning LLM-as-a-Judge and Python data validation.

## Start here

The current evaluation flow is:

```text
EvaluationInput + active rubric
              ↓
       JudgePrompt
         ↙       ↘
      Terra      Luna
         ↘       ↙
 validated results
              ↓
 consensus or human review
```

## File-by-file guide

| Project file | What it does | Detailed guide |
|---|---|---|
| `README.md` | Project introduction and quick start | [Root README guide](files/root-readme.md) |
| `pyproject.toml` | Python package and dependency configuration | [pyproject guide](files/pyproject.md) |
| `.env.example` | Azure environment-variable template | [Environment guide](files/environment.md) |
| `.gitignore` | Prevents local secrets and generated files from being committed | [Gitignore guide](files/gitignore.md) |
| `src/llm_judge/__init__.py` | Public package imports | [Package init guide](files/package-init.md) |
| `src/llm_judge/contracts.py` | Input/output formats and evaluation policy | [Contracts guide](files/contracts.md) |
| `src/llm_judge/rubric.py` | Rules for assigning scores | [Rubric guide](files/rubric.md) |
| `src/llm_judge/dataset.py` | Loads and validates labelled cases | [Dataset module guide](files/dataset-module.md) |
| `src/llm_judge/prompt_builder.py` | Builds safe, mode-specific judge prompts | [Prompt builder guide](files/prompt-builder.md) |
| `src/llm_judge/settings.py` | Validates Azure configuration and protects secrets | [Settings guide](files/settings.md) |
| `src/llm_judge/azure_client.py` | Sends prompts and captures raw Azure responses | [Azure client guide](files/azure-client.md) |
| `src/llm_judge/response_parser.py` | Validates raw responses into trusted Pydantic results | [Response parser guide](files/response-parser.md) |
| `src/llm_judge/multi_judge.py` | Runs Terra and Luna and combines their judgments | [Multi-judge guide](files/multi-judge.md) |
| `src/llm_judge/dataset_runner.py` | Runs both judges across a labelled dataset | [Dataset runner guide](files/dataset-runner.md) |
| `datasets/evaluation_cases.example.jsonl` | Draft cases awaiting human review | [Example dataset guide](files/example-dataset.md) |
| `datasets/evaluation_cases.example.json` | Pretty human-readable copy of draft cases | [Example dataset guide](files/example-dataset.md) |
| `tests/test_contracts.py` | Tests contract behavior and validation | [Contract tests guide](files/test-contracts.md) |
| `tests/test_rubric.py` | Tests rubric completeness and validation | [Rubric tests guide](files/test-rubric.md) |
| `tests/test_dataset.py` | Tests dataset loading and readiness checks | [Dataset tests guide](files/test-dataset.md) |
| `tests/test_prompt_builder.py` | Tests prompt content and schemas | [Prompt builder tests guide](files/test-prompt-builder.md) |
| `tests/test_settings.py` | Tests environment configuration | [Settings tests guide](files/test-settings.md) |
| `tests/test_azure_client.py` | Tests Azure requests using a fake transport | [Azure client tests guide](files/test-azure-client.md) |
| `tests/test_response_parser.py` | Tests response parsing for all evaluation modes | [Response parser tests guide](files/test-response-parser.md) |
| `tests/test_multi_judge.py` | Tests Terra/Luna aggregation without network calls | [Multi-judge tests guide](files/test-multi-judge.md) |
| `tests/test_dataset_runner.py` | Tests safe batch execution and JSONL output | [Dataset runner tests guide](files/test-dataset-runner.md) |

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

Run the draft example dataset against both Azure models (24 paid requests):

```bash
set -a
source .env
set +a
.venv/bin/llm-judge-run --dataset datasets/evaluation_cases.example.jsonl \
  --output results/evaluation_results.jsonl --allow-drafts
```

## How to keep these documents current

When a source file changes, update its matching guide in `docs/files/`. Describe
why the behavior changed, not only the new class or field name.
