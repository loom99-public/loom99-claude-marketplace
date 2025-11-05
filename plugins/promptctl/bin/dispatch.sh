#!/bin/bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
repo_dir="${script_dir}/../../.."

source "${repo_dir}/.venv/bin/activate"
python3 "${script_dir}/dispatch.py" "$@"
