import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ratelimiter import RateLimitExceeded, TokenBucketLimiter, rate_limited
from helpers import FakeClock


class TestDecorator(unittest.TestCase):
    def test_raises_when_limit_exceeded(self):
        clock = FakeClock()
        limiter = TokenBucketLimiter(capacity=1, refill_rate=1, time_func=clock)

        @rate_limited(limiter)
        def handler():
            return "ok"

        self.assertEqual(handler(), "ok")
        with self.assertRaises(RateLimitExceeded):
            handler()

    def test_key_func_gives_independent_limits_per_caller(self):
        clock = FakeClock()
        limiter = TokenBucketLimiter(capacity=1, refill_rate=1, time_func=clock)

        @rate_limited(limiter, key_func=lambda user_id: user_id)
        def handler(user_id):
            return f"ok for {user_id}"

        self.assertEqual(handler("alice"), "ok for alice")
        with self.assertRaises(RateLimitExceeded):
            handler("alice")
        self.assertEqual(handler("bob"), "ok for bob")  # separate key

    def test_exception_carries_the_key(self):
        clock = FakeClock()
        limiter = TokenBucketLimiter(capacity=0.0001, refill_rate=1, time_func=clock)

        @rate_limited(limiter, key_func=lambda user_id: user_id)
        def handler(user_id):
            return "ok"

        with self.assertRaises(RateLimitExceeded) as ctx:
            handler("alice")
        self.assertEqual(ctx.exception.key, "alice")


if __name__ == "__main__":
    unittest.main()
