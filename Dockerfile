FROM python:3.10

COPY --from=ghcr.io/astral-sh/uv:0.10.9 /uv /uvx /bin/
COPY . /app

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN uv sync --locked

CMD ["uv", "run", "promo_service/manage.py", "runserver", "0.0.0.0:8000"]