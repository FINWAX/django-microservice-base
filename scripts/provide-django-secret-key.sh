#!/usr/bin/env bash

ENV_FILE=${1:-".env"}

VARIABLE_NAME="MSVC_APP_SECRET_KEY"

if [ ! -f "$ENV_FILE" ]; then
  echo "ENV File not found."
  exit 1
fi

NEW_SECRET_KEY=$(docker compose exec dj python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
if grep -q "^$VARIABLE_NAME=" "$ENV_FILE"; then
  EXISTING_VALUE=$(grep "^$VARIABLE_NAME=" "$ENV_FILE" | cut -d '=' -f2)

  if [ -z "$EXISTING_VALUE" ]; then
    SECRET_KEY="'$NEW_SECRET_KEY'"
    sed -i "s/^$VARIABLE_NAME=.*/$VARIABLE_NAME=$SECRET_KEY/" "$ENV_FILE"
    echo "File has key variable, but it was empty. New one was generated."
  else
    echo "File has filled key variable."
  fi
else
  echo "$VARIABLE_NAME='$NEW_SECRET_KEY'" >> "$ENV_FILE"
  echo "Key variable was added to file."
fi