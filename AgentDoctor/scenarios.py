"""
scenarios.py - Multi-Bug Production Incident Benchmark Suite for AgentDoctor
Defines 3 distinct production failure scenarios:
  1. Rate Limiter Timestamp Drift (Concurrency / Timing)
  2. Agent Tool Schema Mismatch (API Payload Regression)
  3. Unbounded Cache Memory Leak (Resource Exhaustion & Stale TTL)
"""

import os
from typing import Dict, Any, List

SCENARIOS: Dict[str, Dict[str, Any]] = {
    "rate_limiter": {
        "id": "rate_limiter",
        "title": "Token Bucket Timestamp Drift",
        "category": "Concurrency & Timing",
        "description": "Refill calculation fails to update last_refill timestamp correctly on burst consumption, causing false continuous replenishments.",
        "target_file": "service.py",
        "test_file": "test_service.py",
        "buggy_code": '''"""
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
''',
        "attempt1_code": '''"""
sample_target_repo/service.py - Token Bucket Rate Limiter
[ATTEMPT 1 PATCH - Naive update before elapsed calculation]
"""

import time
from typing import Dict, Tuple


class RateLimiter:
    def __init__(self, rate_per_second: float = 10.0, capacity: int = 20):
        self.rate = float(rate_per_second)
        self.capacity = float(capacity)
        self.tokens: float = float(capacity)
        self.last_refill = time.time()
        self.lockouts = 0

    def allow_request(self, tokens_needed: int = 1) -> Tuple[bool, Dict[str, float]]:
        now = time.time()
        # Flawed: last_refill updated before computing elapsed results in elapsed = 0!
        self.last_refill = now
        elapsed = max(0.0, now - self.last_refill)
        refill = elapsed * self.rate
        self.tokens = min(self.capacity, self.tokens + refill)

        if self.tokens < tokens_needed:
            self.lockouts += 1
            return False, {"tokens_remaining": round(self.tokens, 2), "lockouts": self.lockouts}

        self.tokens -= tokens_needed
        return True, {"tokens_remaining": round(self.tokens, 2), "lockouts": self.lockouts}
''',
        "attempt2_code": '''"""
sample_target_repo/service.py - Token Bucket Rate Limiter
[VERIFIED RESOLUTION - Synchronized timestamp advancement and capacity clamping]
"""

import time
from typing import Dict, Tuple


class RateLimiter:
    def __init__(self, rate_per_second: float = 10.0, capacity: int = 20):
        self.rate = float(rate_per_second)
        self.capacity = float(capacity)
        self.tokens: float = float(capacity)
        self.last_refill = time.time()
        self.lockouts = 0

    def allow_request(self, tokens_needed: int = 1) -> Tuple[bool, Dict[str, float]]:
        now = time.time()
        elapsed = max(0.0, now - self.last_refill)
        
        # Accurately compute replenished tokens based on elapsed interval
        refill = elapsed * self.rate
        self.tokens = min(self.capacity, self.tokens + refill)
        self.last_refill = now

        if self.tokens < tokens_needed:
            self.lockouts += 1
            return False, {"tokens_remaining": round(self.tokens, 2), "lockouts": self.lockouts}

        self.tokens -= tokens_needed
        return True, {"tokens_remaining": round(self.tokens, 2), "lockouts": self.lockouts}
''',
        "test_code": '''"""
sample_target_repo/test_service.py - Regression Suite for RateLimiter
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
    allowed, _ = limiter.allow_request(20)
    assert allowed is True, "Capacity-sized request should be permitted"
    
    allowed, meta = limiter.allow_request(1)
    assert allowed is False, "Request beyond empty bucket must be rejected"
    assert meta["lockouts"] == 1, f"Lockouts counter should increment to 1, got {meta['lockouts']}"


def test_replenishment_timing():
    limiter = RateLimiter(rate_per_second=20.0, capacity=20)
    limiter.allow_request(20)
    
    time.sleep(0.15)
    allowed, meta = limiter.allow_request(2)
    assert allowed is True, f"Request for 2 tokens should succeed after 0.15s, remaining={meta['tokens_remaining']}"


def test_burst_refill_and_continuity():
    limiter = RateLimiter(rate_per_second=20.0, capacity=20)
    allowed, _ = limiter.allow_request(20)
    assert allowed is True
    
    allowed, _ = limiter.allow_request(1)
    assert allowed is False, "Should reject when capacity is exhausted"
    
    time.sleep(0.25)
    allowed, meta = limiter.allow_request(4)
    assert allowed is True, f"Should allow request after 0.25s replenishment, remaining={meta['tokens_remaining']}"
    
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
'''
    },

    "schema_mismatch": {
        "id": "schema_mismatch",
        "title": "Agent Tool Schema Mismatch",
        "category": "API & Payload Regressions",
        "description": "An upstream tool response format changed without backward compatibility, throwing KeyError and breaking downstream agent pipelines.",
        "target_file": "service.py",
        "test_file": "test_service.py",
        "buggy_code": '''"""
sample_target_repo/service.py - Agent Tool Payload Normalizer
BUG: Assumes legacy flat schema, crashes with KeyError when upstream API returns nested structure.
"""

from typing import Dict, Any, List


class ToolDataParser:
    """Parses agent tool responses into standardized record summaries."""

    def normalize_payload(self, raw_response: Dict[str, Any]) -> Dict[str, Any]:
        # BUG: Rigid key access fails when API returns nested 'result' or renamed fields
        items = raw_response["data"]["items"]
        total_count = raw_response["total"]
        
        processed = [{"id": item["id"], "value": item.get("val", 0)} for item in items]
        return {
            "status": "success",
            "count": len(processed),
            "total_reported": total_count,
            "records": processed
        }
''',
        "attempt1_code": '''"""
sample_target_repo/service.py - Agent Tool Payload Normalizer
[ATTEMPT 1 PATCH - Handled nested result but missed default fallback for total]
"""

from typing import Dict, Any, List


class ToolDataParser:
    def normalize_payload(self, raw_response: Dict[str, Any]) -> Dict[str, Any]:
        data = raw_response.get("data") or raw_response.get("result", {})
        items = data.get("items") or data.get("records") or []
        # Flawed: Still hard-indexes raw_response["total"] which causes KeyError when omitted!
        total_count = raw_response["total"]
        
        processed = [{"id": item.get("id"), "value": item.get("val", item.get("value", 0))} for item in items]
        return {
            "status": "success",
            "count": len(processed),
            "total_reported": total_count,
            "records": processed
        }
''',
        "attempt2_code": '''"""
sample_target_repo/service.py - Agent Tool Payload Normalizer
[VERIFIED RESOLUTION - Robust normalization with polymorphic schema support]
"""

from typing import Dict, Any, List


class ToolDataParser:
    def normalize_payload(self, raw_response: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(raw_response, dict):
            return {"status": "error", "count": 0, "total_reported": 0, "records": []}

        # Resolve payload container across both legacy ('data') and modern ('result') shapes
        data = raw_response.get("data") if isinstance(raw_response.get("data"), dict) else raw_response.get("result", {})
        if not isinstance(data, dict):
            items = []
        else:
            items = data.get("items") or data.get("records") or []

        if not isinstance(items, list):
            items = []

        # Graceful fallback for total count
        total_count = raw_response.get("total", data.get("total_count", len(items)))

        processed = [
            {"id": item.get("id", idx), "value": item.get("val", item.get("value", 0))}
            for idx, item in enumerate(items) if isinstance(item, dict)
        ]

        return {
            "status": "success",
            "count": len(processed),
            "total_reported": total_count,
            "records": processed
        }
''',
        "test_code": '''"""
sample_target_repo/test_service.py - Regression Suite for ToolDataParser
"""

import sys
from service import ToolDataParser


def test_legacy_flat_schema():
    parser = ToolDataParser()
    payload = {"data": {"items": [{"id": 1, "val": 100}]}, "total": 1}
    res = parser.normalize_payload(payload)
    assert res["status"] == "success"
    assert res["count"] == 1
    assert res["total_reported"] == 1


def test_modern_nested_schema_with_records():
    parser = ToolDataParser()
    # Modern schema from upstream microservice (nested 'result.records' without root 'total')
    payload = {
        "result": {
            "records": [{"id": "a1", "value": 50}, {"id": "b2", "value": 75}],
            "total_count": 2
        }
    }
    res = parser.normalize_payload(payload)
    assert res["status"] == "success", f"Expected success status, got {res['status']}"
    assert res["count"] == 2, f"Expected count 2, got {res['count']}"
    assert res["total_reported"] == 2, f"Expected total_reported 2, got {res['total_reported']}"


def test_empty_and_graceful_recovery():
    parser = ToolDataParser()
    res = parser.normalize_payload({})
    assert res["status"] in ["success", "error"]
    assert res["count"] == 0


if __name__ == "__main__":
    tests = [
        ("test_legacy_flat_schema", test_legacy_flat_schema),
        ("test_modern_nested_schema_with_records", test_modern_nested_schema_with_records),
        ("test_empty_and_graceful_recovery", test_empty_and_graceful_recovery)
    ]
    
    print("=" * 60)
    print("🧪 Running ToolDataParser Schema Test Suite...")
    print("=" * 60)
    
    passed_count = 0
    for name, test_fn in tests:
        try:
            test_fn()
            print(f"  ✅ {name}: PASSED")
            passed_count += 1
        except KeyError as e:
            print(f"  ❌ {name}: FAILED -> KeyError: {e}")
            sys.exit(1)
        except AssertionError as e:
            print(f"  ❌ {name}: FAILED -> {e}")
            sys.exit(1)
        except Exception as e:
            print(f"  💥 {name}: ERROR -> {e}")
            sys.exit(2)
            
    print("-" * 60)
    print(f"🎉 ALL {passed_count}/{len(tests)} TESTS PASSED SUCCESSFULLY!")
    sys.exit(0)
'''
    },

    "cache_leak": {
        "id": "cache_leak",
        "title": "Unbounded Memory Cache & TTL Leak",
        "category": "Resource Exhaustion",
        "description": "In-memory cache stores session tokens without LRU eviction and fails to invalidate expired TTL entries, risking OOM and stale reads.",
        "target_file": "service.py",
        "test_file": "test_service.py",
        "buggy_code": '''"""
sample_target_repo/service.py - In-Memory Session Cache
BUG: Fails to evict expired TTL items or cap max capacity, causing memory leak and stale reads.
"""

import time
from typing import Dict, Any, Optional


class SessionCache:
    """Session cache with TTL expiration and bounded capacity."""

    def __init__(self, max_entries: int = 5, default_ttl_sec: float = 0.2):
        self.max_entries = max_entries
        self.default_ttl = default_ttl_sec
        self.store: Dict[str, Any] = {}
        # BUG: Missing timestamps mapping for eviction and missing capacity check!

    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        # BUG: Memory leak - continuously appends without respecting max_entries
        self.store[key] = value

    def get(self, key: str) -> Optional[Any]:
        # BUG: Stale read - returns expired entries indefinitely!
        return self.store.get(key)

    def size(self) -> int:
        return len(self.store)
''',
        "attempt1_code": '''"""
sample_target_repo/service.py - In-Memory Session Cache
[ATTEMPT 1 PATCH - Handled TTL check on read but missed LRU max capacity eviction]
"""

import time
from typing import Dict, Any, Optional


class SessionCache:
    def __init__(self, max_entries: int = 5, default_ttl_sec: float = 0.2):
        self.max_entries = max_entries
        self.default_ttl = default_ttl_sec
        self.store: Dict[str, Any] = {}
        self.expiry: Dict[str, float] = {}

    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        # Flawed: Still doesn't evict oldest entries when size exceeds max_entries!
        effective_ttl = ttl if ttl is not None else self.default_ttl
        self.store[key] = value
        self.expiry[key] = time.time() + effective_ttl

    def get(self, key: str) -> Optional[Any]:
        if key in self.store:
            if time.time() > self.expiry.get(key, 0):
                del self.store[key]
                del self.expiry[key]
                return None
            return self.store[key]
        return None

    def size(self) -> int:
        return len(self.store)
''',
        "attempt2_code": '''"""
sample_target_repo/service.py - In-Memory Session Cache
[VERIFIED RESOLUTION - Active TTL eviction and bounded FIFO/LRU capacity enforcement]
"""

import time
from collections import OrderedDict
from typing import Dict, Any, Optional


class SessionCache:
    def __init__(self, max_entries: int = 5, default_ttl_sec: float = 0.2):
        self.max_entries = max_entries
        self.default_ttl = default_ttl_sec
        self.store: OrderedDict[str, Any] = OrderedDict()
        self.expiry: Dict[str, float] = {}

    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        effective_ttl = ttl if ttl is not None else self.default_ttl
        
        # Enforce max capacity bounding
        if key not in self.store and len(self.store) >= self.max_entries:
            oldest_key, _ = self.store.popitem(last=False)
            self.expiry.pop(oldest_key, None)

        self.store[key] = value
        self.store.move_to_end(key)
        self.expiry[key] = time.time() + effective_ttl

    def get(self, key: str) -> Optional[Any]:
        if key in self.store:
            if time.time() > self.expiry.get(key, 0):
                self.store.pop(key, None)
                self.expiry.pop(key, None)
                return None
            self.store.move_to_end(key)
            return self.store[key]
        return None

    def size(self) -> int:
        return len(self.store)
''',
        "test_code": '''"""
sample_target_repo/test_service.py - Regression Suite for SessionCache
"""

import time
import sys
from service import SessionCache


def test_basic_set_get():
    cache = SessionCache(max_entries=3, default_ttl_sec=1.0)
    cache.set("user_1", "active")
    assert cache.get("user_1") == "active"
    assert cache.size() == 1


def test_ttl_expiration_eviction():
    cache = SessionCache(max_entries=5, default_ttl_sec=0.15)
    cache.set("temp_key", "temporary_token")
    assert cache.get("temp_key") == "temporary_token"
    
    # Wait for TTL to elapse
    time.sleep(0.2)
    val = cache.get("temp_key")
    assert val is None, f"Expected key to be evicted after TTL expiration, but got '{val}'"


def test_capacity_bound_no_unbounded_leak():
    cache = SessionCache(max_entries=3, default_ttl_sec=5.0)
    # Insert 6 keys into capacity 3
    for i in range(6):
        cache.set(f"key_{i}", f"val_{i}")
        
    assert cache.size() <= 3, f"Memory leak detected: Cache size grew to {cache.size()}, exceeding max limit of 3!"
    assert cache.get("key_0") is None, "Oldest key should have been evicted"
    assert cache.get("key_5") == "val_5", "Latest key must be present"


if __name__ == "__main__":
    tests = [
        ("test_basic_set_get", test_basic_set_get),
        ("test_ttl_expiration_eviction", test_ttl_expiration_eviction),
        ("test_capacity_bound_no_unbounded_leak", test_capacity_bound_no_unbounded_leak)
    ]
    
    print("=" * 60)
    print("🧪 Running SessionCache Memory & TTL Test Suite...")
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
'''
    }
}


def load_scenario(scenario_id: str, target_dir: str) -> Dict[str, Any]:
    """Loads and writes the specified scenario files into the target repository directory."""
    if scenario_id not in SCENARIOS:
        scenario_id = "rate_limiter"

    sc = SCENARIOS[scenario_id]
    os.makedirs(target_dir, exist_ok=True)

    target_path = os.path.join(target_dir, sc["target_file"])
    test_path = os.path.join(target_dir, sc["test_file"])

    with open(target_path, "w", encoding="utf-8") as f:
        f.write(sc["buggy_code"])

    with open(test_path, "w", encoding="utf-8") as f:
        f.write(sc["test_code"])

    return sc


def get_available_scenarios() -> List[Dict[str, Any]]:
    return [
        {
            "id": sc["id"],
            "title": sc["title"],
            "category": sc["category"],
            "description": sc["description"]
        }
        for sc in SCENARIOS.values()
    ]
