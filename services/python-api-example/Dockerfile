FROM python:3.11-slim

WORKDIR /app

# Copy shared database module
COPY --from=shared /app/shared /app/shared

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 3000

# Run the application
CMD ["python", "app.py"]
