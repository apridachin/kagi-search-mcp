# Use the official Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS uv

# Set working directory
WORKDIR /app

# Copy necessary files for installation
COPY pyproject.toml uv.lock README.md /app/

# Install the project's dependencies using uv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev --no-editable

# Copy the project source code
COPY src/ /app/src/

# Install the project itself
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-editable

# Final stage
FROM python:3.12-slim-bookworm

WORKDIR /app

# COPY --from=uv /root/.local /root/.local
COPY --from=uv --chown=app:app /app/.venv /app/.venv

# Set PATH and PYTHONPATH
ENV PATH="/app/.venv/bin:$PATH" \
    KAGI_API_KEY=YOUR_API_KEY_HERE

# Command to run the server
ENTRYPOINT ["/app/.venv/bin/kagi-mcp"]