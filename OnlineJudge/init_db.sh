#! /bin/bash
set -x

dirname=$(dirname "$(realpath "$0")")
pushd $dirname

if [[ ! -f manage.py ]]; then
    echo "No manage.py, wrong location"
    exit 1
fi

sleep 2

docker ps --filter "name=oj-postgres-dev" --format "{{.Names}}" | grep "oj-postgres-dev" > /dev/null
if [[ $? -eq 1 ]]; then
  docker rm -f oj-postgres-dev 1>/dev/null 2>&1
  docker run -it -d -e POSTGRES_DB=onlinejudge -e POSTGRES_USER=onlinejudge -e POSTGRES_PASSWORD=onlinejudge -p 127.0.0.1:5435:5432 --name oj-postgres-dev postgres:10
fi

docker ps --filter "name=oj-redis-dev" --format "{{.Names}}" | grep "oj-redis-dev" > /dev/null
if [[ $? -eq 1 ]]; then
  docker rm -f oj-redis-dev 1>/dev/null 2>&1
  docker run -it -d -p 127.0.0.1:6380:6379 --name oj-redis-dev redis:4.0-alpine
fi

if [ "$1" = "--migrate" ]; then
    sleep 3
    echo `cat /dev/urandom | head -1 | md5sum | head -c 32` > data/config/secret.key
    python manage.py migrate
    python manage.py inituser --username root --password rootroot --action create_super_admin
fi

popd
