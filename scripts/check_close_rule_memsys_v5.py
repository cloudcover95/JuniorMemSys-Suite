#!/usr/bin/env python3
"""Offline self-check: trit rate 0.05 and close rule sha256(prev||pack||text)[:16].
Stdlib only. No network, no model pull, no sockets. Flags: mint, socket, layer_one, fetch, ue5_launch all False.
Ports touched: none (check only); engines compared: two independent close-rule implementations.
"""
import hashlib, random, sys

RATE = 0.05
FLAGS = {"mint": False, "socket": False, "layer_one": False, "fetch": False, "ue5_launch": False}
HOST = "127.0.0.1"


def close_a(prev: bytes, pack: bytes, text: bytes) -> str:
    return hashlib.sha256(prev + pack + text).hexdigest()[:16]


def close_b(prev: bytes, pack: bytes, text: bytes) -> str:
    h = hashlib.sha256()
    for part in (prev, pack, text):
        h.update(part)
    return h.digest().hex()[:16]


def trit_pack(vals, rate=RATE):
    """Quantize floats to {-1,0,1} with threshold = rate; pack as bytes (value+1)."""
    return bytes((0 if v < -rate else 2 if v > rate else 1) for v in vals)


def main() -> int:
    rng = random.Random(24)
    prev = b"\x00" * 8
    for i in range(500):
        vals = [rng.uniform(-1, 1) for _ in range(rng.randint(1, 64))]
        pack = trit_pack(vals)
        text = ("case-%d" % i).encode()
        a, b = close_a(prev, pack, text), close_b(prev, pack, text)
        assert a == b and len(a) == 16, (i, a, b)
        prev = bytes.fromhex(a)
    assert RATE == 0.05 and not any(FLAGS.values()) and HOST == "127.0.0.1"
    print("OK rate=0.05 close=sha256(prev||pack||text)[:16] cases=500 tail=" + prev.hex())
    return 0


if __name__ == "__main__":
    sys.exit(main())
