from dataclasses import dataclass, field
import os
from pathlib import Path
import keyring

APP_DIR = Path.home() / ".verifai"
_SERVICE = "verifai"
_KEY_NAME = "anthropic_api_key"

def get_api_key() -> str | None:
    return os.environ.get("ANTHROPIC_API_KEY") or keyring.get_password(_SERVICE, _KEY_NAME)

# TODO: check if key is valid
def set_api_key(key: str) -> None:
    keyring.set_password(_SERVICE, _KEY_NAME, key)

@dataclass
class Config:
    data_dir: Path = field(default_factory=lambda: APP_DIR)

    def ensure_dirs(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)


_config: Config | None = None


def get_config() -> Config:
    global _config
    if _config is None:
        _config = Config()
        _config.ensure_dirs()
    return _config
