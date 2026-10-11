"""
sample_target_repo/service.py - Token Bucket Rate Limiter
BUG: Refill calculation fails to advance last_refill on burst consumption.
"""

import time
from typing import Dict, Tuple


class RateLimiter:
    """
    Token-bucket rate limiter.
    BUG: last_refill is never advanced on successful token consumption, causing runaway refills.
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
