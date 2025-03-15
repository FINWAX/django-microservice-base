#!/usr/bin/env bash

REPO_PATH="FINWAX/django-microservice-base"
TARGET_DIR="./msvc"

while getopts d:r: flag; do
    case "${flag}" in
    d*) TARGET_DIR=${OPTARG} ;;
    r*) REPO_PATH=${OPTARG} ;;
    esac
done

mkdir -p "$TARGET_DIR"

if command -v gh &> /dev/null; then
  gh repo clone "$REPO_PATH" "$TARGET_DIR"
else
  curl -sL "https://github.com/$REPO_PATH/archive/refs/heads/master.tar.gz" | tar -xz -C "$TARGET_DIR" --strip-components=1
fi
