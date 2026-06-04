# path: src/hardware/backend_router.py

from enum import Enum

class Backend(Enum):
    MLX = "mlx"
    CUDA = "cuda"

class BackendRouter:
    def __init__(self):
        self._current = Backend.MLX

    def set_backend(self, backend: Backend):
        self._current = backend

    def get_current_backend(self):
        return self._current
