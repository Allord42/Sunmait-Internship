FROM python:3.12.8-slim-bookworm AS builder

WORKDIR /app

COPY requirements.txt .

# COPY service.py service.py

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

FROM python:3.12.8-slim-bookworm

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

COPY --from=builder /app /app

EXPOSE 8000

# ENTRYPOINT ["python", "-m", "gunicorn", "service:app", "--bind", "0.0.0.0:8000", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker"]
ENTRYPOINT ["python", "service.py"]
