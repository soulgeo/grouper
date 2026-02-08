FROM python:3.13.9-slim-bookworm

ENV PYTHONWRITEBUTECODE=1 \
PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    nodejs \
    npm 

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY pyproject.toml uv.lock ./
ENV UV_PROJECT_ENVIRONMENT="/opt/venv"
RUN uv sync --frozen --no-install-project 

COPY src/ .

ENV PATH="/opt/venv/bin:$PATH"

RUN npm install 
RUN npm run build

EXPOSE 8000

CMD ["./entrypoint.sh"]
