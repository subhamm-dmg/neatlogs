"""
cfo_model.py - Financial Model & Unit Economics for AgentDoctor / AutoPatch
Built for the #neatHack cfo.ai business plan requirement.
"""

from typing import Dict, Any


def calculate_agent_economics(
    monthly_tickets_resolved: int = 250,
    tier: str = "growth"
) -> Dict[str, Any]:
    """
    Computes pricing, inference costs, infra, developer hours saved,
    gross margin, and runway projection for AgentDoctor.
    """
    # Pricing tiers
    pricing_plans = {
        "starter": {"monthly_price": 499, "included_patches": 100},
        "growth": {"monthly_price": 1499, "included_patches": 400},
        "enterprise": {"monthly_price": 4999, "included_patches": 1500},
    }
    
    plan = pricing_plans.get(tier, pricing_plans["growth"])
    
    # Model & Token Economics (Groq / Ollama / Cloud)
    # Average bug reproduction & patch cycle:
    # 4 LLM turns x 1,800 prompt tokens + 400 completion tokens = 8,800 tokens per patch
    tokens_per_patch = 8800
    cost_per_1m_tokens = 0.59  # Blended inference rate ($0.59 / 1M tokens on Groq Llama 3.3 70B)
    inference_cost_per_patch = (tokens_per_patch / 1_000_000) * cost_per_1m_tokens
    
    # Compute sandbox / test execution container cost ($0.01 per run)
    sandbox_cost_per_patch = 0.012
    total_unit_cost_per_patch = inference_cost_per_patch + sandbox_cost_per_patch
    
    # Monthly Financials
    active_customers = 50 if tier == "growth" else 20
    mrr = active_customers * plan["monthly_price"]
    arr = mrr * 12
    
    monthly_patches = active_customers * monthly_tickets_resolved
    total_cogs = monthly_patches * total_unit_cost_per_patch
    hosting_and_neatlogs_infra = 250.0  # Neatlogs Pro + AWS baseline
    
    gross_profit = mrr - (total_cogs + hosting_and_neatlogs_infra)
    gross_margin_pct = (gross_profit / mrr) * 100 if mrr > 0 else 0.0
    
    # Value Delivered to Customer
    # Average senior engineer hour: $95/hr. Average incident triage & patch time: 2.5 hours.
    human_cost_avoided_per_patch = 2.5 * 95.0  # $237.50
    customer_monthly_savings = (monthly_tickets_resolved * human_cost_avoided_per_patch) - plan["monthly_price"]
    roi_multiple = (monthly_tickets_resolved * human_cost_avoided_per_patch) / plan["monthly_price"]
    
    # Runway Scenario (Assumes $150k seed/grant pool, 3 engineers)
    monthly_fixed_burn = 22000.0  # Payroll & operations
    net_burn = monthly_fixed_burn - gross_profit
    starting_cash = 150000.0
    runway_months = (starting_cash / net_burn) if net_burn > 0 else 999.0

    return {
        "tier": tier,
        "active_customers": active_customers,
        "mrr": round(mrr, 2),
        "arr": round(arr, 2),
        "unit_economics": {
            "tokens_per_patch": tokens_per_patch,
            "inference_cost_per_patch": round(inference_cost_per_patch, 4),
            "sandbox_cost_per_patch": round(sandbox_cost_per_patch, 4),
            "total_unit_cost_per_patch": round(total_unit_cost_per_patch, 4),
        },
        "gross_profit_monthly": round(gross_profit, 2),
        "gross_margin_pct": round(gross_margin_pct, 1),
        "customer_roi": {
            "hours_saved_per_customer_month": round(monthly_tickets_resolved * 2.5, 1),
            "net_monthly_savings_usd": round(customer_monthly_savings, 2),
            "roi_multiple": round(roi_multiple, 1),
        },
        "runway_months": round(runway_months, 1) if runway_months < 900 else "Profitable / Infinite",
    }


if __name__ == "__main__":
    import json
    results = calculate_agent_economics()
    print(json.dumps(results, indent=2))
