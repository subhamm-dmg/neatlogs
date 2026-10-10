"""
sample_target_repo/service.py
Target service monitored by AgentDoctor: Token Bucket Rate Limiter with burst window.
[PATCHED BY AGENTDOCTOR - VERIFIED VIA NEATLOGS TRACE & ENTIRE CHECKPOINT]
"""

import time
from typing import Dict, Tuple


class RateLimiter:
    """
    Token-bucket rate limiter.
    Patched: Accurate timestamp updates, token replenish clamping, and thread continuity.
    """

    def __init__(self, rate_per_second: float = 10.0, capacity: int = 20):
        self.rate = float(rate_per_second)
        self.capacity = float(capacity)
        self.tokens: float = float(capacity)
        self.last_refill = time.time()
        self.lockouts = 0

    def allow_request(self, tokens_needed: int = 1) -> Tuple[bool, Dict[str, float]]:
        now = time.time()
        elapsed = max(0.0, now - self.last_refill)
        
        # Replenish tokens up to capacity
        replenish = elapsed * self.rate
        self.tokens = min(self.capacity, self.tokens + replenish)
        self.last_refill = now

        if self.tokens < tokens_needed:
            self.lockouts += 1
            return False, {"tokens_remaining": round(self.tokens, 2), "lockouts": self.lockouts}

        self.tokens -= tokens_needed
        return True, {"tokens_remaining": round(self.tokens, 2), "lockouts": self.lockouts}
