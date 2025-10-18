FROM python:3.13 AS builder

WORKDIR /app
COPY requirements.txt ./

RUN pip install --no-cache-dir --target /deps -r requirements.txt jwt uvicorn


FROM python:3.13-slim

WORKDIR /app

ENV PYTHONPATH=/deps

COPY --from=builder /deps /deps

COPY . .


RUN chmod +x ./docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh"]