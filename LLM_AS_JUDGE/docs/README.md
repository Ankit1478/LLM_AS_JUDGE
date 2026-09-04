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
| `src/llm_judge/reliability.py` | Calculates human alignment and reliability metrics | [Reliability guide](files/reliability.md) |
| `src/llm_judge/stability.py` | Measures repeat consistency and A/B position sensitivity | [Stability guide](files/stability.md) |
| `src/llm_judge/error_analysis.py` | Classifies errors and calculates confidence intervals | [Error analysis guide](files/error-analysis.md) |
| `src/llm_judge/production_gate.py` | Converts reliability evidence into a release decision | [Production gate guide](files/production-gate.md) |
| `src/llm_judge/guardrails.py` | Detects common judge-manipulation signals | [Guardrails guide](files/guardrails.md) |
| `src/llm_judge/adversarial.py` | Runs and reports the Step 14 red-team suite | [Adversarial runner guide](files/adversarial.md) |
| `src/llm_judge/calibration.py` | Splits data and compares calibrated judge versions | [Calibration guide](files/calibration.md) |
| `config/production_thresholds.example.json` | Editable Step 12 threshold policy | [Production gate guide](files/production-gate.md) |
| `datasets/adversarial_cases.example.jsonl` | Machine-friendly draft attack suite | [Adversarial dataset guide](files/adversarial-dataset.md) |
| `datasets/adversarial_cases.example.json` | Human-readable draft attack suite | [Adversarial dataset guide](files/adversarial-dataset.md) |
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
| `tests/test_reliability.py` | Tests Kappa, correlation, rates, and warnings | [Reliability tests guide](files/test-reliability.md) |
| `tests/test_stability.py` | Tests repeated and swapped-order evaluation | [Stability tests guide](files/test-stability.md) |
| `tests/test_error_analysis.py` | Tests confusion matrices, error rates, and bootstrap intervals | [Error analysis tests guide](files/test-error-analysis.md) |
| `tests/test_production_gate.py` | Tests passing, failing, and missing-evidence gates | [Production gate tests guide](files/test-production-gate.md) |
| `tests/test_adversarial.py` | Tests detection, red-team execution, and safe failures | [Adversarial tests guide](files/test-adversarial.md) |
| `tests/test_calibration.py` | Tests split isolation, comparison, and held-out verification | [Calibration tests guide](files/test-calibration.md) |

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

Calculate metrics from those saved results without making more Azure requests:

```bash
.venv/bin/llm-judge-metrics --input results/evaluation_results.jsonl \
  --output results/reliability_report.json
```

Estimate Step 10 cost without calling Azure:

```bash
.venv/bin/llm-judge-stability \
  --dataset datasets/evaluation_cases.example.jsonl \
  --output results/stability_results.jsonl --repeats 3 --dry-run
```

Analyze Step 8 errors and statistical uncertainty without calling Azure:

```bash
.venv/bin/llm-judge-error-analysis \
  --input results/evaluation_results.jsonl \
  --output results/error_analysis_report.json
```

Make the final local Step 12 release decision:

```bash
.venv/bin/llm-judge-production-gate \
  --runner-results results/evaluation_results.jsonl \
  --stability-results results/stability_results.jsonl \
  --output results/production_gate_report.json
```

Estimate Step 14 attack-suite calls without contacting Azure:

```bash
.venv/bin/llm-judge-adversarial \
  --dataset datasets/adversarial_cases.example.jsonl \
  --output results/adversarial_results.jsonl --dry-run
```

Create the Step 16 calibration and held-out partitions:

```bash
.venv/bin/llm-judge-calibration split \
  --dataset datasets/evaluation_cases.example.jsonl \
  --calibration-output datasets/calibration.example.jsonl \
  --heldout-output datasets/heldout.example.jsonl \
  --manifest-output datasets/calibration_split.example.json --allow-drafts
```

## How to keep these documents current

When a source file changes, update its matching guide in `docs/files/`. Describe
why the behavior changed, not only the new class or field name.
