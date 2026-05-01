import os
import sys

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QTabWidget, QApplication,
)
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot, QTimer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from core.hotspot import HotspotManager
from core.monitor import NetworkMonitor
from core.autostart import AutostartManager
from widgets import ConfigPanel, DeviceListWidget, QRWidget, StatsWidget, LogWidget
from widgets.styles import get_stylesheet


                                                                                

class InitWorker(QThread):
    ready = pyqtSignal(list, list, bool, str, object)                                       

    def __init__(self, hotspot: HotspotManager, autostart: AutostartManager):
        super().__init__()
        self._hs  = hotspot
        self._ast = autostart

    def run(self):
        wifi_ifaces = self._hs.get_wifi_interfaces()
        all_ifaces  = self._hs.get_all_interfaces()
        active      = self._hs.is_active()
        ip          = self._hs.get_hotspot_ip() if active else None
        ast_on      = self._ast.is_enabled()
        self.ready.emit(wifi_ifaces, all_ifaces, active, ip or "", ast_on)


class HotspotWorker(QThread):
    finished = pyqtSignal(bool, str)

    def __init__(self, manager: HotspotManager, params: dict, mode: str = "start"):
        super().__init__()
        self._mgr    = manager
        self._params = params
        self._mode   = mode

    def run(self):
        if self._mode == "start":
            ok, msg = self._mgr.start(
                self._params["ssid"],
                self._params["password"],
                self._params["band"],
                self._params["interface"],
            )
        else:
            ok, msg = self._mgr.stop()
        self.finished.emit(ok, msg)


