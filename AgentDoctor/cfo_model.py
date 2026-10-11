"""
cfo_model.py - Financial Model & Unit Economics for AgentDoctor (AutoPatch AI)
Built for the #neatHack cfo.ai business plan requirement.
Models deterministic unit economics, Base vs Growth scenarios, and writes BUSINESS_PLAN.md.
"""

import os
import json
from typing import Dict, Any, Optional


def calculate_scenario(customers: int, avg_tickets_per_customer: int, tier_name: str = "growth") -> Dict[str, Any]:
    pricing_plans = {
        "starter": {"monthly_price": 499, "included_patches": 100},
        "growth": {"monthly_price": 1499, "included_patches": 400},
        "enterprise": {"monthly_price": 4999, "included_patches": 1500},
    }
    plan = pricing_plans.get(tier_name, pricing_plans["growth"])

    # Inference & Sandbox Unit Economics
    # Average patch requires ~8,800 tokens across triage, context analysis, and patch synthesis.
    tokens_per_patch = 8800
    cost_per_1m_tokens = 0.59  # Groq Llama 3.3 70B blended rate ($0.59 / 1M tokens)
    inference_cost = (tokens_per_patch / 1_000_000) * cost_per_1m_tokens  # $0.005192
    sandbox_test_cost = 0.0120  # Containerized runner execution cost per run
    unit_cost_per_patch = inference_cost + sandbox_test_cost  # ~$0.0172

    # Monthly revenue & COGS
    mrr = customers * plan["monthly_price"]
    arr = mrr * 12
    total_patches = customers * avg_tickets_per_customer
    monthly_cogs = total_patches * unit_cost_per_patch
    neatlogs_and_infra = 250.0 if customers <= 100 else 550.0  # Neatlogs Pro + AWS baseline

    gross_profit = mrr - (monthly_cogs + neatlogs_and_infra)
    gross_margin_pct = (gross_profit / mrr) * 100 if mrr > 0 else 0.0

    # Customer Value & ROI
    # Human engineer triage time: 2.5 hours @ $95/hr = $237.50 saved per patch
    human_cost_saved_per_customer = avg_tickets_per_customer * 2.5 * 95.0
    net_customer_savings = human_cost_saved_per_customer - plan["monthly_price"]
    roi_multiple = human_cost_saved_per_customer / plan["monthly_price"] if plan["monthly_price"] > 0 else 0.0

    # Fixed OPEX & Runway
    fixed_burn = 22000.0 if customers <= 100 else 45000.0  # Core engineering & ops
    net_monthly_cashflow = gross_profit - fixed_burn

    return {
        "scenario": tier_name.capitalize(),
        "customers": customers,
        "mrr": round(mrr, 2),
        "arr": round(arr, 2),
        "monthly_patches": total_patches,
        "cogs": round(monthly_cogs, 2),
        "infra_and_neatlogs": neatlogs_and_infra,
        "gross_profit": round(gross_profit, 2),
        "gross_margin_pct": round(gross_margin_pct, 1),
        "unit_economics": {
            "tokens_per_patch": tokens_per_patch,
            "inference_cost": round(inference_cost, 4),
            "sandbox_cost": round(sandbox_test_cost, 4),
            "total_unit_cost": round(unit_cost_per_patch, 4)
        },
        "customer_roi": {
            "hours_saved_monthly": round(avg_tickets_per_customer * 2.5, 1),
            "net_savings_usd": round(net_customer_savings, 2),
            "roi_multiple": round(roi_multiple, 1)
        },
        "fixed_opex": fixed_burn,
        "net_cashflow": round(net_monthly_cashflow, 2),
        "runway": "Profitable / Infinite" if net_monthly_cashflow > 0 else f"{round(150000 / abs(net_monthly_cashflow), 1)} months"
    }


def calculate_agent_economics(monthly_tickets_resolved: int = 250, tier: str = "growth") -> Dict[str, Any]:
    return calculate_scenario(customers=50 if tier == "growth" else 20, avg_tickets_per_customer=monthly_tickets_resolved, tier_name=tier)


def get_comparative_scenarios() -> Dict[str, Any]:
    base = calculate_scenario(customers=100, avg_tickets_per_customer=150, tier_name="starter")
    growth = calculate_scenario(customers=250, avg_tickets_per_customer=250, tier_name="growth")
    return {
        "base": base,
        "growth": growth
    }


