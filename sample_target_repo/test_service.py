"""
sample_target_repo/test_service.py
Unit tests for RateLimiter.
Fails on unpatched service.py because last_refill is not advanced, leading to token drift.
"""

import time
from service import RateLimiter


def test_basic_allowance():
    limiter = RateLimiter(rate_per_second=10.0, capacity=10)
    allowed, meta = limiter.allow_request(5)
    assert allowed is True, "Initial tokens should allow request"
    assert meta["tokens_remaining"] == 5.0


def test_burst_refill_and_continuity():
    limiter = RateLimiter(rate_per_second=20.0, capacity=20)
    # Consume all tokens
    allowed, _ = limiter.allow_request(20)
    assert allowed is True
    
    # Check immediate rejection
    allowed, _ = limiter.allow_request(1)
    assert allowed is False, "Should reject when capacity is exhausted"
    
    # Wait 0.25 seconds (should replenish ~5 tokens)
    time.sleep(0.25)
    allowed, meta = limiter.allow_request(4)
    assert allowed is True, f"Should allow request after 0.25s replenishment, remaining={meta['tokens_remaining']}"
    
    # Immediate subsequent request should reflect correct remaining balance
    allowed, meta2 = limiter.allow_request(2)
    assert allowed is False, "Should reject because only ~1 token remains after consuming 4"


if __name__ == "__main__":
    print("Running test_basic_allowance...")
    test_basic_allowance()
    print("Running test_burst_refill_and_continuity...")
    test_burst_refill_and_continuity()
    print("ALL TESTS PASSED!")
