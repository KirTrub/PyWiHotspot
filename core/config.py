import configparser
from pathlib import Path

CONFIG_DIR  = Path.home() / ".config" / "pyhotspot"
CONFIG_FILE = CONFIG_DIR / "config.ini"

DEFAULTS = {
    "ssid":      "PyHotspot",
    "password":  "mypassword123",
    "band":      "bg",
    "interface": "wlan0",
    "source":    "Авто",
}


class AppConfig:
    def __init__(self):
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        self._cfg = configparser.ConfigParser()
        self.load()

    def load(self):
        if CONFIG_FILE.exists():
            self._cfg.read(CONFIG_FILE, encoding="utf-8")
        if "hotspot" not in self._cfg:
            self._cfg["hotspot"] = DEFAULTS
            self.save()

    def save(self):
        """Сохранить конфиг на диск."""
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            self._cfg.write(f)


    def get(self, key: str) -> str:
        return self._cfg.get("hotspot", key, fallback=DEFAULTS.get(key, ""))

    def set(self, key: str, value: str):
        self._cfg["hotspot"][key] = value

    def set_many(self, **kwargs):
        for key, value in kwargs.items():
            self.set(key, value)
        self.save()


    @property
    def ssid(self)      -> str: return self.get("ssid")
    @property
    def password(self)  -> str: return self.get("password")
    @property
    def band(self)      -> str: return self.get("band")
    @property
    def interface(self) -> str: return self.get("interface")
    @property
    def source(self)    -> str: return self.get("source")