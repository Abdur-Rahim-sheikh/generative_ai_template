FROM python:3.12.12-alpine3.23



COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --group test --locked

COPY . ./

EXPOSE 8000

CMD ["sh", "-c", "uv run alembic upgrade head && uv run fastapi dev --host 0.0.0.0"]