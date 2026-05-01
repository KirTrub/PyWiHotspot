import subprocess
from pathlib import Path
from typing import Tuple


class AutostartManager:
    SERVICE_NAME = "pyhotspot"
    SERVICE_PATH = Path(f"/etc/systemd/system/pyhotspot.service")

    def _run_sudo(self, cmd) -> Tuple[int, str, str]:
        r = subprocess.run(["sudo", "-n"] + cmd, capture_output=True, text=True)
        if r.returncode != 0 and "password" in r.stderr.lower():
            r = subprocess.run(["pkexec"] + cmd, capture_output=True, text=True)
        return r.returncode, r.stdout.strip(), r.stderr.strip()

    def is_enabled(self) -> bool:
        r = subprocess.run(
            ["systemctl", "is-enabled", self.SERVICE_NAME],
            capture_output=True, text=True
        )
        return r.stdout.strip() == "enabled"

    def enable(self, ssid: str, password: str, band: str, interface: str) -> Tuple[bool, str]:
        service_content = f"""[Unit]
Description=PyHotspot WiFi Access Point
After=NetworkManager.service network.target
Wants=NetworkManager.service

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStartPre=/bin/sleep 8
ExecStart=/usr/bin/nmcli device wifi hotspot \\
    ifname {interface} \\
    ssid "{ssid}" \\
    password "{password}" \\
    band {band} \\
    con-name PyHotspot
ExecStop=/usr/bin/nmcli connection down PyHotspot
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
"""
                               
        code, out, err = self._run_sudo(
            ["bash", "-c",
             f"cat > {self.SERVICE_PATH} << 'PYHOTSPOT_EOF'\n{service_content}\nPYHOTSPOT_EOF"]
        )
                                         
        r = subprocess.run(
            ["sudo", "-n", "tee", str(self.SERVICE_PATH)],
            input=service_content, capture_output=True, text=True
        )
        if r.returncode != 0:
            r = subprocess.run(
                ["pkexec", "tee", str(self.SERVICE_PATH)],
                input=service_content, capture_output=True, text=True
            )
        if r.returncode != 0:
            return False, f"Не удалось записать сервис: {r.stderr}"

                       
        self._run_sudo(["systemctl", "daemon-reload"])

                  
        code, out, err = self._run_sudo(
            ["systemctl", "enable", self.SERVICE_NAME]
        )
        if code != 0:
            return False, f"Не удалось включить сервис: {err}"

        return True, "Автозапуск включён ✓"

    def disable(self) -> Tuple[bool, str]:
        self._run_sudo(["systemctl", "disable", self.SERVICE_NAME])
        self._run_sudo(["rm", "-f", str(self.SERVICE_PATH)])
        self._run_sudo(["systemctl", "daemon-reload"])
        return True, "Автозапуск отключён"

    def get_status(self) -> str:
        r = subprocess.run(
            ["systemctl", "status", self.SERVICE_NAME],
            capture_output=True, text=True
        )
        return r.stdout