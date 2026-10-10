"""
server.py - Interactive Web Dashboard & Demo Server for AgentDoctor (#neatHack)
"""

import os
from flask import Flask, render_template, jsonify
from agent import AgentDoctor
from main import reset_repo
from cfo_model import calculate_agent_economics

base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, "templates")
app = Flask(__name__, template_folder=template_dir)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/run")
def run_agent():
    # Reset first to ensure pre-fix failure is captured
    reset_repo()
    doctor = AgentDoctor()
    results = doctor.run_healing_cycle()
    return jsonify(results)


@app.route("/api/reset")
def reset_service():
    reset_repo()
    return jsonify({"status": "reset_successful"})


@app.route("/api/economics")
def get_economics():
    return jsonify(calculate_agent_economics())


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    print(f"\n🌐 [Dashboard Ready] Open http://localhost:{port} in your browser for the live demo!")
    app.run(host="0.0.0.0", port=port, debug=False)
