FROM python:3.10-slim

COPY --from=ghcr.io/astral-sh/uv:0.10.9 /uv /uvx /bin/
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

COPY . .
RUN chmod +x ./entrypoint.sh

CMD ["./entrypoint.sh"]