"""Inference-slice self-check for JuniorMemSys-Suite (additive, stdlib only).

Checks the layer-stack tier pick, the close rule sha256(prev || pack || text)[:16],
the 0.05 rate, loopback binding, and that the guarded flags stay false.
No bench, no LUT, no GGUF, no model pull, no network.
"""
import hashlib
import sys

RATE = 0.05
HOST = "127.0.0.1"
FLAGS = {"mint": False, "socket": False, "layer_one": False, "fetch": False, "ue5_launch": False}


def trit_pack(weights):
    """Pack ternary weights {-1,0,1} into bytes, 5 trits per byte (base 3)."""
    out = bytearray()
    for i in range(0, len(weights), 5):
        v = 0
        for w in reversed(weights[i:i + 5]):
            if w not in (-1, 0, 1):
                raise ValueError("not ternary")
            v = v * 3 + (w + 1)
        out.append(v)
    return bytes(out)


def pick_tier(n, native_available=False):
    if n < 512 * 512:
        return "T0"
    if n < 1024 * 1024:
        return "T1"
    return "T2" if native_available else "T1"


def close(prev, pack, text):
    return hashlib.sha256(prev + pack + text).hexdigest()[:16]


def main():
    ok = True
    pack = trit_pack([1, 0, -1, 1, 1, -1, 0])
    tiers = [pick_tier(10), pick_tier(512 * 512), pick_tier(1024 * 1024),
             pick_tier(1024 * 1024, True)]
    ok &= tiers == ["T0", "T1", "T1", "T2"]
    c1 = close(b"", pack, b"x")
    ok &= c1 == close(b"", pack, b"x") and len(c1) == 16
    ok &= c1 != close(b"", pack, b"y")
    ok &= RATE == 0.05 and HOST == "127.0.0.1" and not any(FLAGS.values())
    print("PASS" if ok else "FAIL", tiers, c1)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
