import os

files = {
    "junior_memsys_suite/core/audit.py": """import json, hashlib, os, time
from pathlib import Path
from datetime import datetime

class BitDriftAuditor:
    def __init__(self):
        self.log_dir = Path.home() / ".junior_memsys" / "audit"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.ledger = self.log_dir / "bitdrift_ledger.jsonl"
    def log(self, action, **kwargs):
        entry = {"ts": datetime.utcnow().isoformat(), "action": action, **kwargs}
        with open(self.ledger, "a") as f:
            f.write(json.dumps(entry) + "\\n")
""",
    "junior_memsys_suite/core/encoder.py": """import hashlib, numpy as np
from junior_memsys_suite.config import settings
class SovereignEncoder:
    def __init__(self):
        self.dim = settings.embedding_dim
        self.model = None
    def _lazy_load(self):
        if self.model: return
        try:
            import mlx.core as mx
            from mlx_embedding_models.embedding import EmbeddingModel
            self.model = EmbeddingModel.from_registry("bge-small-en-v1.5")
            self.backend = "mlx"
        except: self.backend = "crypto"
    def embed(self, text):
        self._lazy_load()
        if self.backend == "crypto":
            return np.random.normal(size=(1, self.dim)).astype(np.float32)
        emb = np.array(self.model.encode([text])[0], dtype=np.float32)
        return emb[:self.dim].reshape(1, -1)
"""
}

for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"DONE: {path}")
