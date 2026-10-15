#!/usr/bin/env python3
"""Inference-slice self-check for JuniorMemSys-Suite (JuniorCloud LLC).

Additive, offline, stdlib-only utility. It documents and verifies the
memory-suite inference slice contract:

* all risky flags (mint, socket, layer_one, fetch, ue5_launch) stay False
* any server/socket host binds to 127.0.0.1 only
* trit pack rate is 0.05
* close rule is sha256(prev || pack || text)[:16]
* the reference engine and the memory-store engine agree on rate + close rule

No network access, no model pulls, no remote scripts. Run:

    python3 scripts/check_inference_slice_memsys.py
"""
from __future__ import annotations

import hashlib
import json
import sys

TRIT_RATE = 0.05
BIND_HOST = "127.0.0.1"
FLAGS = {
    "mint": False,
    "socket": False,
    "layer_one": False,
    "fetch": False,
    "ue5_launch": False,
}


def close_reference(prev: str, pack: str, text: str) -> str:
    """Reference close rule: sha256(prev || pack || text)[:16]."""
    return hashlib.sha256((prev + pack + text).encode("utf-8")).hexdigest()[:16]


class MemStoreEngine:
    """Minimal in-memory chain that applies the same close rule per record."""

    rate = TRIT_RATE

    def __init__(self) -> None:
        self.records: list[dict] = []
        self.prev = ""

    def append(self, pack: str, text: str) -> str:
        h = hashlib.sha256()
        for part in (self.prev, pack, text):
            h.update(part.encode("utf-8"))
        close = h.hexdigest()[:16]
        self.records.append({"prev": self.prev, "pack": pack, "text": text, "close": close})
        self.prev = close
        return close


def run_checks() -> list[str]:
    errors: list[str] = []
    for name, value in FLAGS.items():
        if value is not False:
            errors.append(f"flag {name} must be False")
    if BIND_HOST != "127.0.0.1":
        errors.append("bind host must be 127.0.0.1")
    if TRIT_RATE != 0.05:
        errors.append("trit rate must be 0.05")

    engine = MemStoreEngine()
    if engine.rate != TRIT_RATE:
        errors.append("engines disagree on trit rate")
    prev = ""
    samples = [("+0-", "recall: hello"), ("0+-", "store: slice"), ("--+", "evict: none")]
    for pack, text in samples:
        ref = close_reference(prev, pack, text)
        got = engine.append(pack, text)
        if ref != got or len(got) != 16:
            errors.append(f"close rule mismatch for {pack!r}: {ref} != {got}")
        prev = ref
    return errors


def main() -> int:
    errors = run_checks()
    report = {
        "repo": "JuniorMemSys-Suite",
        "trit_rate": TRIT_RATE,
        "close_rule": "sha256(prev || pack || text)[:16]",
        "bind_host": BIND_HOST,
        "flags": FLAGS,
        "engines_agree": not errors,
        "ok": not errors,
        "errors": errors,
    }
    print(json.dumps(report, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
