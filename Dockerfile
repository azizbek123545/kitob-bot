FROM python:3.9

# Set working directory
WORKDIR /app

# Install system dependencies for better compatibility
RUN apt-get update && apt-get install -y \
    gcc \
    sqlite3 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data/books logs

# Set proper permissions
RUN chmod +x main.py && chmod -R 755 data/

# Create non-root user for security
RUN useradd -m -u 1000 botuser && chown -R botuser:botuser /app
USER botuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8080}/health || exit 1

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV PORT=8080

# Expose port for Railway
EXPOSE $PORT

# Run the bot
CMD ["python", "main.py"]