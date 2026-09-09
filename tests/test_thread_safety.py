"""
Proves the thread-safety claim rather than assuming it: fires many
threads at a token bucket with real time.monotonic (not the fake
clock, since this test cares about actual concurrent execution) and
asserts the total number of successful allow() calls never exceeds
capacity — which would only be possible if the lock had a race.
"""

import os
import sys
import threading
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ratelimiter import TokenBucketLimiter


class TestThreadSafety(unittest.TestCase):
    def test_concurrent_calls_never_exceed_capacity(self):
        capacity = 50
        # refill_rate effectively 0 for the test's duration so only
        # the initial capacity can be consumed — isolates the assertion
        # to "did the lock prevent double-spending tokens".
        limiter = TokenBucketLimiter(capacity=capacity, refill_rate=0.0001)

        successes = []
        lock = threading.Lock()

        def worker():
            if limiter.allow("shared-key"):
                with lock:
                    successes.append(1)

        threads = [threading.Thread(target=worker) for _ in range(500)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertLessEqual(sum(successes), capacity)
        self.assertGreater(sum(successes), 0)


if __name__ == "__main__":
    unittest.main()
