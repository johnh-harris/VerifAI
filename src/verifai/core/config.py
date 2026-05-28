from dataclasses import dataclass, field
from pathlib import Path


APP_DIR = Path.home() / ".verifai"


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
