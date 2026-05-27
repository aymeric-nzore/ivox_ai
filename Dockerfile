FROM ghcr.io/astral-sh/uv:latest AS uv

FROM python:3.11-slim

WORKDIR /app

COPY --from=uv /uv /bin/uv

COPY pyproject.toml ./pyproject.toml
COPY uv.lock ./uv.lock

RUN uv sync --frozen --no-dev

# Copier uniquement le code utile au runtime
COPY api ./api
COPY core ./core
COPY memory ./memory

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]