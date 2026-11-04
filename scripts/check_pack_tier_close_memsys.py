#!/usr/bin/env python3
"""Self-check: trit-pack before layer pick, stack tiers, close rule (JuniorMemSys-Suite).

Additive check only. Pure stdlib. No bench, no LUT, no GGUF, no network.
Layer stack: T0 Python trit (n < 512*512), T1 bit-plane numpy (n < 1024*1024),
T2 native C when the .so exists, falling back to T1.
"""
import hashlib
import os

RATE = 0.05
BIND = "127.0.0.1"
FLAGS = {"mint": False, "socket": False, "layer_one": False, "fetch": False, "ue5_launch": False}
PORTS = ("Home", "OSai", "FieldCore", "Flagstaff", "JuniorLLM")


def trit(x, thr=RATE):
    return 1 if x > thr else (-1 if x < -thr else 0)


def trit_pack(ws):
    out = bytearray()
    ts = [trit(w) + 1 for w in ws]
    for i in range(0, len(ts), 5):
        v = 0
        for t in reversed(ts[i:i + 5]):
            v = v * 3 + t
        out.append(v)
    return bytes(out)


def close(prev, pack, text):
    return hashlib.sha256(prev + pack + text.encode()).hexdigest()[:16]


def pick_layer(n, so_path=None):
    if n < 512 * 512:
        return "T0"
    if n < 1024 * 1024:
        return "T1"
    if so_path and os.path.exists(so_path):
        return "T2"
    return "T1"


def main():
    ws = [0.2, -0.3, 0.01, 0.0, -0.04, 0.06, -0.06]
    pack = trit_pack(ws)  # pack first, then pick
    assert [trit(w) for w in ws] == [1, -1, 0, 0, 0, 1, -1]
    assert len(pack) == 2
    assert pick_layer(10) == "T0"
    assert pick_layer(512 * 512) == "T1"
    assert pick_layer(1024 * 1024, "/nonexistent.so") == "T1"
    c1 = close(b"", pack, "memsys")
    c2 = close(c1.encode(), pack, "memsys")
    assert len(c1) == 16 and c1 != c2 and c1 == close(b"", pack, "memsys")
    assert all(v is False for v in FLAGS.values())
    assert BIND == "127.0.0.1"
    print("PASS rate=%s close=%s ports=%s" % (RATE, c1, ",".join(PORTS)))


if __name__ == "__main__":
    main()
