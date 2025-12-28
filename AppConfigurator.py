import os
from pathlib import Path
from typing import FrozenSet

class InitialSettings:
    isAdmin = False
    isConfig = False
    isNetwork = False

    @classmethod
    def set_admin_value(cls, value: bool):
        cls.isAdmin = value

    @classmethod
    def set_first_start_value(cls, value: bool):
        cls.isConfig = value

    @classmethod
    def set_network_value(cls, value: bool):
        cls.isNetwork = value




class AppSettings:
    appName: str = "HOSSAnna"
    languages: FrozenSet[str] = frozenset({
        "English",
        "Polski",
        "Français",
        "Deutsch",
        "Español",
        "Italiano",
        "עברית",
    })

    @classmethod
    def app_folder_path(cls) -> Path:
        base = Path(os.getenv("APPDATA", Path.home()))
        return base / cls.appName

    @classmethod
    def config_path(cls) -> Path:
        return cls.app_folder_path() / "Configs" / "config.txt"

