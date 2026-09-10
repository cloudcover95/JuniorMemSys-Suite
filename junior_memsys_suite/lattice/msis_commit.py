"""Toy Module-SIS-style commitment over ternary z.

NOT a SNARK, NOT Jolt, NOT NIST ML-DSA. Small q for local integrity only.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass

Q = 8380417  # Dilithium-ish modulus, used here as a field only
N = 16
M = 32


def _mat(seed: bytes) -> list[list[int]]:
    rows: list[list[int]] = []
    h = seed
    for _ in range(N):
        row = []
        for _j in range(M):
            h = hashlib.sha256(h).digest()
            row.append(int.from_bytes(h[:4], "big") % Q)
        rows.append(row)
    return rows


def _clamp3(xs: list[int]) -> list[int]:
    out = []
    for x in xs[:M]:
        if x > 0:
            out.append(1)
        elif x < 0:
            out.append(-1)
        else:
            out.append(0)
    while len(out) < M:
        out.append(0)
    return out


@dataclass(frozen=True)
class Commit:
    seed: bytes
    c: tuple[int, ...]


def commit(z: list[int], seed: bytes = b"junior-msis-v0") -> Commit:
    A = _mat(seed)
    zz = _clamp3(z)
    c = []
    for row in A:
        s = sum(a * x for a, x in zip(row, zz)) % Q
        c.append(s)
    return Commit(seed, tuple(c))


def verify(z: list[int], com: Commit) -> bool:
    return commit(z, com.seed).c == com.c
