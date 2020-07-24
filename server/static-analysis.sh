#!/usr/bin/env bash


TOP_LEVEL_DIR="$(cd "$(dirname "$0")"; pwd)"


# run this script from project's parent directory
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)/.."


function run_mypy() {
    mypy ${TOP_LEVEL_DIR}             \
        --ignore-missing-imports      \
        --disallow-untyped-defs       \
        --disallow-untyped-decorators \
        --disallow-incomplete-defs
}

function check_mypy() {
    [[ $(run_mypy) =~ "Success: no issues found in" ]]
}

function run_flake8() {
    # check line-length
    flake8 ${TOP_LEVEL_DIR}     \
        --count                 \
        --statistics            \
        --select=E501           \
        --max-line-length=120   \
        --extend-exclude=venv

    # check the rest while printing source
    flake8 ${TOP_LEVEL_DIR}     \
        --count                 \
        --statistics            \
        --ignore=E501           \
        --show-source           \
        --extend-exclude=venv
}

function check_flake8() {
    [[ $(run_flake8) =~ 0.0 ]]
}

function run_pylint() {
    PYTHONPATH=${TOP_LEVEL_DIR} pylint ${TOP_LEVEL_DIR}     \
        --max-line-length=120                               \
        --ignore-imports=yes                                \
        --ignore=venv                                       \
        --disable="missing-docstring,
                   no-member,
                   broad-except,
                   invalid-name,
                   bad-continuation,
                   too-many-instance-attributes,
                   R0801"
}

function check_pylint() {
    [[ $(run_pylint) =~ rated.at.10\.00\/10 ]]
}

function run_bandit() {
    bandit ${TOP_LEVEL_DIR} -r --exclude="venv,tests"
}

function check_bandit() {
    run_bandit &> /dev/null
}

function run_black() {
    black ${TOP_LEVEL_DIR}      \
        --line-length=120       \
        --target-version=py38   \
        --check                 \
        --diff
}

function check_black() {
    run_black &> /dev/null
}

function check_func() {
    local running=$1
    local method=$2

    echo -n ${running};
    if ${method}; then
        echo -ne "\r\033[0;32m${running}PASS\033[0m\n"
    else
        echo -ne "\r\033[0;31m${running}FAIL\033[0m\n"
        if [[ ${STOP_ON_FAILURE} == 1 ]]; then
            echo "--------------"
            # re-run with output
            method="run_${method#"check_"}"
            ${method}
            exit 1
        fi
    fi
}

function run_all_summary() {
    check_func "mypy......" check_mypy
    check_func "flake8...." check_flake8
    check_func "pylint...." check_pylint
    check_func "black....." check_black
    check_func "bandit...." check_bandit
}

case $1 in
    mypy)
        run_mypy
        ;;
    flake)
        run_flake8
        ;;
    pylint)
        run_pylint
        ;;
    black)
        run_black
        ;;
    bandit)
        run_bandit
        ;;
    --stop-on-failure)
        STOP_ON_FAILURE=1
        run_all_summary
        ;;
    *)
        run_all_summary
        ;;
esac
