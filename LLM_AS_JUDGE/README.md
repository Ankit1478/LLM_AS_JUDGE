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

## Step 9: reliability metrics

`reliability.py` measures Terra-versus-human, Luna-versus-human, combined-versus-
human, and Terra-versus-Luna agreement. It calculates Cohen's Kappa, Pearson score
correlation, failures, abstentions, disagreements, and human-review rates. Results
are also segmented by evaluation mode, and draft or small-sample runs receive
clear interpretation warnings.

```bash
.venv/bin/llm-judge-metrics \
  --input results/evaluation_results.jsonl \
  --output results/reliability_report.json
```

Metric calculation is local and does not spend Azure tokens. It does not yet make
a production approval decision because reliability thresholds are not configured.

## Step 10: repeat consistency and position bias

`stability.py` repeats the same unchanged prompt for Terra and Luna, calculates
decision consistency, and reports score mean, median, standard deviation, and
range. Pairwise cases are also repeated after swapping A and B. Swapped winners
are mapped back to the original identities before calculating position-flip rate,
first/second-position preference, and tie consistency.

First estimate the request count without contacting Azure:

```bash
.venv/bin/llm-judge-stability \
  --dataset datasets/evaluation_cases.example.jsonl \
  --output results/stability_results.jsonl \
  --repeats 3 --dry-run
```

The included 12-case dataset requires 108 Azure calls for three repeats across
Terra, Luna, and both orders of its pairwise cases. The actual learning run needs
`--allow-drafts`; production mode requires human-reviewed data. The CLI also has
a paid-call safety limit controlled by `--max-calls`.

## Step 11: error analysis and statistical confidence

`error_analysis.py` explains *how* each judge is wrong, not only how often it
agrees with humans. For Terra, Luna, and their combined decision it calculates:

- PASS/FAIL confusion matrices;
- accuracy, precision, recall, and F1;
- false-pass rate and the exact false-pass case IDs;
- false-fail rate and the exact false-fail case IDs;
- pairwise `A_WINS`, `B_WINS`, and `TIE` confusion and per-label metrics; and
- percentile-bootstrap confidence intervals with explicit denominators.

Run it on the Step 8 result file:

```bash
.venv/bin/llm-judge-error-analysis \
  --input results/evaluation_results.jsonl \
  --output results/error_analysis_report.json
```

This command is entirely local and makes no Azure calls. The default is 2,000
bootstrap samples with a 95% confidence level and deterministic seed 42. A wide
interval means the dataset is too small or variable for a precise estimate.
Confidence intervals measure sampling uncertainty; they do not independently
prove that a judge is safe for production.

## Step 12: production release gate

`production_gate.py` reads the saved Step 8 and Step 10 JSONL files, rebuilds the
Step 9–11 measurements locally, and returns `PASSED` only when every required
check succeeds. It checks human review status, sample size, failures, disagreement,
Cohen's Kappa, conservative accuracy and error-rate confidence bounds, score
correlation, repeat consistency, and position-flip rate.

```bash
.venv/bin/llm-judge-production-gate \
  --runner-results results/evaluation_results.jsonl \
  --stability-results results/stability_results.jsonl \
  --output results/production_gate_report.json
```

The gate fails safely when a required measurement is missing. The starting policy
is shown in `config/production_thresholds.example.json`. These defaults are for
learning; production owners must approve thresholds based on the harm caused by
false passes and false fails. Supply a reviewed policy with
`--thresholds config/production_thresholds.example.json`.

## Step 13: skipped

Continuous production monitoring and drift detection are intentionally deferred.

## Step 14: adversarial and prompt-injection testing

`guardrails.py` detects common manipulation signals without changing or silently
blocking candidate text. `adversarial.py` runs human-labelled attacks through
Terra and Luna and marks each case as `resisted`, `compromised`, or `error`.
Detection alone is not considered proof; resistance means both judges still made
the expected human-approved decision.

The included eight draft cases cover instruction override, fake system roles,
forced decisions, JSON/schema hijacking, prompt extraction, encoded commands,
model-identity influence, and verbosity distraction. Estimate cost without Azure:

```bash
.venv/bin/llm-judge-adversarial \
  --dataset datasets/adversarial_cases.example.jsonl \
  --output results/adversarial_results.jsonl \
  --dry-run
```

The dry run reports 16 planned calls: eight cases times two models. Run the actual
learning suite by removing `--dry-run` and adding `--allow-drafts`. For production,
humans must review the cases and labels first, then `--allow-drafts` must be omitted.

## Step 15: skipped

Connecting the optional adversarial suite to the production gate is intentionally
deferred.

## Step 16: calibration and held-out testing

`calibration.py` creates a deterministic split stratified by evaluation mode:
one reusable calibration partition and one protected held-out partition. A SHA-256
manifest records the exact case IDs and dataset fingerprints.

Create the split for the included draft learning dataset:

```bash
.venv/bin/llm-judge-calibration split \
  --dataset datasets/evaluation_cases.example.jsonl \
  --calibration-output datasets/calibration.example.jsonl \
  --heldout-output datasets/heldout.example.jsonl \
  --manifest-output datasets/calibration_split.example.json \
  --allow-drafts
```

Run Step 8 on the calibration file before and after a developer-approved prompt,
rubric, example, or threshold change. Then compare the two saved result files:

```bash
.venv/bin/llm-judge-calibration compare \
  --baseline-results results/calibration_baseline.jsonl \
  --candidate-results results/calibration_candidate.jsonl \
  --manifest datasets/calibration_split.example.json \
  --baseline-version rubric-v2 \
  --candidate-version rubric-v3 \
  --change-summary "Do not penalize short answers only for being short" \
  --reviewed-by developer-name \
  --output results/calibration_comparison.json
```

The comparison shows improved, unchanged, regressed, fixed-error, and new-error
cases. It rejects changed human labels or unexpected case IDs. Only after a change
is accepted should its configuration be locked and run once on the held-out file:

```bash
.venv/bin/llm-judge-calibration verify \
  --results results/heldout_locked.jsonl \
  --manifest datasets/calibration_split.example.json \
  --comparison results/calibration_comparison.json \
  --configuration-version rubric-v3 \
  --output results/heldout_verification.json
```

Splitting, comparing, and verifying are local. The Azure calls occur only when
the existing Step 8 runner is explicitly used to generate the result files.

Create the local environment and install dependencies:

```bash
python3 -m venv .venv
.venv/bin/pip install .
```

Configure your own Azure values using `.env.example` as a guide. The project does
not load `.env` automatically; export variables through your shell, deployment
platform, or secret manager. Structured-output request design follows the
[official OpenAI documentation](https://platform.openai.com/docs/guides/structured-outputs).
