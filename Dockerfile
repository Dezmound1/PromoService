FROM python:3.10-slim

COPY --from=ghcr.io/astral-sh/uv:0.10.9 /uv /uvx /bin/
COPY . /app

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN uv sync --locked
RUN chmod +x ./entrypoint.sh

CMD ["./entrypoint.sh"]