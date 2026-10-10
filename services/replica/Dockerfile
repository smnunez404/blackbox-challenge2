FROM python:3.13-slim

WORKDIR /app
RUN useradd --create-home --shell /usr/sbin/nologin replica
COPY domain.py http_server.py ./

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOST=0.0.0.0

USER replica
CMD ["python", "http_server.py"]
