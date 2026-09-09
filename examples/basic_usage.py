"""
Run: python3 examples/basic_usage.py
(from the project root, with src/ on the path — see the sys.path
line below, which mirrors how the tests import the package without
requiring `pip install -e .` first.)
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ratelimiter import RateLimitExceeded, TokenBucketLimiter, rate_limited


# --- Basic usage: check allow() directly ---
limiter = TokenBucketLimiter(capacity=3, refill_rate=1)  # 3 burst, 1/sec sustained

print("Direct usage:")
for i in range(5):
    result = "allowed" if limiter.allow("user-42") else "DENIED"
    print(f"  request {i + 1}: {result}")


# --- Decorator usage: per-user limiting on a function ---
api_limiter = TokenBucketLimiter(capacity=2, refill_rate=0.5)


@rate_limited(api_limiter, key_func=lambda user_id, query: user_id)
def handle_search(user_id: str, query: str) -> str:
    return f"results for '{query}'"


print("\nDecorator usage:")
for i in range(3):
    try:
        print(f"  {handle_search('alice', f'query-{i}')}")
    except RateLimitExceeded as e:
        print(f"  denied: {e}")
