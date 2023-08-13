FROM python:3.10-slim-buster
LABEL project = py-clean-arch

COPY ./pyproject.toml ./poetry.lock /
RUN pip install --upgrade pip \
	&& pip install --root-user-action=ignore "poetry>=1.5.1,<1.6" \
	&& poetry config virtualenvs.create false \
	&& poetry install --only main --no-root --no-interaction --no-ansi --no-cache -vv \
	&& rm -f pyproject.toml poetry.lock

COPY ./src /app/
EXPOSE 8000

CMD ["sh", "-c", "uvicorn main:app --app-dir ./app  --host 0.0.0.0 --port 8000"]
