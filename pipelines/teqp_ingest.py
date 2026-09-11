"""Ingest JuniorTeqp public rows into this suite's audit style.
Does not store z. Prefers JuniorLLM home_sync pieces.
"""
from __future__ import annotations

import json
from pathlib import Path


def ingest(dest: Path) -> dict:
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    try:
        from junior_bitnet.ledger import append
        from junior_bitnet.vault import write_vault

        note = write_vault(dest)
        led = append(dest / "JuniorTeqp" / "observations.jsonl")
        return {"ok": True, "note": str(note), "ledger": str(led)}
    except Exception as exc:
        stub = dest / "JuniorTeqp" / "ATTACH_JUNIORLLM.md"
        stub.parent.mkdir(parents=True, exist_ok=True)
        stub.write_text("Need JuniorLLM on PYTHONPATH.\n", encoding="utf-8")
        return {"ok": False, "error": str(exc)}


if __name__ == "__main__":
    print(json.dumps(ingest(Path("/tmp/memsys_teqp")), indent=2))
