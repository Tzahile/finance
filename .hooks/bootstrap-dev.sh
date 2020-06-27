#!/bin/bash


set -e


function install_dev_venv() {
    if [[ -n ${VIRTUAL_ENV} ]]; then
        echo "Already running inside a virtual environment - skipping"
        return
    fi

    if [[ -d venv ]]; then
        echo "venv already exists, activating it"
        if ! source venv/bin/activate &> /dev/null; then
            echo "Error: cannot activate the existing venv, please fix / remove it and re-run"
            exit 1
        fi
    fi

    local py_version="3.8"
    local python="python${py_version}"
    local pip="pip${py_version}"

    if ! command -v ${python} &> /dev/null; then
        echo "ERROR: ${python} is missing. Please make sure you have it installed" 1>&2
        exit 1
    fi

    if ! command -v ${pip} &> /dev/null; then
        echo "ERROR: ${pip} is missing. Please make sure you have it installed" 1>&2
        exit 1
    fi

    if ! command -v virtualenv &> /dev/null; then
        echo "ERROR: virtualenv is missing - installing" 1>&2
        ${pip} install virtualenv
    fi

    echo "Creating venv"
    virtualenv -p ${python} venv
    source venv/bin/activate
}

function install_dev_requirements() {
    if [[ -z ${VIRTUAL_ENV} ]]; then
        echo "Error: you are not running in a virtual environment"
        exit 1
    fi

    if [[ ! $(which pip) =~ "venv/bin/pip" ]]; then
        echo "Error: pip is not found in the virtual environment"
        exit 1
    fi

    echo "Installing requirements"
    pip install -r requirements/dev.txt
    echo "Done"
}

function install_hook() {
    local hook="pre-push"
    local hook_path="${PWD}/.hooks/${hook}"
    local git_hook_path="${PWD}/.git/hooks/${hook}"

    if [[ -n "$NO_HOOKS" ]]; then
        echo "Skipping hooks setup as environment variable NO_HOOKS is set"
        return
    fi

    if [[ -e "${git_hook_path}" ]]; then
        echo "Found ${hook} hook - removing"
        rm "${git_hook_path}"
    fi

    echo "Installing '${hook}' hook"
    ln -s "${hook_path}" "${git_hook_path}"
    chmod +x "${git_hook_path}"
    echo "Done"
}

echo "Stage 1 - Venv Installation"
install_dev_venv
echo ""
echo ""

echo "Stage 2 - Dev Requirements"
install_dev_requirements
echo ""
echo ""

echo "Stage 3 - Install Hook"
install_hook
