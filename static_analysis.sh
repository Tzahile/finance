#!/usr/bin/env bash

function run_mypy() {
    mypy .                            \
        --ignore-missing-imports      \
        --disallow-untyped-defs       \
        --disallow-untyped-decorators \
        --disallow-incomplete-defs
}

function run_flake8() {
    # check line-length without printing source
    flake8 . --count --statistics --select=E501 --max-line-length=127 --extend-exclude=venv

    # check the rest while printing source
    flake8 . --count --statistics --ignore=E501 --show-source --extend-exclude=venv
}

function run_pylint() {
    cd ..
    pylint finance                                          \
        --max-line-length=120                               \
        --disable=missing-docstring,no-member,broad-except  \
        --variable-rgx="^[a-z][a-z0-9]*((_[a-z0-9]+)*)?$"   \
        --argument-rgx="^[a-z][a-z0-9]*((_[a-z0-9]+)*)?$"   \
        --ignore=venv
    cd finance
}

function run_bandit() {
    bandit . -r --exclude="./venv"
}

function run_black() {
    black . --check --line-length=120 --target-version=py38 --diff
}

read -p "mypy? [y/n] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    run_mypy
fi

read -p "flake8? [y/n] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    run_flake8
fi

read -p "pylint? [y/n] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    run_pylint
fi

read -p "black? [y/n] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    run_black
fi

read -p "bandit? [y/n] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    run_bandit
fi
