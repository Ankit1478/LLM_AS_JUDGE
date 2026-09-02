# LLM-as-a-Judge Learning Project

This project builds a production-oriented LLM judge one small step at a time.

For beginner-friendly, file-by-file explanations, start with
[`docs/README.md`](docs/README.md).

## Step 1: evaluation contract

The judge can score one answer, make a binary decision, or compare two blinded
answers with an explicit tie option. Each case declares whether reference evidence
is required, optional, or intentionally unavailable. Pairwise comparison is the
preferred mode, while pointwise scoring remains available for diagnostics.

Step 1 also defines the human evaluation procedure, task-complexity categories,
required example types, position-swap policy, and reliability metrics. Reliability
thresholds are configured only after measuring a human-labelled baseline rather
than assuming a universal target.

Pointwise mode scores correctness, relevance, completeness, and clarity from 1 to
5. The application calculates the final `PASS` or `FAIL` decision.

An answer passes when:

- its weighted score is at least `3.5`;
- correctness is at least `3`; and
- relevance is at least `3`.

The judge must not use model identity, response length alone, personal style
preferences, cost, or latency in its decision.

Run the Step 1 tests:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Azure integration and the judge prompt intentionally belong to later steps.

## Step 2: scoring rubric

`RUBRIC_V1` preserves the original reference-based pointwise rubric. `RUBRIC_V2`
is the active rubric and extends the same 1–5 score anchors with:

- score, binary, and pairwise mode instructions;
- required, optional, and reference-free guidance;
- precise `A_WINS`, `B_WINS`, and `TIE` meanings;
- explicit position, identity, length, confidence, formatting, style, and
  concreteness bias controls; and
- six human-labelled examples covering good, bad, borderline, A-wins, B-wins,
  and tie cases.

The old rubric remains available for reproducibility. New evaluations use
`ACTIVE_RUBRIC`, currently version `2.0.0`.

## Step 3: evaluation dataset

`datasets/evaluation_cases.example.jsonl` contains 12 representative draft cases
in machine-friendly JSONL. `datasets/evaluation_cases.example.json` contains the
same cases as an indented JSON array for easy human reading. They cover good, bad,
borderline, A-wins, B-wins, pairwise ties, all evaluation modes, and both
reference-based and reference-free evaluation.

`dataset.py` loads JSONL, validates mode-specific human labels, rejects duplicate
IDs, checks minimum category coverage, and blocks draft cases from production.
The included labels are examples only; humans must confirm them and change
`review_status` before the file becomes trusted gold data.

Inspect the example dataset:

```bash
PYTHONPATH=src python3 -c \
  'from llm_judge import load_jsonl; print(load_jsonl("datasets/evaluation_cases.example.jsonl").kind_counts)'
```

## Step 4: judge prompt builder

`prompt_builder.py` converts a validated `EvaluationInput` and `ACTIVE_RUBRIC`
into provider-neutral system and user messages. It selects instructions and
examples matching the evaluation mode and reference policy, includes the correct
Pydantic response schema, and treats candidate content as untrusted data.

The prompt builder makes no network or Azure call. Its output will be passed to
the model client in the next step.

## Step 5: Azure OpenAI transport

`settings.py` loads the Azure endpoint, secret API key, API version, timeout,
retry count, output-token limit, and optional temperature from environment
variables. The judge uses the `gpt-5.6-terra` deployment by default;
`AZURE_OPENAI_DEPLOYMENT` is an optional override. `.env.example` documents the
names; real secrets must stay outside source control.

`azure_client.py` sends a `JudgePrompt` through the official OpenAI Python SDK's
`AzureOpenAI` client. It requests strict JSON-schema output and returns raw content,
refusals, IDs, finish reason, rubric version, deployment, and token usage. Step 6
will parse the raw content into a validated result.

## Step 6: response validation

`response_parser.py` converts Terra's raw JSON into `BinaryEvaluationResult`,
`PairwiseEvaluationResult`, or `EvaluationResult`, based on the requested mode.
It rejects refusals, malformed JSON, invalid or unexpected fields, and mismatched
case IDs. Only a successfully validated Pydantic result should be stored or used
for reliability metrics.

## Step 7: Terra + Luna judging

`multi_judge.py` sends the same case and prompt to `gpt-5.6-terra` and
`gpt-5.6-luna`, then validates both responses independently. Binary and pairwise
results become final only when both models agree; a 1–1 split is flagged for human
review. Score results include per-criterion averages and an application-computed
weighted decision while preserving both original judgments.

## Step 8: dataset runner

`dataset_runner.py` runs every labelled case through Terra and Luna, validates the
results, compares the aggregate decision with the human answer key, and writes one
JSONL record per case. It continues safely after case-level errors and records
model disagreement, human-review requirements, response metadata, and token use.

Run the included draft dataset for learning (12 cases × 2 models = 24 requests):

```bash
set -a
source .env
set +a

.venv/bin/llm-judge-run \
  --dataset datasets/evaluation_cases.example.jsonl \
  --output results/evaluation_results.jsonl \
  --allow-drafts
```

For production, omit `--allow-drafts`; the runner will reject any dataset that
has not passed the human-review and coverage gates. Use `--overwrite` only when
you intentionally want to replace an existing result file.

Create the local environment and install dependencies:

```bash
python3 -m venv .venv
.venv/bin/pip install .
```

Configure your own Azure values using `.env.example` as a guide. The project does
not load `.env` automatically; export variables through your shell, deployment
platform, or secret manager. Structured-output request design follows the
[official OpenAI documentation](https://platform.openai.com/docs/guides/structured-outputs).
