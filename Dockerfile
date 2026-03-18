FROM python:3.13-slim

RUN apt-get update && apt-get install -y pipx
RUN pipx ensurepath
RUN pipx install poetry

WORKDIR /app

COPY pyproject.toml ./
RUN pipx run poetry install --no-root

COPY todo todo

CMD ["bash", "-c", "sleep 10 && pipx run poetry run flask --app todo run --host 0.0.0.0 --port 6400"]
