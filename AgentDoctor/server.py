"""
server.py - Interactive Web Dashboard & Demo Server for AgentDoctor (#neatHack)
Features:
  - Multi-Agent Swarm Visualizer
  - Benchmark Scenario Selector (3 scenarios)
  - Interactive cfo.ai Dynamic Financial Slider
  - Interactive Entire AST Graph & Git Diff Inspector
"""

import os
import sys

# Ensure current directory is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from flask import Flask, render_template, jsonify, request
from agent import AgentDoctor
from main import reset_repo
from cfo_model import get_comparative_scenarios, calculate_scenario
from entire_manager import EntireCheckpointManager
from scenarios import get_available_scenarios, load_scenario

base_dir = os.path.dirname(os.path.abspath(__file__))
workspace_dir = os.path.dirname(base_dir)
template_dir = os.path.join(base_dir, "templates")
app = Flask(__name__, template_folder=template_dir)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/scenarios")
def list_scenarios():
    return jsonify(get_available_scenarios())


@app.route("/api/run")
def run_agent():
    scenario_id = request.args.get("scenario", "rate_limiter")
    # Reset first to ensure baseline pre-fix failure is captured
    reset_repo(scenario_id)
    doctor = AgentDoctor()
    results = doctor.run_healing_cycle(scenario_id=scenario_id)
    return jsonify(results)


@app.route("/api/reset")
def reset_service():
    scenario_id = request.args.get("scenario", "rate_limiter")
    reset_repo(scenario_id)
    return jsonify({
        "status": "reset_successful",
        "scenario": scenario_id,
        "message": f"sample_target_repo/ reset to buggy baseline for {scenario_id}"
    })


@app.route("/api/economics")
def get_economics():
    return jsonify(get_comparative_scenarios())


@app.route("/api/economics/simulate")
def simulate_economics():
    customers = int(request.args.get("customers", 250))
    tier = request.args.get("tier", "growth")
    avg_tickets = int(request.args.get("avg_tickets", 250))
    data = calculate_scenario(customers=customers, avg_tickets_per_customer=avg_tickets, tier_name=tier)
    return jsonify(data)


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
