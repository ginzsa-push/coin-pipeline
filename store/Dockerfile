FROM python:3.11-slim

# Install PostgreSQL client tools (optional but useful)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir sqlalchemy psycopg2-binary alembic

# Working directory for Alembic
WORKDIR /alembic

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
