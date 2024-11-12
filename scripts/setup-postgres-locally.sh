#!/bin/bash

# Set default values for the PostgreSQL container
POSTGRES_USER="postgres"
POSTGRES_PASSWORD="password"
POSTGRES_DB="voice-testdb"
CONTAINER_NAME="llm-voice-local-postgres"
POSTGRES_PORT="5432"
POSTGRES_VERSION="latest"
PGVECTOR_VERSION="0.4.2"

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Now you can use SCRIPT_DIR to construct relative paths
# For example, assuming you want to go to the 'packages/migration' folder relative to the script
MIGRATION_DIR="$SCRIPT_DIR/../packages/migration"

# Check if Docker is installed
if ! [ -x "$(command -v docker)" ]; then
  echo "Error: Docker is not installed." >&2
  exit 1
fi

# Check if the container is already running
if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
  echo "PostgreSQL container ($CONTAINER_NAME) is already running."
else
  # If the container exists but is stopped, start it
  if [ "$(docker ps -aq -f status=exited -f name=$CONTAINER_NAME)" ]; then
    echo "Starting the existing PostgreSQL container..."
    docker start $CONTAINER_NAME
  else
    # Run a new PostgreSQL container
    echo "Pulling PostgreSQL Docker image..."
    docker pull postgres:$POSTGRES_VERSION

    echo "Running PostgreSQL container..."
    docker run --rm --name $CONTAINER_NAME \
      -e POSTGRES_USER=$POSTGRES_USER \
      -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
      -e POSTGRES_DB=$POSTGRES_DB \
      -p $POSTGRES_PORT:5432 \
      -d postgres:$POSTGRES_VERSION

    # Check docker container status
    echo "Checking if PostgreSQL is ready..."
    until docker run --rm --network container:$CONTAINER_NAME postgres pg_isready -h localhost -p 5432; do
      echo "PostgreSQL is not ready yet. Retrying..."
      sleep 1
    done

    echo "PostgreSQL is ready!"
    echo "PostgreSQL container is up and running!"
    echo "Access it using: docker exec -it $CONTAINER_NAME psql -U $POSTGRES_USER -d $POSTGRES_DB"
    echo "Connection string: postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@localhost:$POSTGRES_PORT/$POSTGRES_DB"
  fi
fi

# Install the pgvector extension
echo "Installing pgvector extension..."
docker exec $CONTAINER_NAME bash -c "
  apt-get update && \
  apt-get install -y postgresql-server-dev-all git make gcc && \
  git clone https://github.com/pgvector/pgvector.git && \
  cd pgvector && make && make install
"

# Enable pgvector extension in PostgreSQL
echo "Enabling pgvector extension in the $POSTGRES_DB database..."
docker exec $CONTAINER_NAME psql -U $POSTGRES_USER -d $POSTGRES_DB -c "CREATE EXTENSION IF NOT EXISTS vector;"

echo "pgvector extension installed and enabled in $POSTGRES_DB."

# Check if the migration directory exists
# if [ -d "$MIGRATION_DIR" ]; then
#   echo "Migration directory found at: $MIGRATION_DIR"
#   # Change to the migration directory
#   cd "$MIGRATION_DIR" || exit 1
# else
#   echo "Migration directory does not exist at: $MIGRATION_DIR"
#   exit 1
# fi

echo "Postgres locally setup completed successfully!"
