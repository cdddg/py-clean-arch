FROM python:3.11-slim-bookworm
LABEL project=py-clean-arch

COPY ./pyproject.toml ./uv.lock /
RUN pip install --upgrade pip \
    && pip install --root-user-action=ignore uv \
    && uv sync --all-groups --frozen

COPY ./src /app/
EXPOSE 8000

CMD ["sh", "-c", "uvicorn main:app --app-dir ./app  --host 0.0.0.0 --port 8000"]
