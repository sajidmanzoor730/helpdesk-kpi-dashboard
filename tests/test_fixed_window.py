import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ratelimiter import FixedWindowLimiter
from helpers import FakeClock


class TestFixedWindow(unittest.TestCase):
    def test_allows_up_to_max_requests_per_window(self):
        clock = FakeClock()
        limiter = FixedWindowLimiter(max_requests=2, window_seconds=10, time_func=clock)
        self.assertTrue(limiter.allow("a"))
        self.assertTrue(limiter.allow("a"))
        self.assertFalse(limiter.allow("a"))

    def test_counter_resets_on_new_window(self):
        clock = FakeClock()
        limiter = FixedWindowLimiter(max_requests=1, window_seconds=10, time_func=clock)
        self.assertTrue(limiter.allow("a"))
        clock.advance(10.0)  # into the next window
        self.assertTrue(limiter.allow("a"))

    def test_documents_the_known_boundary_burst_flaw(self):
        """This is the tradeoff documented in fixed_window.py: up to
        2x max_requests can pass in a short span straddling a window
        boundary. This test proves it happens rather than assuming it,
        so the README's claim about it is backed by a real test."""
        clock = FakeClock(start=9.99)  # 0.01s before window boundary at t=10
        limiter = FixedWindowLimiter(max_requests=2, window_seconds=10, time_func=clock)
        self.assertTrue(limiter.allow("a"))
        self.assertTrue(limiter.allow("a"))  # 2 calls just before t=10

        clock.advance(0.02)  # now at t=10.01, new window
        self.assertTrue(limiter.allow("a"))
        self.assertTrue(limiter.allow("a"))  # 2 more calls just after

        # 4 calls happened within ~0.02s of real time — double the
        # intended rate of 2 per 10s. This is expected/documented
        # behavior for this algorithm, not a bug in this test.

    def test_reset_single_key(self):
        clock = FakeClock()
        limiter = FixedWindowLimiter(max_requests=1, window_seconds=10, time_func=clock)
        limiter.allow("a")
        limiter.reset("a")
        self.assertTrue(limiter.allow("a"))


if __name__ == "__main__":
    unittest.main()
