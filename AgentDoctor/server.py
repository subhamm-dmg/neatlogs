"""
server.py - Interactive Web Dashboard & Demo Server for AgentDoctor (#neatHack)
"""

import os
import sys

# Ensure current directory is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from flask import Flask, render_template, jsonify
from agent import AgentDoctor
from main import reset_repo
from cfo_model import get_comparative_scenarios
from entire_manager import EntireCheckpointManager

base_dir = os.path.dirname(os.path.abspath(__file__))
workspace_dir = os.path.dirname(base_dir)
template_dir = os.path.join(base_dir, "templates")
app = Flask(__name__, template_folder=template_dir)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/run")
def run_agent():
    # Reset first to ensure baseline pre-fix failure is captured
    reset_repo()
    doctor = AgentDoctor()
    results = doctor.run_healing_cycle()
    return jsonify(results)


@app.route("/api/reset")
def reset_service():
    reset_repo()
    return jsonify({"status": "reset_successful", "message": "sample_target_repo/service.py reset to buggy baseline"})


@app.route("/api/economics")
def get_economics():
    return jsonify(get_comparative_scenarios())


@app.route("/api/entire/checkpoints")
def get_checkpoints():
    mgr = EntireCheckpointManager(workspace_dir)
    return jsonify(mgr.list_checkpoints())


@app.route("/api/entire/graph")
def get_graph():
    doctor = AgentDoctor()
    return jsonify(doctor.tool_query_entire_graph())


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    print(f"\n🌐 [Dashboard Ready] Open http://localhost:{port} in your browser for the live demo!")
    app.run(host="0.0.0.0", port=port, debug=False)
