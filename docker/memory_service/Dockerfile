FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn pydantic

# Copy application code
COPY app.py /app/app.py
COPY pmm_memory.py /app/pmm_memory.py

# Create data directory
RUN mkdir -p /data

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["python", "/app/app.py"]
