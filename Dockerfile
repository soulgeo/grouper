FROM node:22-bookworm-slim AS asset-builder

WORKDIR /app

COPY src/package*.json ./
RUN npm install 

COPY src/tailwind.config.js ./
COPY src/static/ ./static/
COPY src/templates/ ./templates/
COPY src/chat/templates/ ./chat/templates/
COPY src/core/templates/ ./core/templates/
COPY src/notifications/templates/ ./notifications/templates/
COPY src/users/templates/ ./users/templates/

RUN npm run build 

FROM python:3.13.9-slim-bookworm

ENV PYTHONWRITEBUTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* 

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY pyproject.toml uv.lock ./
ENV UV_PROJECT_ENVIRONMENT="/opt/venv"
RUN uv sync --frozen --no-install-project 

COPY src/ .

COPY --from=asset-builder /app/static/src/htmx.min.js ./static/src/htmx.min.js
COPY --from=asset-builder /app/static/src/ws.js ./static/src/ws.js
COPY --from=asset-builder /app/static/css/output.css ./static/css/output.css

ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 8000

CMD ["./entrypoint.sh"]
