FROM python:3.14-slim AS builder

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


FROM python:3.14-slim

WORKDIR /app

COPY --from=builder /install /usr/local
COPY app/ ./app/

EXPOSE 8000
CMD uvicorn --host 0.0.0.0 app.main:app
