# Dockerfile for the Study Assistant FastAPI backend.
#
# IMPORTANT LIMITATION (read this before using Docker for this project):
# Ollama is NOT included in this image. Ollama normally runs directly on
# your host machine (or its own container) and is NOT something this
# Dockerfile installs, because:
#   - Ollama needs to download multi-GB model weights, which does not
#     belong inside an application image.
#   - Running an LLM inside the same container as the API mixes concerns
#     and makes the image huge.
#
# So: run Ollama on your HOST machine as usual ("ollama serve"), and when
# running this backend container, point OLLAMA_HOST at your host machine
# instead of "localhost" (which, inside a container, refers to the
# container itself, not your host):
#
#   docker run --rm -p 8000:8000 \
#     -e OLLAMA_HOST=http://host.docker.internal:11434 \
#     -v $(pwd)/data/vector_store:/app/data/vector_store \
#     study-assistant-backend
#
# On Linux, "host.docker.internal" may need --add-host=host.docker.internal:host-gateway.
# If this friction is not worth it for your demo, it's perfectly fine to
# just run the backend directly with uvicorn (see README) -- Docker is a
# nice-to-have here, not a requirement for local Ollama-based projects.

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
