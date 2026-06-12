# ── Etapa 1: construcción ──────────────────────────────────────────────────
FROM python:3.12-slim AS builder
WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e .

# ── Etapa 2: imagen final de producción ────────────────────────────────────
FROM python:3.12-slim
WORKDIR /app

# Copiar solo los paquetes instalados (no el código fuente de pip ni las herramientas de dev)
COPY --from=builder /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiar el código fuente
COPY src/ ./src/

# Variables de entorno necesarias para Python
ENV PYTHONPATH=/app/src
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8001

# Comando de inicio: uvicorn es el servidor ASGI de FastAPI
CMD ["uvicorn", "profesor.main:app", "--host", "0.0.0.0", "--port", "8001"]
