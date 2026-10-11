#!/usr/bin/env bash
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi
export PYTHONPATH="${PYTHONPATH}:$(pwd)/AgentDoctor"
python AgentDoctor/main.py "$@"
