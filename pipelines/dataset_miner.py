# junior-memsys-suite/pipelines/dataset_miner.py
import json
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path
from junior_memsys_suite.core.palace import MemoryPalace

class DatasetMiner:
    def __init__(self):
        self.palace = MemoryPalace()

    def mine_conversations(self, jsonl_path: str | Path, wing: str = "conversations"):
        path = Path(jsonl_path)
        with open(path, "r") as f:
            for i, line in enumerate(f):
                data = json.loads(line)
                content = data.get("content") or str(data)
                self.palace.store(
                    wing=wing,
                    hall=data.get("session_id", "default"),
                    room=f"turn_{i}",
                    content=content,
                    z_score=1.8
                )
        print(f"[OK] Mined {i+1} conversation turns into manifold wing '{wing}'")

    def export_to_parquet(self, wing: str, output_path: str | Path):
        """Exports high-density topological TS data to Parquet."""
        target_wing = self.palace.root / wing
        if not target_wing.exists():
            print("[ERROR] Wing manifold non-existent.")
            return

        records = []
        for hall in target_wing.iterdir():
            if not hall.is_dir(): continue
            for room in hall.iterdir():
                if not room.is_dir(): continue
                drawer_file = room / "drawers.jsonl"
                if drawer_file.exists():
                    with open(drawer_file, "r") as f:
                        for line in f:
                            records.append(json.loads(line))
        
        if not records:
            return

        # Vectorize to PyArrow Table
        table = pa.Table.from_pylist(records)
        pq.write_table(table, output_path)
        print(f"[OK] Exported {len(records)} nodes to {output_path}")