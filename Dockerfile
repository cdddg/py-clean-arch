FROM python:3.8.9
LABEL project = fastapi-pokedex
COPY . .
RUN pip install --upgrade pip \
  && pip install -r requirements.txt --no-cache-dir
