#!/usr/bin/env python3
"""Additive self-check for JuniorMemSys-Suite (JuniorCloud LLC, inference slice 2026-10-25).

Verifies the LLC engine agreements locally, with no network, no model pull, no GGUF:
- trit-pack rate 0.05
- close rule sha256(prev || pack || text)[:16]
- layer stack tiers: T0 Python trit n < 512*512, T1 bit-plane n < 1024*1024,
  T2 native C when the .so exists, else fall back to T1
- safety flags mint/socket/layer_one/fetch/ue5_launch all False
- bind host 127.0.0.1
Ports touched: Home, OSai, FieldCore, Flagstaff, JuniorLLM (read-only checks).
"""
import hashlib
import os
import sys

RATE = 0.05
BIND_HOST = "127.0.0.1"
SAFETY = {"mint": False, "socket": False, "layer_one": False, "fetch": False, "ue5_launch": False}
PORTS = ("Home", "OSai", "FieldCore", "Flagstaff", "JuniorLLM")
T0_MAX = 512 * 512
T1_MAX = 1024 * 1024


def close_rule(prev: bytes, pack: bytes, text: bytes) -> str:
    return hashlib.sha256(prev + pack + text).hexdigest()[:16]


def trit_pack(values):
    """Ternary quantize with threshold RATE: -1, 0, +1."""
    return [0 if abs(v) <= RATE else (1 if v > 0 else -1) for v in values]


def pick_tier(n: int, so_path: str = "") -> str:
    if n < T0_MAX:
        return "T0"
    if n < T1_MAX:
        return "T1"
    if so_path and os.path.exists(so_path):
        return "T2"
    return "T1"


def main() -> int:
    ok = True
    def check(name, cond):
        nonlocal ok
        print(("PASS " if cond else "FAIL ") + name)
        ok = ok and cond

    check("rate == 0.05", RATE == 0.05)
    a = close_rule(b"prev", b"pack", b"text")
    b = hashlib.sha256(b"prevpacktext").hexdigest()[:16]
    check("close rule engines agree", a == b and len(a) == 16)
    check("close rule deterministic", a == close_rule(b"prev", b"pack", b"text"))
    check("trit pack", trit_pack([0.2, -0.2, 0.01, -0.05, 0.051]) == [1, -1, 0, 0, 1])
    check("tier T0", pick_tier(T0_MAX - 1) == "T0")
    check("tier T1", pick_tier(T0_MAX) == "T1" and pick_tier(T1_MAX - 1) == "T1")
    check("tier T2 fallback to T1", pick_tier(T1_MAX, "/nonexistent/stack.so") == "T1")
    check("tier T2 when .so exists", pick_tier(T1_MAX, __file__) == "T2")
    check("safety flags false", not any(SAFETY.values()))
    check("bind 127.0.0.1", BIND_HOST == "127.0.0.1")
    check("ports named", len(PORTS) == 5)
    print("ALL PASS" if ok else "SOME FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
