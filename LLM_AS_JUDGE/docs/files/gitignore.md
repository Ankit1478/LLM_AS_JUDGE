# File Guide: `.gitignore`

Actual file: [`.gitignore`](../../.gitignore)

## Purpose

This file keeps local secrets, virtual environments, Python caches, test caches,
and generated reports out of source control.

Most importantly, `.env` is ignored so a developer is less likely to commit an
Azure API key accidentally. `.env.example` is not ignored because it contains only
safe placeholder names.

The `results/` and `reports/` directories are ignored because evaluation output
may contain candidate text, model evidence, identifiers, and usage metadata.
