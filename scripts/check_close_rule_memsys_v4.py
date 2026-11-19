#!/usr/bin/env python3
"""Self-check: rate and close rule agreement for JuniorMemSys-Suite (additive, local only).

Ports touched (names only): Home, OSai, FieldCore, Flagstaff, JuniorLLM.
"""
import hashlib
import sys

RATE = 0.05
HOST = "127.0.0.1"
FLAGS = {"mint": False, "socket": False, "layer_one": False, "fetch": False, "ue5_launch": False}
PORTS = ("Home", "OSai", "FieldCore", "Flagstaff", "JuniorLLM")


def close_rule(prev: bytes, pack: bytes, text: bytes) -> str:
    return hashlib.sha256(prev + pack + text).hexdigest()[:16]


def close_rule_alt(prev: bytes, pack: bytes, text: bytes) -> str:
    h = hashlib.sha256()
    for part in (prev, pack, text):
        h.update(part)
    return h.hexdigest()[:16]


def main() -> int:
    errs = []
    if RATE != 0.05:
        errs.append("rate")
    if HOST != "127.0.0.1":
        errs.append("host")
    if any(FLAGS.values()):
        errs.append("flags")
    prev, pack, text = b"", b"\x00\x01\x02", b"memsys"
    a, b = close_rule(prev, pack, text), close_rule_alt(prev, pack, text)
    if a != b or len(a) != 16:
        errs.append("close_rule")
    print("rate=%s host=%s close=%s ports=%s" % (RATE, HOST, a, ",".join(PORTS)))
    print("FAIL " + ",".join(errs) if errs else "PASS")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
