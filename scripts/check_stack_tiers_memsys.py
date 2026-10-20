#!/usr/bin/env python3
"""Offline stack-tier and close-rule self-check for JuniorMemSys-Suite.

Additive Inference Core slice (JuniorCloud LLC). Stdlib only: no network,
no sockets, no model pull, no GGUF, no bench, no LUT.

Layer stack (mirrors JuniorLLM junior_osai/kernels/stack.py and
JuniorHome docs/LAYER_STACK.md):
  T0  Python trit        for n < 512*512
  T1  bit-plane numpy    for n < 1024*1024
  T2  native C when the .so exists, otherwise falls back to T1
Weights are trit-packed before the layer pick (BitNet-mlx
src/bitnet_mlx/core/trit_pack_front.py).

Trit pack: rate 0.05, close rule sha256(prev || pack || text)[:16].
Not a quant file; ports touched: none.

Run: python3 scripts/check_stack_tiers_memsys.py
"""
from __future__ import annotations

import hashlib
import os
import sys

RATE = 0.05
T0_MAX = 512 * 512
T1_MAX = 1024 * 1024
HOST = "127.0.0.1"
FLAGS = {"mint": False, "socket": False, "layer_one": False,
         "fetch": False, "ue5_launch": False}


def trit_pack(weights):
    """Absmean ternary quantization to {-1, 0, 1}, packed 5 trits per byte."""
    if not weights:
        return b""
    scale = sum(abs(w) for w in weights) / len(weights) or 1.0
    trits = []
    for w in weights:
        q = round(w / scale)
        trits.append(-1 if q < -1 else (1 if q > 1 else int(q)))
    out = bytearray()
    for i in range(0, len(trits), 5):
        v = 0
        for t in reversed(trits[i:i + 5]):
            v = v * 3 + (t + 1)
        out.append(v)
    return bytes(out)


def pick_tier(n, so_path=None):
    if n < T0_MAX:
        return "T0"
    if n < T1_MAX:
        return "T1"
    if so_path and os.path.exists(so_path):
        return "T2"
    return "T1"


def close(prev: bytes, pack: bytes, text: str) -> str:
    return hashlib.sha256(prev + pack + text.encode("utf-8")).hexdigest()[:16]


def close_alt(prev: bytes, pack: bytes, text: str) -> str:
    h = hashlib.sha256()
    h.update(prev)
    h.update(pack)
    h.update(text.encode("utf-8"))
    return h.hexdigest()[:16]


def main() -> int:
    errors = []
    weights = [((i * 37) % 11 - 5) / 5.0 for i in range(64)]
    pack = trit_pack(weights)  # pack before the layer pick
    if len(pack) != 13:
        errors.append(f"pack length {len(pack)} != 13")
    tier = pick_tier(len(weights))
    cases = [(0, "T0"), (T0_MAX - 1, "T0"), (T0_MAX, "T1"),
             (T1_MAX - 1, "T1"), (T1_MAX, "T1")]
    for n, want in cases:
        got = pick_tier(n, so_path="/nonexistent/stack_native.so")
        if got != want:
            errors.append(f"pick_tier({n}) = {got}, want {want}")
    if pick_tier(T1_MAX, so_path=__file__) != "T2":
        errors.append("T2 not chosen when .so path exists")
    prev = b"\x00" * 16
    text = "memsys-inference-slice"
    c1, c2 = close(prev, pack, text), close_alt(prev, pack, text)
    if c1 != c2 or len(c1) != 16:
        errors.append("close-rule engines disagree")
    if RATE != 0.05:
        errors.append("rate drift")
    if any(FLAGS.values()):
        errors.append("a safety flag is not false")
    if HOST != "127.0.0.1":
        errors.append("host is not 127.0.0.1")
    if errors:
        for e in errors:
            print("FAIL:", e)
        return 1
    print(f"OK tier={tier} rate={RATE} close={c1}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