class MonitorThread(QThread):
    stats_updated   = pyqtSignal(object)
    devices_updated = pyqtSignal(list)

    def __init__(self, hotspot_mgr: HotspotManager, monitor_mgr: NetworkMonitor):
        super().__init__()
        self._hs      = hotspot_mgr
        self._mon     = monitor_mgr
        self._running = True

    def run(self):
        tick = 0
        while self._running:
            tick += 1
                                         
            if tick % 3 == 1:
                is_active = self._hs.is_active()
                                                 

            if is_active:
                iface = self._hs.get_active_interface()
                stats = self._mon.get_traffic_stats(iface)
                self.stats_updated.emit(stats)

                                                                
                if tick % 3 == 1:
                    devices = self._mon.get_connected_devices(iface)
                    self.devices_updated.emit(devices)

            self.msleep(1000)

    def stop(self):
        self._running = False


                                                                                

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyHotspot")
        self.resize(1020, 660)
        self.setStyleSheet(get_stylesheet())

                 
        self.hotspot   = HotspotManager()
        self.monitor   = NetworkMonitor()
        self.autostart = AutostartManager()

                                                                       
        self._init_worker    = None
        self._hotspot_worker = None
        self._active_params  = {}

                                                            
        self._init_ui_placeholder()

                               
        self._init_worker = InitWorker(self.hotspot, self.autostart)
        self._init_worker.ready.connect(self._on_init_ready)
        self._init_worker.start()

                                                                            

    def _init_ui_placeholder(self):

        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

                                                                  
        self.config_panel = ConfigPanel(["wlan0"], ["eth0", "wlan0"])
        layout.addWidget(self.config_panel)

                                
        self.tabs        = QTabWidget()
        self.stats_page  = StatsWidget()
        self.devices_page = DeviceListWidget()
        self.qr_page     = QRWidget()
        self.log_widget  = LogWidget()

        self.tabs.addTab(self.stats_page,   "Статистика")
        self.tabs.addTab(self.devices_page, "Устройства")
        self.tabs.addTab(self.qr_page,      "QR-код")
        self.tabs.addTab(self.log_widget,   "Логи")
        layout.addWidget(self.tabs)

                 
        self.config_panel.sig_start.connect(self._start_hotspot)
        self.config_panel.sig_stop.connect(self._stop_hotspot)
        self.config_panel.sig_autostart_changed.connect(self._toggle_autostart)
        self.devices_page.sig_refresh.connect(self._force_refresh)

                                                                             

    @pyqtSlot(list, list, bool, str, object)
    def _on_init_ready(self, wifi_ifaces, all_ifaces, active, ip, ast_on):
                                          
        self.config_panel._combo_iface.clear()
        for iface in wifi_ifaces:
            self.config_panel._combo_iface.addItem(iface)

        self.config_panel._combo_source.clear()
        self.config_panel._combo_source.addItem("Авто")
        for iface in all_ifaces:
            self.config_panel._combo_source.addItem(iface)

        self.config_panel.set_autostart(ast_on)

        if active:
            ssid = self.hotspot.config.ssid
            self.config_panel.set_active(True, ssid, ip or None)
            self.qr_page.generate(ssid, self.hotspot.config.password)
            self.log_widget.log("Хот-спот уже активен при запуске", "INFO")
        else:
            self.config_panel.set_active(False)
            self.log_widget.log("Приложение готово к работе", "INFO")

                              
        self._monitor_thread = MonitorThread(self.hotspot, self.monitor)
        self._monitor_thread.stats_updated.connect(self._on_stats_received)
        self._monitor_thread.devices_updated.connect(self._on_devices_received)
        self._monitor_thread.start()

                                                                             

    @pyqtSlot(object)
    def _on_stats_received(self, stats):
        self.stats_page.update_stats(
            stats, self.monitor.fmt_speed, self.monitor.fmt_bytes
        )

    @pyqtSlot(list)
    def _on_devices_received(self, devices):
        self.devices_page.update_devices(devices)
        self.config_panel.set_clients_count(len(devices))

    def _force_refresh(self):
        self.log_widget.log("Принудительное обновление списка устройств…", "INFO")

                                                                            

    @pyqtSlot(str, str, str, str, str)
    def _start_hotspot(self, ssid, pwd, band, iface, source):
        self.log_widget.log(f"Запуск точки доступа «{ssid}» на {iface}…", "INFO")
        self.config_panel.set_busy(True)
        self._active_params = {
            "ssid": ssid, "password": pwd,
            "band": band, "interface": iface,
        }
        self._hotspot_worker = HotspotWorker(
            self.hotspot, self._active_params, mode="start"
        )
        self._hotspot_worker.finished.connect(self._on_start_finished)
        self._hotspot_worker.start()

    @pyqtSlot(bool, str)
    def _on_start_finished(self, success, msg):
        self.config_panel.set_busy(False)
        if success:
            self.log_widget.log("Хот-спот успешно запущен", "SUCCESS")
            ip = self.hotspot.get_hotspot_ip()
            self.config_panel.set_active(
                True, self._active_params["ssid"], ip
            )
            self.qr_page.generate(
                self._active_params["ssid"],
                self._active_params["password"],
            )
        else:
            self.log_widget.log(f"Ошибка запуска: {msg}", "ERROR")
            self.config_panel.show_error(msg)
            self.config_panel.set_active(False)

    @pyqtSlot()
    def _stop_hotspot(self):
        self.log_widget.log("Остановка хот-спота…", "INFO")
        self.config_panel.set_busy(True)
        self._hotspot_worker = HotspotWorker(self.hotspot, {}, mode="stop")
        self._hotspot_worker.finished.connect(self._on_stop_finished)
        self._hotspot_worker.start()

    @pyqtSlot(bool, str)
    def _on_stop_finished(self, success, msg):
        self.config_panel.set_busy(False)
        if success:
            self.log_widget.log("Хот-спот остановлен", "SUCCESS")
            self.config_panel.set_active(False)
            self.qr_page.clear()
        else:
            self.log_widget.log(f"Ошибка при остановке: {msg}", "ERROR")

    @pyqtSlot(bool)
    def _toggle_autostart(self, enabled: bool):
        if enabled:
            conf     = self.config_panel.get_config()
            ok, msg  = self.autostart.enable(**conf)
        else:
            ok, msg  = self.autostart.disable()
        level = "SUCCESS" if ok else "ERROR"
        self.log_widget.log(msg, level)

                                                                            

    def closeEvent(self, event):
        if hasattr(self, "_monitor_thread"):
            self._monitor_thread.stop()
            self._monitor_thread.wait(2000)
        event.accept()
