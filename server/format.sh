#!/usr/bin/env bash


TOP_LEVEL_DIR="finance"


# run this script from project's parent directory
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)/.."


black ${TOP_LEVEL_DIR}      \
    --line-length=120       \
    --target-version=py38
