FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HOME=/tmp

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .
RUN mkdir -p /app/data /app/dokumen /app/staticfiles \
    && addgroup --system django \
    && adduser --system --ingroup django django \
    && chown -R django:django /app

USER django
EXPOSE 8000

ENTRYPOINT ["python", "docker/entrypoint.py"]
CMD ["gunicorn", "arsip.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "1", "--threads", "2", "--timeout", "120"]
