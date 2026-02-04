FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY notification-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy common utilities
COPY common /app/common

# Copy application
COPY notification-service .

# Create logs directory
RUN mkdir -p /app/logs

# Expose port
EXPOSE 3004

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:3004/health || exit 1

# Run application
CMD ["uvicorn", "main:socket_app", "--host", "0.0.0.0", "--port", "3004"]
