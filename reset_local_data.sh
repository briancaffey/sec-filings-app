docker-compose down

docker volume rm form13-project_pg-data form13-project_redis-data

docker-compose up &

docker exec $(docker ps -q -f name="backend") python3 manage.py migrate --no-input
docker exec $(docker ps -q -f name="backend") python3 manage.py collectstatic --no-input
docker exec $(docker ps -q -f name="backend") python3 manage.py createsuperuser --no-input