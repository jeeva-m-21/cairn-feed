FROM python:3.13-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

WORKDIR /app

RUN addgroup --system cairn && adduser --system --ingroup cairn cairn

COPY pyproject.toml ./
COPY src ./src

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir .

USER cairn
EXPOSE 8000

CMD ["uvicorn", "cairn_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
