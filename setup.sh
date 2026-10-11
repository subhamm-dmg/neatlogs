#!/usr/bin/env bash
set -e
echo "🚀 Setting up AgentDoctor environment..."
python3 -m venv .venv
source .venv/bin/activate
pip install -r AgentDoctor/requirements.txt
echo "✅ Environment setup complete! Use './run.sh' or 'python AgentDoctor/main.py' to run."
