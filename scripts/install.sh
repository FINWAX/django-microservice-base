#!/usr/bin/env bash

START_DIR=$(pwd)

USER_ID=$(id -u)
GROUP_ID=$(id -g)
REPO_PATH="FINWAX/django-microservice-base"
CUR_DIR="./msvc"
PREV_DIR="./prev"

while getopts u:g:r:d:p: flag; do
    case "${flag}" in
    u*) USER_ID=${OPTARG} ;;
    g*) GROUP_ID=${OPTARG} ;;
    r*) REPO_PATH=${OPTARG} ;;
    d*) CUR_DIR=${OPTARG} ;;
    p*) PREV_DIR=${OPTARG} ;;
    esac
done

export WWWGROUP=$GROUP_ID
export WWWUSER=$USER_ID

echo "Pulling..."
if ! sh "$START_DIR/pull.sh" -r"$REPO_PATH" -d"$CUR_DIR"; then
    echo 'Failed to pull repo'
    exit 1
fi

echo "Preparation..."
if ! sh "$START_DIR/prepare.sh" -u"$USER_ID" -g"$GROUP_ID" -d"$CUR_DIR"; then
    echo 'Failed to prepare project'
    exit 1
fi

if [ -d "$PREV_DIR" ]; then
    echo "Importing..."
    if ! sh "$START_DIR/import.sh" "$PREV_DIR" "$CUR_DIR"; then
        echo 'Failed to import project'
        exit 1
    fi
fi

echo "Installation is done!"
cd "$START_DIR" || exit 1;
