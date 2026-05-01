import subprocess
import time
from dataclasses import dataclass
from typing import Optional, Tuple, List


@dataclass
class HotspotConfig:
    ssid: str = "PyHotspot"
    password: str = "mypassword"
    band: str = "bg"                                 
    interface: str = "wlan0"
    connection_name: str = "PyHotspot"


class HotspotManager:

    CONNECTION_NAME = "PyHotspot"

    def __init__(self):
        self.config = HotspotConfig()
        self._active_interface: Optional[str] = None

                                                                             

    def _run(self, cmd: List[str], timeout: int = 30) -> Tuple[int, str, str]:
        try:
            r = subprocess.run(
                cmd, capture_output=True, text=True, timeout=timeout
            )
            return r.returncode, r.stdout.strip(), r.stderr.strip()
        except subprocess.TimeoutExpired:
            return 1, "", "Таймаут команды"
        except FileNotFoundError as e:
            return 1, "", f"Команда не найдена: {e}"

    def _run_sudo(self, cmd: List[str], timeout: int = 30) -> Tuple[int, str, str]:
 
                                               
        full_cmd = ["sudo", "-n"] + cmd
        code, out, err = self._run(full_cmd, timeout)
        
                                                             
                                                         
        if code != 0 and ("password" in err.lower() or "not allowed" in err.lower() or "not permitted" in err.lower()):
            code, out, err = self._run(["pkexec"] + cmd, timeout)
            
        return code, out, err

                                                                            

    def check_nm_running(self) -> Tuple[bool, str]:
        code, out, _ = self._run(["systemctl", "is-active", "NetworkManager"])
        if out.strip() == "active":
            return True, "NetworkManager активен"
        return False, (
            "NetworkManager не запущен.\n"
            "Запустите: sudo systemctl start NetworkManager"
        )

    def check_rfkill(self) -> Tuple[bool, str]:

        code, out, err = self._run(["rfkill", "list", "wifi"])
        if not out:
            code, out, err = self._run(["rfkill", "list"])

        hard = "Hard blocked: yes" in out
        soft = "Soft blocked: yes" in out

        if hard:
            return True, (
                "WiFi заблокирован аппаратно (Hard block).\n"
                "Нажмите физическую кнопку WiFi на устройстве."
            )
        if soft:
            return True, "WiFi заблокирован программно (Soft block). Выполняется разблокировка…"
        return False, ""

    def unblock_rfkill(self) -> Tuple[bool, str]:
        code, out, err = self._run_sudo(["rfkill", "unblock", "wifi"])
        if code == 0:
            time.sleep(1)                                      
            return True, "WiFi разблокирован"
        return False, f"Не удалось разблокировать WiFi: {err}"

    def get_wifi_interfaces(self) -> List[str]:
        code, out, err = self._run(
            ["nmcli", "-t", "-f", "DEVICE,TYPE", "device"]
        )
        ifaces = []
        for line in out.splitlines():
            parts = line.split(":")
            if len(parts) >= 2 and parts[1].strip() == "wifi":
                ifaces.append(parts[0].strip())
        return ifaces if ifaces else ["wlan0"]

                                                                            

    def is_active(self) -> bool:
        code, out, _ = self._run([
            "nmcli", "-t", "-f", "NAME,TYPE,STATE",
            "connection", "show", "--active"
        ])
        for line in out.splitlines():
            parts = line.split(":")
            if len(parts) >= 3 and self.CONNECTION_NAME in parts[0]:
                return parts[-1].strip() == "activated"
        return False

    def get_active_interface(self) -> str:
        code, out, _ = self._run(
            ["nmcli", "-t", "-f", "DEVICE,CONNECTION", "device"]
        )
        for line in out.splitlines():
            parts = line.split(":")
            if len(parts) >= 2 and self.CONNECTION_NAME in parts[1]:
                return parts[0].strip()
        return self._active_interface or self.config.interface

    def get_hotspot_ip(self) -> Optional[str]:
        iface = self.get_active_interface()
        code, out, _ = self._run(
            ["ip", "-4", "-o", "addr", "show", iface]
        )
        if out:
                                                           
            parts = out.split()
            for i, p in enumerate(parts):
                if p == "inet" and i + 1 < len(parts):
                    return parts[i + 1].split("/")[0]
        return None

    def get_all_interfaces(self) -> List[str]:
        code, out, _ = self._run(["nmcli", "-t", "-f", "DEVICE,TYPE", "device"])
        ifaces = []
        for line in out.splitlines():
            parts = line.split(":")
            if len(parts) >= 1:
                name = parts[0].strip()
                if name != "lo":                   
                    ifaces.append(name)
        return ifaces if ifaces else ["eth0", "wlo1"]

                                                                            
    def _enable_ip_forwarding(self) -> bool:
        try:
                                   
            self._run_sudo(["sysctl", "-w", "net.ipv4.ip_forward=1"])
            return True
        except:
            return False
    def start(
        self,
        ssid: str,
        password: str,
        band: str,
        interface: str,
    ) -> Tuple[bool, str]:
        self._enable_ip_forwarding()
                           
        nm_ok, nm_msg = self.check_nm_running()
        if not nm_ok:
            return False, nm_msg

                   
        blocked, rfkill_msg = self.check_rfkill()
        if blocked:
            if "Soft block" in rfkill_msg:
                ok, msg = self.unblock_rfkill()
                if not ok:
                    return False, msg
            else:
                return False, rfkill_msg
        
        self._run_sudo(["nmcli", "device", "disconnect", interface])
                                
        self._run_sudo(["nmcli", "connection", "delete", self.CONNECTION_NAME])
                                   
        self._run_sudo(["nmcli", "connection", "delete", self.CONNECTION_NAME])

                             
        cmd = [
            "nmcli", "device", "wifi", "hotspot",
            "ifname", interface,
            "ssid", ssid,
            "password", password,
            "band", band,
            "con-name", self.CONNECTION_NAME
        ]
        code, out, err = self._run_sudo(cmd, timeout=45)

        if code == 0:
            self._active_interface = interface
            self.config.ssid = ssid
            self.config.password = password
            self.config.band = band
            self.config.interface = interface
            self._run_sudo(["nmcli", "connection", "modify", self.CONNECTION_NAME, 
                            "ipv4.method", "shared", 
                            "ipv6.method", "ignore"])
                                                            
            self._run_sudo(["nmcli", "connection", "up", self.CONNECTION_NAME])
            return True, f"Хот-спот «{ssid}» запущен на {interface}"

                          
        raw = (err or out).lower()
        if "device not found" in raw or "no device found" in raw:
            msg = f"Интерфейс «{interface}» не найден"
        elif "ap mode" in raw or "access point" in raw or "не поддерживает" in raw:
            msg = f"«{interface}» не поддерживает режим точки доступа"
        elif "wpa_supplicant" in raw:
            msg = ("Ошибка wpa_supplicant.\n"
                   "Попробуйте: sudo systemctl restart wpa_supplicant")
        elif "permission" in raw or "not authorized" in raw or "pkexec" in raw:
            msg = ("Нет прав. Настройте sudoers:\n"
                   "sudo cp sudoers.d/pyhotspot /etc/sudoers.d/")
        elif "already" in raw:
            msg = "Хот-спот уже запущен"
        else:
            msg = err or out or "Неизвестная ошибка nmcli"

        return False, msg

    def stop(self) -> Tuple[bool, str]:
        code, out, err = self._run_sudo([
            "nmcli", "connection", "down", self.CONNECTION_NAME
        ])
        if code == 0:
            return True, "Хот-спот остановлен"
        return False, err or "Не удалось остановить хот-спот"

    def delete_connection(self) -> Tuple[bool, str]:
        code, _, err = self._run_sudo([
            "nmcli", "connection", "delete", self.CONNECTION_NAME
        ])
        return code == 0, err