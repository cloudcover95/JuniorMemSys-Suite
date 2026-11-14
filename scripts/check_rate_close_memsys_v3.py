#!/usr/bin/env python3
"""Self-check: trit-pack rate 0.05 and close rule sha256(prev || pack || text)[:16].

Local only. Ports named: Home, OSai, FieldCore, Flagstaff, JuniorLLM.
Guards: mint/socket/layer_one/fetch/ue5_launch all false; bind 127.0.0.1 only.
No network, no model pull, no bench.
"""
import hashlib

RATE = 0.05
HOST = "127.0.0.1"
PORTS = ("Home", "OSai", "FieldCore", "Flagstaff", "JuniorLLM")
FLAGS = {"mint": False, "socket": False, "layer_one": False, "fetch": False, "ue5_launch": False}


def close(prev: bytes, pack: bytes, text: str) -> str:
    return hashlib.sha256(prev + pack + text.encode()).hexdigest()[:16]


def stack_tier(n: int) -> str:
    if n < 512 * 512:
        return "T0"
    if n < 1024 * 1024:
        return "T1"
    return "T2"


def main() -> int:
    a = close(b"", b"\x00\x01\x02", "hello")
    b = close(b"", b"\x00\x01\x02", "hello")
    c = close(b"x", b"\x00\x01\x02", "hello")
    ok = [
        len(a) == 16,
        a == b,
        a != c,
        RATE == 0.05,
        HOST == "127.0.0.1",
        not any(FLAGS.values()),
        stack_tier(1000) == "T0" and stack_tier(600000) == "T1" and stack_tier(2000000) == "T2",
    ]
    print("rate", RATE, "close", a, "ports", ",".join(PORTS))
    print("PASS" if all(ok) else "FAIL")
    return 0 if all(ok) else 1


if __name__ == "__main__":
    raise SystemExit(main())
