#!/usr/bin/env bash

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <source_directory> <target_directory>"
  exit 1
fi

SOURCE_DIR="$1"
TARGET_DIR="$2"

SOURCE_VOLUMES="${SOURCE_DIR}/volumes"
TARGET_VOLUMES="${TARGET_DIR}/volumes"

if [ ! -d "$SOURCE_VOLUMES" ]; then
  echo "Source Volumes not found: $SOURCE_VOLUMES"
  exit 1
fi

mkdir -p "$TARGET_VOLUMES"

for DIR in "$SOURCE_VOLUMES"/*; do
  if [ -d "$DIR" ] && [ -n "$(ls -A "$DIR")" ]; then
    DIR_NAME=$(basename "$DIR")

    if [ -d "${TARGET_VOLUMES}/${DIR_NAME}" ] && [ -n "$(ls -A "${TARGET_VOLUMES}/${DIR_NAME}")" ]; then
      echo "Removing: ${TARGET_VOLUMES}/${DIR_NAME}"
      rm -rf "${TARGET_VOLUMES:?}/${DIR_NAME}"/*
    fi

    echo "Copying: $DIR_NAME"
    cp -r "$DIR" "$TARGET_VOLUMES"
  fi
done

if [ -f "$SOURCE_DIR/env.dev" ]; then
    cp -af "$SOURCE_DIR/env.dev" "$TARGET_DIR/env.dev"
fi

if [ -f "$SOURCE_DIR/env.prod" ]; then
    cp -af "$SOURCE_DIR/env.prod" "$TARGET_DIR/env.prod"
fi

