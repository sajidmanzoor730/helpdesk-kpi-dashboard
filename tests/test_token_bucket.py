import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ratelimiter import TokenBucketLimiter
from helpers import FakeClock


class TestTokenBucket(unittest.TestCase):
    def test_allows_up_to_capacity_burst(self):
        clock = FakeClock()
        limiter = TokenBucketLimiter(capacity=3, refill_rate=1, time_func=clock)
        self.assertTrue(limiter.allow("a"))
        self.assertTrue(limiter.allow("a"))
        self.assertTrue(limiter.allow("a"))
        self.assertFalse(limiter.allow("a"))  # 4th call, bucket empty

    def test_refills_over_time(self):
        clock = FakeClock()
        limiter = TokenBucketLimiter(capacity=2, refill_rate=1, time_func=clock)
        self.assertTrue(limiter.allow("a"))
        self.assertTrue(limiter.allow("a"))
        self.assertFalse(limiter.allow("a"))

        clock.advance(1.0)  # 1 token refills
        self.assertTrue(limiter.allow("a"))
        self.assertFalse(limiter.allow("a"))

    def test_refill_never_exceeds_capacity(self):
        clock = FakeClock()
        limiter = TokenBucketLimiter(capacity=2, refill_rate=1, time_func=clock)
        clock.advance(100.0)  # would overfill without the cap
        self.assertAlmostEqual(limiter.tokens_remaining("a"), 2)

    def test_keys_are_independent(self):
        clock = FakeClock()
        limiter = TokenBucketLimiter(capacity=1, refill_rate=1, time_func=clock)
        self.assertTrue(limiter.allow("user-a"))
        self.assertFalse(limiter.allow("user-a"))
        self.assertTrue(limiter.allow("user-b"))  # separate bucket

    def test_reset_single_key(self):
        clock = FakeClock()
        limiter = TokenBucketLimiter(capacity=1, refill_rate=1, time_func=clock)
        limiter.allow("a")
        self.assertFalse(limiter.allow("a"))
        limiter.reset("a")
        self.assertTrue(limiter.allow("a"))

    def test_invalid_construction_raises(self):
        with self.assertRaises(ValueError):
            TokenBucketLimiter(capacity=0, refill_rate=1)
        with self.assertRaises(ValueError):
            TokenBucketLimiter(capacity=1, refill_rate=0)


if __name__ == "__main__":
    unittest.main()
