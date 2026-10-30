#!/usr/bin/env python3
"""Layer-pick self-check for JuniorMemSys-Suite (Inference Core lane, JuniorCloud LLC).

Additive, standalone, stdlib only. Mirrors the layer stack:
  T0 Python trit   for n < 512*512
  T1 bit-plane numpy for n < 1024*1024
  T2 native C when the .so exists, else falls back to T1
Weights are trit-packed before the layer pick. No bench, no LUT, no GGUF.
Ports touched (quant): Home, OSai, FieldCore, Flagstaff, JuniorLLM.
"""
import hashlib
import os
import sys

BIND_HOST = "127.0.0.1"
FLAGS = {"mint": False, "socket": False, "layer_one": False, "fetch": False, "ue5_launch": False}
RATE = 0.05
T0_MAX = 512 * 512
T1_MAX = 1024 * 1024
PORTS = ("Home", "OSai", "FieldCore", "Flagstaff", "JuniorLLM")


def trit_pack(weights):
    """Map floats to trits {-1,0,1} using threshold RATE, then pack 5 trits per byte."""
    trits = [0 if abs(w) < RATE else (1 if w > 0 else -1) for w in weights]
    out = bytearray()
    for i in range(0, len(trits), 5):
        v = 0
        for t in reversed(trits[i:i + 5]):
            v = v * 3 + (t + 1)
        out.append(v)
    return bytes(out), len(trits)


def close_rule(prev: bytes, pack: bytes, text: str) -> str:
    return hashlib.sha256(prev + pack + text.encode("utf-8")).hexdigest()[:16]


def pick_layer(n, so_path=None):
    if n < T0_MAX:
        return "T0"
    if n < T1_MAX:
        return "T1"
    if so_path and os.path.exists(so_path):
        return "T2"
    return "T1"


def self_check():
    errs = []
    if BIND_HOST != "127.0.0.1":
        errs.append("bind")
    if any(FLAGS.values()):
        errs.append("flags")
    if RATE != 0.05:
        errs.append("rate")
    cases = [(0, None, "T0"), (T0_MAX - 1, None, "T0"), (T0_MAX, None, "T1"),
             (T1_MAX - 1, None, "T1"), (T1_MAX, None, "T1"),
             (T1_MAX, "/nonexistent/kernel.so", "T1"), (T1_MAX, sys.executable, "T2")]
    for n, so, want in cases:
        got = pick_layer(n, so)
        if got != want:
            errs.append(f"pick({n},{so})={got}!={want}")
    pack, count = trit_pack([0.2, -0.3, 0.01, 0.0, 0.07, -0.04])
    if count != 6 or len(pack) != 2:
        errs.append("pack")
    a = close_rule(b"", pack, "memsys")
    b = close_rule(b"", pack, "memsys")
    if a != b or len(a) != 16:
        errs.append("close_rule")
    # engines agree: an independent recompute of the close rule must match
    if hashlib.sha256(b"" + pack + b"memsys").hexdigest()[:16] != a:
        errs.append("engine_agree")
    return errs


if __name__ == "__main__":
    e = self_check()
    print("ports:", ", ".join(PORTS))
    print("SELF-CHECK", "PASS" if not e else "FAIL " + ";".join(e))
    sys.exit(1 if e else 0)
