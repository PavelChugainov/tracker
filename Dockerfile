FROM python:3.13 AS builder

WORKDIR /app
COPY requirements.txt ./

RUN pip install --no-cache-dir --target /deps -r requirements.txt \
    && pip install --no-cache-dir --target /deps uvicorn



FROM python:3.13-slim

WORKDIR /app

ENV PYTHONPATH=/deps

COPY --from=builder /deps /deps

COPY . .

CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]