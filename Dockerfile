FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
RUN useradd --create-home --uid 10001 appuser
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app ./app
COPY evals ./evals
COPY sample_data ./sample_data
COPY docs ./docs
COPY .env.example ./.env.example
RUN mkdir -p /app/.chroma && chown -R appuser:appuser /app
USER appuser
EXPOSE 8000
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
