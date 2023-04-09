FROM python:3.10-slim-buster
LABEL project = py-clean-arch

COPY ./pyproject.toml ./poetry.lock /
RUN pip install --upgrade pip
RUN pip install --root-user-action=ignore poetry>=1.4.0
RUN poetry config virtualenvs.create false
RUN poetry install --only main --no-root --no-interaction --no-ansi --no-cache -vv
RUN rm -f pyproject.toml poetry.lock

COPY ./src /app/
EXPOSE 8000

CMD ["sh", "-c", "uvicorn main:app --app-dir ./app  --host 0.0.0.0 --port 8000"]
