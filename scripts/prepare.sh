#!/usr/bin/env bash

START_DIR=$(pwd)

USER_ID=$(id -u)
GROUP_ID=$(id -g)
TARGET_DIR="./msvc"

while getopts u:g:d: flag; do
    case "${flag}" in
    u*) USER_ID=${OPTARG} ;;
    g*) GROUP_ID=${OPTARG} ;;
    d*) TARGET_DIR=${OPTARG} ;;
    esac
done

if [ ! -d "$TARGET_DIR" ]; then
  echo "Target dir not found: $TARGET_DIR"
  exit 1
fi
cd "$TARGET_DIR" || exit 1

mkdir -p "./volumes/django_cache"
mkdir -p "./volumes/pgsql"
mkdir -p "./volumes/mysql"
mkdir -p "./volumes/mariadb"
mkdir -p "./volumes/redis"
mkdir -p "./volumes/selenium/chrome-data"

cp -a "./.env.example" "./env.dev"
cp -a "./.env.example" "./env.prod"

chown -R "$USER_ID":"$GROUP_ID" "$TARGET_DIR"
chmod -R ug+rwx "$TARGET_DIR"

cd "$START_DIR" || exit 1;
