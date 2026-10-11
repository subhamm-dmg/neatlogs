"""
main.py - CLI Entry Point for AgentDoctor (#neatHack)
Supports Multi-Agent Swarm execution and selectable incident benchmarks.
"""

import os
import sys
import argparse
import json

# Ensure AgentDoctor directory is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from agent import AgentDoctor
from cfo_model import get_comparative_scenarios, generate_business_plan_markdown
from scenarios import load_scenario, get_available_scenarios


def reset_repo(scenario_id: str = "rate_limiter"):
    target_dir = os.path.join(current_dir, "sample_target_repo")
    sc = load_scenario(scenario_id, target_dir)
    print(f"🔄 [Reset] sample_target_repo/ has been reset to baseline for: {sc['title']} ({sc['category']})")


def main():
    parser = argparse.ArgumentParser(description="AgentDoctor - Autonomous Multi-Agent Bug Triage & Self-Healing Platform")
    parser.add_argument("--run", action="store_true", help="Execute the autonomous multi-agent healing cycle")
    parser.add_argument("--scenario", type=str, default="rate_limiter", choices=["rate_limiter", "schema_mismatch", "cache_leak"],
                        help="Select incident benchmark: rate_limiter | schema_mismatch | cache_leak")
    parser.add_argument("--list-scenarios", action="store_true", help="List all available production benchmark scenarios")
    parser.add_argument("--reset", action="store_true", help="Reset target repo to buggy baseline for scenario")
    parser.add_argument("--economics", action="store_true", help="Generate BUSINESS_PLAN.md & print cfo.ai financial scenarios")
    args = parser.parse_args()

    if args.list_scenarios:
        print("\n📋 Available Production Benchmark Scenarios:")
        for s in get_available_scenarios():
            print(f"  • {s['id']}: {s['title']} [{s['category']}]")
            print(f"    {s['description']}\n")
        return

    if args.reset:
        reset_repo(args.scenario)
        return

    if args.economics:
        plan_path = os.path.join(os.path.dirname(current_dir), "BUSINESS_PLAN.md")
        generate_business_plan_markdown(plan_path)
        print("\n📊 [cfo.ai] Comparative Scenarios (Base vs. Growth):")
        print(json.dumps(get_comparative_scenarios(), indent=2))
        return

    # Default action: reset baseline and run multi-agent swarm
    reset_repo(args.scenario)
    doctor = AgentDoctor()
    results = doctor.run_healing_cycle(scenario_id=args.scenario)
    print("\nFinal Results Summary:")
    print(json.dumps({
        "scenario": results["scenario"]["title"],
        "status": results["status"],
        "attempts_to_heal": results["attempts"],
        "neatlogs_spans": len(results["telemetry_spans"]),
        "entire_checkpoints": len(results["checkpoints"]),
        "gross_margin": f"{results['economics']['gross_margin_pct']}%",
        "customer_roi": f"{results['economics']['customer_roi']['roi_multiple']}x"
    }, indent=2))


if __name__ == "__main__":
    main()
