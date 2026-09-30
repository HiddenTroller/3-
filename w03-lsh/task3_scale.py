#!/usr/bin/env python3
"""Week 3 · Task 3 — Find the same pairs without comparing everything.

Textbook §3.4.

`BruteForce` compares every pair. On 3,000 documents that is 4.5 million
comparisons and it is completely correct. On 3 million documents it is 4.5
trillion and it is completely useless.

Beat it. Find the same near-duplicate pairs while making far fewer comparisons.

    python3 bench.py
    python3 bench.py --yours

The harness counts every call you make to `similarity()`. That is your score.
It also checks **recall** - which of the truly similar pairs you found. Skipping
comparisons is easy; skipping comparisons without losing the pairs is the task.
"""


class BruteForce:
    """Correct, and quadratic."""

    def __init__(self, threshold):
        self.threshold = threshold

    def find(self, docs, similarity):
        """docs is [set_of_shingles, ...]. Return {(i, j), ...} with i < j."""
        out = set()
        for i in range(len(docs)):
            for j in range(i + 1, len(docs)):
                if similarity(docs[i], docs[j]) >= self.threshold:
                    out.add((i, j))
        return out


import random


class YourFinder:
    """Your near-duplicate finder.

        __init__(threshold)
        find(docs, similarity) -> {(i, j), ...}

    `similarity(a, b)` is the only way to compare two documents, and every call
    is counted. Everything else - signatures, banding, bucketing - is free, in
    the sense that the harness does not charge you for it.
    """

    def __init__(self, threshold):
        self.threshold = threshold
        self.num_hashes = 128
        self.bands = 32
        self.rows_per_band = self.num_hashes // self.bands  # r = 4

        # Fixed seed so hashes are deterministic
        rng = random.Random(246)
        p = 1_000_003
        self.hashes = [
            (rng.randint(1, p - 1), rng.randint(0, p - 1), p)
            for _ in range(self.num_hashes)
        ]

    def find(self, docs, similarity):
        # 1. Compute minhash signatures for all documents
        sigs = []
        for doc in docs:
            if not doc:
                sigs.append([0] * self.num_hashes)
                continue
            doc_list = list(doc)
            sig = [min((a * x + b) % p for x in doc_list) for a, b, p in self.hashes]
            sigs.append(sig)

        # 2. LSH candidate generation via banding
        candidates = set()
        r = self.rows_per_band
        for b in range(self.bands):
            buckets = {}
            start = b * r
            end = start + r
            for doc_idx, sig in enumerate(sigs):
                key = tuple(sig[start:end])
                if key in buckets:
                    for prev in buckets[key]:
                        candidates.add((prev, doc_idx))
                    buckets[key].append(doc_idx)
                else:
                    buckets[key] = [doc_idx]

        # 3. Filter candidates using similarity()
        out = set()
        for i, j in candidates:
            if similarity(docs[i], docs[j]) >= self.threshold:
                out.add((i, j))

        return out
