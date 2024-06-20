start-dev:
  uvicorn app.main:app --reload


start:
  uvicorn app.main:app

  # Initialize your local database
psql-up:
docker compose -f .docker/docker-compose.yml up -d --build --force-recreate --remove-orphans db
# Remove your local database
psql-down:
sudo docker compose -f .docker/docker-compose.yml down -v --remove-orphans