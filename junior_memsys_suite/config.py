# junior-memsys-suite/junior_memsys_suite/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    storage_path: Path = Path.home() / ".jcllc_memsys" / "palace"
    variance_retention: float = 0.95
    h_bar_mkt: float = 0.01
    etch_threshold: float = 0.50
    embedding_dim: int = 512

    model_config = SettingsConfigDict(env_prefix="JCLLC_")

settings = Settings()