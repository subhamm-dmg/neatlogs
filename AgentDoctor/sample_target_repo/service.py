"""
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
