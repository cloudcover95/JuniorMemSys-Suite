import numpy as np
import platform
import warnings
from junior_memsys_suite.config import settings

# -------------------------------------------------------------------------
# Dynamic Architecture Router: IP Protection Layer
# -------------------------------------------------------------------------
if platform.system() == "Darwin":
    # M4/M1 Local Node: Strict requirement for the compiled .so binary
    try:
        from junior_memsys_suite.core.omni_math import SovereignOmniKernel
    except ImportError:
        raise RuntimeError("CRITICAL: macOS detected but protected omni_math.so is missing. Execution halted to protect IP.")
else:
    # Replit / Linux VM: Standard Python fallback for dashboard prototyping
    try:
        from junior_memsys_suite.core.omni_math_fallback import SovereignOmniKernel
        warnings.warn("Replit/Linux edge node detected. Utilizing Python fallback kernel.", RuntimeWarning)
    except ImportError:
        raise RuntimeError("CRITICAL: omni_math_fallback.py missing on Linux node.")
# -------------------------------------------------------------------------

class TDAMemoryMesh:
    def __init__(self):
        self.kernel = SovereignOmniKernel(settings.variance_retention, settings.h_bar_mkt)
        self.capacity = 50000
        self.dim = settings.embedding_dim
        self.mesh_tensors = np.zeros((self.capacity, self.dim), dtype=np.float32)
        self.mesh_signatures = np.zeros((self.capacity, self.dim), dtype=np.int8)
        self.head_pointer = 0

    def _quantize(self, x):
        return np.where(x > 0, 1, -1).astype(np.int8)

    def femtosecond_encode(self, signal: np.ndarray, z_score: float = 1.8):
        # Implementation remains locked to your core logic
        q = self.kernel.calculate_quantum_matrix(np.array([z_score]), np.array([0.5]), np.array([0.1]))[0]
        if q < settings.etch_threshold:
            return False, q
        projected = np.linalg.qr(signal.reshape(1, -1).T)[0].flatten()
        sig = self._quantize(projected)
        idx = self.head_pointer % self.capacity
        self.mesh_tensors[idx] = projected
        self.mesh_signatures[idx] = sig
        self.head_pointer += 1
        return True, q

    def compute_bit_drift(self, query_tensor: np.ndarray, threshold: float = 0.15):
        query_sig = self._quantize(query_tensor.flatten())
        active_nodes = min(self.head_pointer, self.capacity)
        active = self.mesh_signatures[:active_nodes]
        if len(active) == 0:
            return np.array([])
        disagreement = np.mean(np.abs(active - query_sig) / 2, axis=1)
        return np.where(disagreement < threshold)[0]