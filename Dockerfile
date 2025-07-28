FROM python:3.11-slim

# Install system dependencies for native libraries
RUN apt-get update && apt-get install -y \
    libssl3 \
    libstdc++6 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Create necessary directories
RUN mkdir -p libs

# Copy application files
COPY *.py ./
COPY libs/libnabto_client_api.so ./libs/
COPY pichler.ini ./
COPY unabto_queries.xml ./

# Create a non-root user for security
RUN groupadd -r pichler && useradd -r -g pichler pichler
RUN chown -R pichler:pichler /app
USER pichler

# Expose the port the app runs on
EXPOSE 8000

CMD ["python", "main.py"]
