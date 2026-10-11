#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PYTHONPATH="${PYTHONPATH}:${SCRIPT_DIR}/AgentDoctor"

if [ -f "${SCRIPT_DIR}/.venv/bin/python" ]; then
    exec "${SCRIPT_DIR}/.venv/bin/python" "${SCRIPT_DIR}/AgentDoctor/main.py" "$@"
else
    exec python3 "${SCRIPT_DIR}/AgentDoctor/main.py" "$@"
fi
