import subprocess
import time
import socket
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple
from pathlib import Path


@dataclass
class ConnectedDevice:
    ip: str
    mac: str
    hostname: str = "—"
    vendor: str = ""
    rx_bytes: int = 0
    tx_bytes: int = 0


@dataclass
class TrafficStats:
    rx_bytes: int = 0
    tx_bytes: int = 0
    rx_speed: float = 0.0             
    tx_speed: float = 0.0
    history_rx: List[float] = field(default_factory=list)                       
    history_tx: List[float] = field(default_factory=list)
    HISTORY_LEN: int = 60                    


def _fmt_bytes(n: int) -> str:
    for unit in ("Б", "КБ", "МБ", "ГБ"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} ТБ"


def _fmt_speed(bps: float) -> str:
    if bps < 1024:
        return f"{bps:.0f} Б/с"
    elif bps < 1024 ** 2:
        return f"{bps/1024:.1f} КБ/с"
    else:
        return f"{bps/1024**2:.2f} МБ/с"


class NetworkMonitor:

    def __init__(self):
        self._prev: Dict[str, Tuple[int, int, float]] = {}                          
        self._stats_cache: Dict[str, TrafficStats] = {}

                                                                            

    def get_connected_devices(self, interface: str) -> List[ConnectedDevice]:

        devices = self._from_leases(interface)
        if not devices:
            devices = self._from_arp(interface)
        return devices

    def _from_leases(self, interface: str) -> List[ConnectedDevice]:
        devices = []
        lease_dir = Path("/var/lib/NetworkManager")
        patterns = [
            f"dnsmasq-{interface}.leases",
            "dnsmasq*.leases",
        ]
        lease_file = None
        for pattern in patterns:
            found = list(lease_dir.glob(pattern))
            if found:
                lease_file = found[0]
                break

        if not lease_file or not lease_file.exists():
            return devices

        try:
            with open(lease_file) as f:
                for line in f:
                                                                           
                    parts = line.strip().split()
                    if len(parts) >= 4:
                        mac = parts[1].upper()
                        ip  = parts[2]
                        hostname = parts[3] if parts[3] != "*" else "—"
                        devices.append(ConnectedDevice(ip=ip, mac=mac, hostname=hostname))
        except (PermissionError, IOError):
            pass

        return devices

    def _from_arp(self, interface: str) -> List[ConnectedDevice]:
        devices = []
        try:
            result = subprocess.run(
                ["arp", "-n", "-i", interface],
                capture_output=True, text=True, timeout=5
            )
            for line in result.stdout.splitlines()[1:]:               
                parts = line.split()
                if len(parts) >= 3 and parts[2] not in ("(incomplete)", "<incomplete>"):
                    ip  = parts[0]
                    mac = parts[2].upper()
                    hostname = self._resolve_hostname(ip)
                    devices.append(ConnectedDevice(ip=ip, mac=mac, hostname=hostname))
        except (subprocess.TimeoutExpired, FileNotFoundError):
                                     
            devices = self._from_proc_arp(interface)

        return devices

    def _from_proc_arp(self, interface: str) -> List[ConnectedDevice]:
        devices = []
        try:
            with open("/proc/net/arp") as f:
                next(f)               
                for line in f:
                    parts = line.split()
                    if len(parts) >= 6 and parts[5] == interface:
                        ip  = parts[0]
                        mac = parts[3].upper()
                        if mac != "00:00:00:00:00:00":
                            hostname = self._resolve_hostname(ip)
                            devices.append(ConnectedDevice(ip=ip, mac=mac, hostname=hostname))
        except IOError:
            pass
        return devices

    def _resolve_hostname(self, ip: str) -> str:
        try:
            return socket.gethostbyaddr(ip)[0]
        except (socket.herror, socket.gaierror):
            return "—"

                                                                            

    def get_traffic_stats(self, interface: str) -> TrafficStats:
        if interface not in self._stats_cache:
            self._stats_cache[interface] = TrafficStats()

        stats = self._stats_cache[interface]

        try:
            with open("/proc/net/dev") as f:
                for line in f:
                    if interface + ":" in line:
                        parts = line.split()
                                                              
                                                                                     
                                                                                   
                        rx = int(parts[1])
                        tx = int(parts[9])

                        now = time.monotonic()
                        if interface in self._prev:
                            prev_rx, prev_tx, prev_t = self._prev[interface]
                            dt = now - prev_t
                            if dt > 0:
                                rx_speed = max(0.0, (rx - prev_rx) / dt)
                                tx_speed = max(0.0, (tx - prev_tx) / dt)
                                stats.rx_speed = rx_speed
                                stats.tx_speed = tx_speed

                                                    
                                stats.history_rx.append(rx_speed)
                                stats.history_tx.append(tx_speed)
                                if len(stats.history_rx) > stats.HISTORY_LEN:
                                    stats.history_rx.pop(0)
                                    stats.history_tx.pop(0)

                        self._prev[interface] = (rx, tx, now)
                        stats.rx_bytes = rx
                        stats.tx_bytes = tx
                        break
        except (IOError, IndexError, ValueError):
            pass

        return stats

    def reset(self, interface: str):
        self._prev.pop(interface, None)
        self._stats_cache.pop(interface, None)

                                                                           

    @staticmethod
    def fmt_bytes(n: int) -> str:
        return _fmt_bytes(n)

    @staticmethod
    def fmt_speed(bps: float) -> str:
        return _fmt_speed(bps)