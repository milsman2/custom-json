# custom-json

A small Python CLI that sends formatted build, deployment, and merge notifications to Slack.

## Requirements

- Python 3.10+
- uv

## Setup

```bash
uv sync
cp .env.example .env
```

Set `SLACK_WEBHOOK` in `.env`. Optional settings are `ENVIRONMENT`,
`DEBUG`, `TESTING`, and `TIMEZONE` (an IANA timezone such as
`America/Chicago`).

## Usage

```bash
uv run custom-json --stage build --author "Jane Doe"
uv run custom-json --stage deployment --author "Jane Doe"
uv run custom-json --stage push --author "Jane Doe"
```

The original option spellings remain supported: `--Stage` and `--Author`.
Existing Docker invocations using `python app/main.py` remain supported.
The legacy `app.settings.config` import path is also retained.

## Development

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy app
uv run pytest --cov
```

Ruff provides import sorting and Black-compatible formatting; Google-style
docstrings are enforced through Ruff's pydocstyle rules.

## Project layout

```text
app/
  custom_json/
    __init__.py
    config.py
    main.py
  settings/                 # legacy import compatibility
    __init__.py
    config.py
  main.py                   # legacy script entry point
tests/
```
