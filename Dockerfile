FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /code

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

COPY pyproject.toml README.md ./
COPY app ./app

RUN uv sync --no-dev --no-cache

# Preserve the original script entry point and allow docker run arguments.
CMD ["uv", "run", "--no-sync", "python", "app/main.py"]
