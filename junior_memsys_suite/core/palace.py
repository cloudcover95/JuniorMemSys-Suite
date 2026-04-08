# junior_memsys_suite/core/palace.py
import json
import time
from pathlib import Path
from typing import Dict, List, Optional
from pydantic import BaseModel
from junior_memsys_suite.config import settings
from junior_memsys_suite.core.tda_mesh import TDAMemoryMesh
import numpy as np

class MemoryObject(BaseModel):
    content: str
    metadata: Dict[str, str]
    q_mark: float
    timestamp: float

class MemoryPalace:
    def __init__(self):
        self.root = settings.storage_path
        self.root.mkdir(parents=True, exist_ok=True)
        self.meshes: Dict[str, TDAMemoryMesh] = {}

    def _get_path(self, wing: str, hall: str, room: str) -> Path:
        p = self.root / wing / hall / room
        p.mkdir(parents=True, exist_ok=True)
        return p

    def get_mesh(self, wing: str) -> TDAMemoryMesh:
        if wing not in self.meshes:
            self.meshes[wing] = TDAMemoryMesh(node_id=f"node-{wing}")
        return self.meshes[wing]

    def store(self, wing: str, hall: str, room: str, content: str, z_score: float = 1.5):
        mesh = self.get_mesh(wing)
        synthetic_tensor = np.random.normal(size=(1, settings.embedding_dim))
        
        success, q_mark = mesh.femtosecond_encode(synthetic_tensor, z_score, delta=0.5, base_vol=0.1)
        
        if success:
            path = self._get_path(wing, hall, room) / "drawers.jsonl"
            mem_obj = MemoryObject(
                content=content,
                metadata={"wing": wing, "hall": hall, "room": room},
                q_mark=float(q_mark),
                timestamp=time.time()
            )
            with open(path, "a") as f:
                f.write(mem_obj.model_dump_json() + "\n")
            return True
        return False

    def semantic_search(self, query: str, wing: Optional[str] = None) -> List[Dict]:
        results = []
        target_wings = [wing] if wing else [w.name for w in self.root.iterdir() if w.is_dir()]
        
        query_tensor = np.random.normal(size=(1, settings.embedding_dim))
        
        for w in target_wings:
            mesh = self.get_mesh(w)
            valid_indices = mesh.compute_bit_drift(query_tensor, threshold=0.30)
            
            if len(valid_indices) > 0:
                wing_path = self.root / w
                if not wing_path.exists(): continue
                for hall in wing_path.iterdir():
                    if not hall.is_dir(): continue
                    for room in hall.iterdir():
                        if not room.is_dir(): continue
                        drawer_file = room / "drawers.jsonl"
                        if drawer_file.exists():
                            with open(drawer_file, "r") as f:
                                for line in f:
                                    results.append(json.loads(line))
        return results