# Use Python 3.10.9 slim image as base
FROM python:3.10.9-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies using uv
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY app/ .

# Create non-root user for security
RUN adduser --disabled-password --gecos '' ecguser && \
    chown -R ecguser:ecguser /app
USER ecguser

EXPOSE 8000

# Run the application
CMD ["fastapi", "run"]
