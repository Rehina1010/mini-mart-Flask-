FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN pip install poetry

RUN poetry install --no-root --no-dev

COPY . /app/

CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0"]
