#!/bin/sh
set -e

# Ensure alembic.ini exists
if [ ! -f alembic.ini ]; then
  echo "❌ No alembic.ini found in /alembic"
  exit 1
fi

echo "✅ Running Alembic migrations..."

# downgrade to base
alembic downgrade base

# Run upgrade
alembic upgrade head

echo "######## INFO ###########"
# get alembic information
alembic current
alembic history --verbose
echo "########################"


# exec "$@"
