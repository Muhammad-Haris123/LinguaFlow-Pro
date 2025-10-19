# Multi-stage build for the multilingual translation service

# Stage 1: Build the backend
FROM python:3.9-slim as backend-builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend/
COPY data/ ./data/
COPY models/ ./models/
COPY training/ ./training/
COPY evaluation/ ./evaluation/

# Stage 2: Build the frontend
FROM node:16-alpine as frontend-builder

WORKDIR /app

# Copy frontend package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy frontend source code
COPY frontend/ ./

# Build the frontend
RUN npm run build

# Stage 3: Final production image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder
COPY --from=backend-builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=backend-builder /usr/local/bin /usr/local/bin

# Copy backend code
COPY backend/ ./backend/
COPY data/ ./data/
COPY models/ ./models/
COPY training/ ./training/
COPY evaluation/ ./evaluation/

# Copy built frontend from builder
COPY --from=frontend-builder /app/build ./frontend/build

# Create necessary directories
RUN mkdir -p logs checkpoints data/cache

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose ports
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]



