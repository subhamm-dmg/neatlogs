"""
main.py - CLI Entry Point for AgentDoctor
"""

import sys
import argparse
from agent import AgentDoctor
from cfo_model import calculate_agent_economics


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
    when capacity is exceeded, causing sudden zero-token lockouts under burst traffic!
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
        # BUG: missing self.last_refill = now
        return True, {"tokens_remaining": self.tokens, "lockouts": self.lockouts}
'''
    with open("sample_target_repo/service.py", "w", encoding="utf-8") as f:
        f.write(buggy_code)
    print("🔄 [Reset] sample_target_repo/service.py has been reset to its buggy baseline state.")


def main():
    parser = argparse.ArgumentParser(description="AgentDoctor - Autonomous Bug Triage & Self-Healing Agent")
    parser.add_argument("--run", action="store_true", help="Execute the autonomous healing cycle")
    parser.add_argument("--reset", action="store_true", help="Reset target repo to buggy baseline")
    parser.add_argument("--economics", action="store_true", help="Print cfo.ai business plan & unit economics")
    args = parser.parse_args()

    if args.reset:
        reset_repo()
        return

    if args.economics:
        import json
        print(json.dumps(calculate_agent_economics(), indent=2))
        return

    # Default action: reset and run
    reset_repo()
    doctor = AgentDoctor()
    doctor.run_healing_cycle()


if __name__ == "__main__":
    main()
