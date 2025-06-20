#!/usr/bin/env bash

START_DIR="$(pwd)"

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <target_directory>"
  exit 1
fi

TARGET_DIR="$1"

cd "$TARGET_DIR" || exit 1

if [ ! -s "./env.dev" ]; then
    cp -a "./.env.example" "./env.dev"
fi

cp -af "./env.dev" "./.env"

docker compose build --no-cache
docker compose up -d

echo "Providing Django secret key..."
if ! sh "$START_DIR/provide-django-secret-key.sh"; then
    echo 'Failed to provide Django secret key.'
    exit 1
fi

APP_KEY=$(grep --color=never -Po "^MSVC_APP_SECRET_KEY=\K('?.*'?)" ./.env | sed "s/^'//;s/'$//" || true)

sed -i "s,^MSVC_APP_SECRET_KEY=.*,MSVC_APP_SECRET_KEY='$APP_KEY'," ./env.dev
sed -i "s,^MSVC_APP_SECRET_KEY=.*,MSVC_APP_SECRET_KEY='$APP_KEY'," ./env.prod

docker compose exec dj python manage.py migrate

docker compose down

cd "$START_DIR" || exit 1
