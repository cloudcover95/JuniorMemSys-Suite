# junior-memsys-suite/junior_memsys_suite/core/tda_mesh.py
import numpy as np
from junior_memsys_suite.core.omni_math import SovereignOmniKernel
from junior_memsys_suite.config import settings
import pyarrow as pa
import pyarrow.parquet as pq

class TDAMemoryMesh:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.kernel = SovereignOmniKernel(settings.variance_retention, settings.h_bar_mkt)
        self.capacity = 10000
        self.dim = settings.embedding_dim
        
        self.mesh_tensors = np.zeros((self.capacity, self.dim), dtype=np.float32)
        self.mesh_signatures = np.zeros((self.capacity, self.dim), dtype=np.int8)
        self.head_pointer = 0

    def _quantize_signature(self, x: np.ndarray) -> np.ndarray:
        return np.where(x > 0, 1, -1).astype(np.int8)

    def femtosecond_encode(self, signal_tensor: np.ndarray, z_score: float, delta: float, base_vol: float):
        q_marks = self.kernel.calculate_quantum_matrix(
            np.array([z_score]), np.array([delta]), np.array([base_vol])
        )
        
        if q_marks[0] < settings.etch_threshold:
            return False, q_marks[0]

        signal_t = signal_tensor.reshape(1, self.dim).T
        q, r = np.linalg.qr(signal_t)
        projected_state = (q @ r).flatten()
        signature = self._quantize_signature(projected_state)
        
        idx = self.head_pointer % self.capacity
        self.mesh_tensors[idx] = projected_state
        self.mesh_signatures[idx] = signature
        self.head_pointer += 1
        return True, q_marks[0]

    def compute_bit_drift(self, query_tensor: np.ndarray, threshold: float = 0.15) -> np.ndarray:
        query_sig = self._quantize_signature(query_tensor.flatten())
        active_nodes = min(self.head_pointer, self.capacity)
        
        if active_nodes == 0:
            return np.array([])
            
        active_signatures = self.mesh_signatures[:active_nodes]
        disagreement_matrix = np.abs(active_signatures - query_sig) / 2
        drift_scores = np.mean(disagreement_matrix, axis=1)
        
        valid_indices = np.where(drift_scores < threshold)[0]
        return valid_indices