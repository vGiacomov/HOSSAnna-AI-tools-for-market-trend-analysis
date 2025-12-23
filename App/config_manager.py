import os
from pathlib import Path


class ConfigManager:
    @staticmethod
    def get_config_path():
        appdata_path = os.getenv('APPDATA')
        if not appdata_path:
            return None
        return Path(appdata_path) / 'GPCtools' / 'Configs' / 'config.txt'

    @staticmethod
    def create_appdata_structure():
        appdata_path = os.getenv('APPDATA')
        if not appdata_path:
            return False
        base_path = Path(appdata_path) / 'GPCtools'
        configs_path = base_path / 'Configs'
        logs_path = base_path / 'logs'
        try:
            configs_path.mkdir(parents=True, exist_ok=True)
            logs_path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception:
            return False

    @staticmethod
    def load_config():
        config_path = ConfigManager.get_config_path()
        if not config_path or not config_path.exists():
            return {
                "language": "English",
                "theme": "light",
                "terms_accepted": False
            }

        config = {}
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if '=' in line:
                        key, value = line.split('=', 1)
                        config[key] = value

            return {
                "language": config.get("language", "English"),
                "theme": config.get("theme", "light"),
                "terms_accepted": config.get("terms_accepted", "False") == "True"
            }
        except Exception:
            return {
                "language": "English",
                "theme": "light",
                "terms_accepted": False
            }

    @staticmethod
    def save_config(language, theme, terms_accepted=None):
        ConfigManager.create_appdata_structure()
        config_path = ConfigManager.get_config_path()
        if not config_path:
            return False

        # Load existing config to preserve terms_accepted if not provided
        if terms_accepted is None:
            existing = ConfigManager.load_config()
            terms_accepted = existing.get("terms_accepted", False)

        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                f.write(f"language={language}\n")
                f.write(f"theme={theme}\n")
                f.write(f"terms_accepted={terms_accepted}\n")
            return True
        except Exception:
            return False
