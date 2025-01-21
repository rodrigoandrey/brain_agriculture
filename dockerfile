# Dockerfile
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_HOME=/app/brain_agriculture
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONRECURSIONLIMIT=10000

# Set work directory
WORKDIR $APP_HOME

# Install system dependencies and PostgreSQL development files
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    postgresql-server-dev-all \
    python3-dev \
    libpq-dev \
    locales \
    && rm -rf /var/lib/apt/lists/* \
    && locale-gen C.UTF-8

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create entrypoint script
RUN echo '#!/bin/sh' > /entrypoint.sh && \
    echo 'set -e' >> /entrypoint.sh && \
    echo 'python -c "import sys; sys.setrecursionlimit(10000)"' >> /entrypoint.sh && \
    echo 'python manage.py migrate' >> /entrypoint.sh && \
    echo 'python manage.py loaddata fixtures/mock_data.json' >> /entrypoint.sh && \
    echo 'python manage.py runserver 0.0.0.0:8000' >> /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Run entrypoint script
CMD ["/entrypoint.sh"]