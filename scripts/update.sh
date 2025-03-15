#!/usr/bin/env bash

START_DIR=$(pwd)

USER_ID=$(id -u)
GROUP_ID=$(id -g)
REPO_PATH="FINWAX/django-microservice-base"
CURRENT_DIR="./msvc"
BACKUP_DIR="$START_DIR/prev_$(date +'%Y-%d-%m_%H-%M-%S')"

while getopts u:g:r:d:p: flag; do
    case "${flag}" in
    u*) USER_ID=${OPTARG} ;;
    g*) GROUP_ID=${OPTARG} ;;
    r*) REPO_PATH=${OPTARG} ;;
    d*) CURRENT_DIR=${OPTARG} ;;
    p*) BACKUP_DIR=${OPTARG} ;;
    esac
done

echo "Updating..."

if [ ! -d "$CURRENT_DIR" ]; then
    echo "Aim directory doesnt exist!"
    exit 1
fi

cd "$CURRENT_DIR" || exit 1
docker compose down
cd "$START_DIR" || exit 1

mkdir -p "$BACKUP_DIR"

if ! mv "$CURRENT_DIR"/* "$BACKUP_DIR"; then
    echo 'Failed to move current files'
    exit 1
fi
mv -f "$CURRENT_DIR"/.* "$BACKUP_DIR"

echo "New installation..."
if ! sh "$START_DIR/install.sh" -u"$USER_ID" -g"$GROUP_ID" -r"$REPO_PATH" -d"$CURRENT_DIR" -p"$BACKUP_DIR"; then
    echo 'Failed to install last version'
    exit 1
fi

echo "First launching..."
if ! sh "$START_DIR/first-launch.sh" -d"$CURRENT_DIR"; then
    echo 'Failed to do First Launch'
    exit 1
fi

echo "Successful updated!"
