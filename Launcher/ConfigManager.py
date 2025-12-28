from pathlib import Path
from AppConfigurator import AppSettings


class ConfigManager:
    APP_FOLDER_PATH: Path = AppSettings.app_folder_path()
    CONFIG_PATH: Path = APP_FOLDER_PATH / "Configs" / "config.txt"


    @staticmethod
    def create_appdata_structure() -> bool:
        try:
            (ConfigManager.APP_FOLDER_PATH / "Configs").mkdir(parents=True, exist_ok=True)
            (ConfigManager.APP_FOLDER_PATH / "logs").mkdir(parents=True, exist_ok=True)
            return True
        except Exception:
            return False

    @staticmethod
    def save_config(language: str, theme: str, terms_accepted: bool) -> bool:
        try:
            ConfigManager.CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(ConfigManager.CONFIG_PATH, "w", encoding="utf-8") as f:
                f.write(f"language={language}\n")
                f.write(f"theme={theme}\n")
                f.write(f"terms_accepted={terms_accepted}\n")
            return True
        except Exception:
            return False

    @staticmethod
    def load_config():
        default_config = {
            "language": "English",
            "theme": "light",
            "terms_accepted": False
        }

        if not ConfigManager.CONFIG_PATH.exists():
            return default_config

        try:
            config = {}
            with open(ConfigManager.CONFIG_PATH, "r", encoding="utf-8") as f:
                for line in f:
                    if "=" in line.strip():
                        key, value = line.strip().split("=", 1)
                        config[key] = value

            return {
                "language": config.get("language", "English"),
                "theme": config.get("theme", "light"),
                "terms_accepted": config.get("terms_accepted", "False") == "True"
            }
        except Exception:
            return default_config