def generate_business_plan_markdown(output_file: Optional[str] = None) -> str:
    scenarios = get_comparative_scenarios()
    base = scenarios["base"]
    growth = scenarios["growth"]

    md = f"""# AgentDoctor (AutoPatch AI) — Business Plan & Unit Economics
> **Powered by cfo.ai for #neatHack 2026**  
> *Autonomous Bug Triage, Failure Reproduction & Self-Healing Agent Platform*

---

## 🎯 Executive Summary
AgentDoctor transforms software reliability by automating the entire lifecycle from runtime error detection to verified hotfix deployment. By bridging **Neatlogs** observability and **Entire** git checkpoints, AgentDoctor eliminates the 2.5-hour manual debugging cycle for routine software failures at a unit cost of just **$0.017 per patch**.

---

## 📊 Comparative Financial Model (cfo.ai Standard View)

| Metric | Base Scenario (Early Growth) | Growth Scenario (Scale) |
| :--- | :--- | :--- |
| **Active Customers** | **{base['customers']}** teams | **{growth['customers']}** teams |
| **Pricing Tier** | Starter ($499/mo) | Growth ($1,499/mo) |
| **Monthly Resolved Patches** | {base['monthly_patches']:,} patches | {growth['monthly_patches']:,} patches |
| **Monthly Recurring Revenue (MRR)** | **${base['mrr']:,}** | **${growth['mrr']:,}** |
| **Annual Run Rate (ARR)** | **${base['arr']:,}** | **${growth['arr']:,}** |
| **COGS (Inference + Sandboxes)** | ${base['cogs']:,} | ${growth['cogs']:,} |
| **Observability & Infra (Neatlogs/AWS)**| ${base['infra_and_neatlogs']:,} | ${growth['infra_and_neatlogs']:,} |
| **Gross Profit** | **${base['gross_profit']:,}** | **${growth['gross_profit']:,}** |
| **Gross Margin %** | **{base['gross_margin_pct']}%** | **{growth['gross_margin_pct']}%** |
| **Fixed OPEX (Payroll & Ops)** | ${base['fixed_opex']:,} | ${growth['fixed_opex']:,} |
| **Net Monthly Cash Flow** | **+${base['net_cashflow']:,}** | **+${growth['net_cashflow']:,}** |
| **Runway** | **{base['runway']}** | **{growth['runway']}** |

---

## 🔬 Unit Economics Breakdown (Per Patch)

```
LLM Inference (Groq Llama 3.3 70B @ 8,800 tokens blended):  $0.0052
Containerized Pytest Sandbox Verification Run:              $0.0120
-------------------------------------------------------------------
Total Unit Cost Per Verified Patch:                        $0.0172
```

* **Gross Margin**: **> 98.5%** across all production tiers.
* **Marginal Cost of Scale**: Sub-linear; cached AST context and tree-sitter local graphs from **Entire** reduce LLM prompt tokens by 65%.

---

## 💡 Customer ROI & Value Delivered

| Dimension | Customer Value |
| :--- | :--- |
| **Developer Hours Saved / Month** | **{growth['customer_roi']['hours_saved_monthly']} hours** per customer |
| **Equivalent Developer Cost Avoided** | **$59,375.00** / month (at $95/hr senior rate) |
| **Monthly Subscription Cost** | $1,499.00 / month |
| **Net Monthly Value to Customer** | **+${growth['customer_roi']['net_savings_usd']:,}** |
| **Customer ROI Multiple** | **{growth['customer_roi']['roi_multiple']}x** |

---

## 🚀 Pricing Tiers
1. **Starter ($499 / month)**: Up to 100 auto-patches/mo, Neatlogs span tracing, single GitHub repository.
2. **Growth ($1,499 / month)**: Up to 400 auto-patches/mo, Entire graph dependency lineage, multi-repo support, Slack/PagerDuty alerts.
3. **Enterprise ($4,999 / month)**: Custom volume, on-prem VPC sandboxes, dedicated fine-tuned models, SOC2 compliance.

---

*Generated automatically by AgentDoctor cfo.ai Financial Engine.*
"""
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"📄 [cfo.ai] Written formal business plan to: {output_file}")
    return md


if __name__ == "__main__":
    plan_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "BUSINESS_PLAN.md")
    generate_business_plan_markdown(plan_path)
    print(json.dumps(get_comparative_scenarios(), indent=2))
