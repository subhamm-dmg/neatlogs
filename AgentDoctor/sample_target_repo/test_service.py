"""
sample_target_repo/test_service.py
Regression Test Suite for RateLimiter microservice.
Fails on unpatched service.py because last_refill timestamp drift causes erroneous replenishments.
"""

import time
import sys
from service import RateLimiter


def test_basic_allowance():
    limiter = RateLimiter(rate_per_second=10.0, capacity=10)
    allowed, meta = limiter.allow_request(5)
    assert allowed is True, "Initial tokens should allow request"
    assert meta["tokens_remaining"] == 5.0, f"Expected 5.0 tokens remaining, got {meta['tokens_remaining']}"


def test_burst_exhaustion():
    limiter = RateLimiter(rate_per_second=20.0, capacity=20)
    # Drain entire bucket
    allowed, _ = limiter.allow_request(20)
    assert allowed is True, "Capacity-sized request should be permitted"
    
    # Immediate subsequent request must be denied
    allowed, meta = limiter.allow_request(1)
    assert allowed is False, "Request beyond empty bucket must be rejected"
    assert meta["lockouts"] == 1, f"Lockouts counter should increment to 1, got {meta['lockouts']}"


def test_replenishment_timing():
    limiter = RateLimiter(rate_per_second=20.0, capacity=20)
    limiter.allow_request(20)
    
    # Wait 0.15s -> should refill ~3.0 tokens
    time.sleep(0.15)
    allowed, meta = limiter.allow_request(2)
    assert allowed is True, f"Request for 2 tokens should succeed after 0.15s, remaining={meta['tokens_remaining']}"


def test_burst_refill_and_continuity():
    limiter = RateLimiter(rate_per_second=20.0, capacity=20)
    # Drain capacity
    allowed, _ = limiter.allow_request(20)
    assert allowed is True
    
    # Rejection under zero balance
    allowed, _ = limiter.allow_request(1)
    assert allowed is False, "Should reject when capacity is exhausted"
    
    # Wait 0.25 seconds (replenishes ~5 tokens)
    time.sleep(0.25)
    allowed, meta = limiter.allow_request(4)
    assert allowed is True, f"Should allow request after 0.25s replenishment, remaining={meta['tokens_remaining']}"
    
    # Immediate subsequent request: only ~1 token left; request for 2 must fail!
    # Bugs that fail to update last_refill will recalculate elapsed time and falsely grant 5 tokens again!
    allowed, meta2 = limiter.allow_request(2)
    assert allowed is False, (
        f"CRITICAL DRIFT BUG: Request for 2 tokens was granted (tokens_remaining={meta2['tokens_remaining']}) "
        "because last_refill was not advanced properly!"
    )


if __name__ == "__main__":
    tests = [
        ("test_basic_allowance", test_basic_allowance),
        ("test_burst_exhaustion", test_burst_exhaustion),
        ("test_replenishment_timing", test_replenishment_timing),
        ("test_burst_refill_and_continuity", test_burst_refill_and_continuity)
    ]
    
    print("=" * 60)
    print("🧪 Running RateLimiter Service Test Suite...")
    print("=" * 60)
    
    passed_count = 0
    for name, test_fn in tests:
        try:
            test_fn()
            print(f"  ✅ {name}: PASSED")
            passed_count += 1
        except AssertionError as e:
            print(f"  ❌ {name}: FAILED -> {e}")
            sys.exit(1)
        except Exception as e:
            print(f"  💥 {name}: ERROR -> {e}")
            sys.exit(2)
            
    print("-" * 60)
    print(f"🎉 ALL {passed_count}/{len(tests)} TESTS PASSED SUCCESSFULLY!")
    sys.exit(0)
