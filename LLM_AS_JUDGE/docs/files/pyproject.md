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
dependencies = ["pydantic>=2.9,<3"]
```

Pydantic validates evaluation inputs, outputs, task settings, and rubric data.

### Source layout

```toml
[tool.setuptools.packages.find]
where = ["src"]
```

This tells Python that importable code lives under the `src/` directory.

## When to update it

Update this file when adding a runtime dependency, changing supported Python
versions, or preparing a new package release.

