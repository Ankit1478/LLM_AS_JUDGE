# File Guide: `pyproject.toml`

Actual file: [`pyproject.toml`](../../pyproject.toml)

## Purpose

This file tells Python how the project is packaged and which libraries it needs.
It is similar to `package.json` in a JavaScript project.

## Important sections

### Build system

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"
```

This tells packaging tools to build the project with `setuptools`.

### Project information

```toml
[project]
name = "llm-as-judge-learning"
version = "0.1.0"
requires-python = ">=3.9"
```

This defines the package name, version, and minimum Python version.

### Dependencies

```toml
dependencies = [
    "openai>=1.42,<3",
    "pydantic>=2.9,<3",
]
```

Pydantic validates evaluation inputs, outputs, task settings, and rubric data.
The OpenAI Python SDK provides the `AzureOpenAI` transport used in Step 5.

### Command-line script

```toml
[project.scripts]
llm-judge-run = "llm_judge.dataset_runner:main"
```

Installing the project creates `.venv/bin/llm-judge-run`, which runs a labelled
dataset through Terra and Luna.

It also creates `.venv/bin/llm-judge-metrics`, which calculates a local reliability
report from the runner's JSONL output.

`.venv/bin/llm-judge-stability` runs Step 10 repeated and swapped-order model
experiments.

### Source layout

```toml
[tool.setuptools.packages.find]
where = ["src"]
```

This tells Python that importable code lives under the `src/` directory.

## When to update it

Update this file when adding a runtime dependency, changing supported Python
versions, or preparing a new package release.
