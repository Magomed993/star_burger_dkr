FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN apt update && apt-get install -y build-essential libpq-dev python3-dev && python3 -m venv venv && pip install -r requirements.txt --no-cache-dir
