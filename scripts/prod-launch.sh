#!/usr/bin/env bash

START_DIR="$(pwd)"

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <target_directory>"
  exit 1
fi

TARGET_DIR="$1"

cd "$TARGET_DIR" || exit 1;
cp -af "./env.prod" "./.env"

docker compose up -d

cd "$START_DIR" || exit 1;
