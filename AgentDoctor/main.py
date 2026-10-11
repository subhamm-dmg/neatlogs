"""
main.py - CLI Entry Point for AgentDoctor (#neatHack)
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


def reset_repo():
    buggy_code = '''"""
sample_target_repo/service.py
Target service monitored by AgentDoctor: Token Bucket Rate Limiter with burst window.
"""

import time
from typing import Dict, Tuple


class RateLimiter:
    """
    Token-bucket rate limiter.
    BUG: The refill calculation fails to update last_refill_timestamp correctly
    when capacity is exceeded, causing sudden zero-token lockouts or runaway refills under burst traffic!
    """

    def __init__(self, rate_per_second: float = 10.0, capacity: int = 20):
        self.rate = rate_per_second
        self.capacity = capacity
        self.tokens: float = float(capacity)
        self.last_refill = time.time()
        self.lockouts = 0

    def allow_request(self, tokens_needed: int = 1) -> Tuple[bool, Dict[str, float]]:
        now = time.time()
        elapsed = now - self.last_refill
        refill = elapsed * self.rate
        self.tokens = min(float(self.capacity), self.tokens + refill)
        
        if self.tokens < tokens_needed:
            self.lockouts += 1
            return False, {"tokens_remaining": self.tokens, "lockouts": self.lockouts}

        self.tokens -= tokens_needed
        # BUG: missing self.last_refill = now on burst consumption!
        return True, {"tokens_remaining": self.tokens, "lockouts": self.lockouts}
'''
    target_file = os.path.join(current_dir, "sample_target_repo", "service.py")
    with open(target_file, "w", encoding="utf-8") as f:
        f.write(buggy_code)
    print("🔄 [Reset] sample_target_repo/service.py has been reset to its buggy baseline state.")


def main():
    parser = argparse.ArgumentParser(description="AgentDoctor - Autonomous Bug Triage & Self-Healing Agent")
    parser.add_argument("--run", action="store_true", help="Execute the autonomous healing cycle")
    parser.add_argument("--reset", action="store_true", help="Reset target repo to buggy baseline")
    parser.add_argument("--economics", action="store_true", help="Generate BUSINESS_PLAN.md & print cfo.ai financial scenarios")
    args = parser.parse_args()

    if args.reset:
        reset_repo()
        return

    if args.economics:
        plan_path = os.path.join(os.path.dirname(current_dir), "BUSINESS_PLAN.md")
        generate_business_plan_markdown(plan_path)
        print("\n📊 [cfo.ai] Comparative Scenarios (Base vs. Growth):")
        print(json.dumps(get_comparative_scenarios(), indent=2))
        return

    # Default action: reset baseline and run healing cycle
    reset_repo()
    doctor = AgentDoctor()
    doctor.run_healing_cycle()


if __name__ == "__main__":
    main()
