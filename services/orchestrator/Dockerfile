FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY orchestrator/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy common utilities
COPY common /app/common

# Copy application
COPY orchestrator .

# Create logs directory
RUN mkdir -p /app/logs

# Expose port
EXPOSE 4000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:4000/health || exit 1

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4000"]
