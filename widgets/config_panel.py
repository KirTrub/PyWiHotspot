from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QComboBox,
    QScrollArea, QWidget, QSizePolicy, QSpacerItem,
)
from PyQt6.QtCore import Qt, pyqtSignal

from .components import ToggleSwitch, StatusDot, SpinnerWidget, FadeContainer
from widgets.styles import COLORS as C


                                                                                

def _sep() -> QFrame:
    line = QFrame()
    line.setObjectName("separator")
    line.setFixedHeight(1)
    return line


def _section_header(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setObjectName("section_header")
    return lbl


def _field_label(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setObjectName("subtitle")
    return lbl


                                                                                

class ConfigPanel(QFrame):

    sig_start             = pyqtSignal(str, str, str, str, str)
    sig_stop              = pyqtSignal()
    sig_autostart_changed = pyqtSignal(bool)

                                      
    _BANDS = [("2.4 ГГц (совместимее)", "bg"), ("5 ГГц", "a")]

    def __init__(self, wifi_interfaces: list, all_interfaces: list, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(292)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        inner = QWidget()
        inner.setObjectName("inner")
        inner.setStyleSheet("QWidget#inner { background: transparent; }")

        self._layout = QVBoxLayout(inner)
        self._layout.setContentsMargins(16, 18, 16, 20)
        self._layout.setSpacing(0)

        self._build_logo()
        self._layout.addSpacing(14)
        self._layout.addWidget(_sep())
        self._layout.addSpacing(14)
        self._build_status_card()
        self._layout.addSpacing(16)
        self._build_controls()
        self._layout.addSpacing(4)
        self._layout.addWidget(_sep())
        self._layout.addSpacing(14)
        self._build_config(wifi_interfaces, all_interfaces)
        self._layout.addSpacing(4)
        self._layout.addWidget(_sep())
        self._layout.addSpacing(14)
        self._build_autostart()
        self._layout.addStretch()

        scroll.setWidget(inner)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        outer.addWidget(scroll)

                                                                            

    def _build_logo(self):
        row = QHBoxLayout()
        row.setSpacing(10)

                                                       
        icon_frame = QFrame()
        icon_frame.setFixedSize(32, 32)
        icon_frame.setStyleSheet(
            f"background: {C['accent_dim']}; border: 1px solid {C['border_focus']};"
            " border-radius: 8px;"
        )
        icon_inner = QVBoxLayout(icon_frame)
        icon_inner.setContentsMargins(0, 0, 0, 0)
        dot = QLabel("W")
        dot.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dot.setStyleSheet(
            f"color: {C['accent']}; font-size: 13px; font-weight: 800;"
            " background: transparent; border: none;"
        )
        icon_inner.addWidget(dot)

        title = QLabel("PyHotspot")
        title.setObjectName("app_title")

        row.addWidget(icon_frame)
        row.addWidget(title)
        row.addStretch()
        self._layout.addLayout(row)

    def _build_status_card(self):
        self._fade = FadeContainer()

        self._status_card = QFrame()
        self._status_card.setObjectName("card_danger")

        lay = QVBoxLayout(self._status_card)
        lay.setContentsMargins(14, 12, 14, 12)
        lay.setSpacing(5)

                        
        row = QHBoxLayout()
        row.setSpacing(8)
        self._dot = StatusDot(C["danger"], size=9)
        self._lbl_status = QLabel("Остановлен")
        self._lbl_status.setObjectName("status_inactive")

        self._spinner = SpinnerWidget(size=16, color=C["warning"])
        row.addWidget(self._dot)
        row.addWidget(self._lbl_status)
        row.addStretch()
        row.addWidget(self._spinner)

                               
        self._lbl_ssid    = QLabel("Сеть: —")
        self._lbl_ssid.setObjectName("info_val")
        self._lbl_ip      = QLabel("IP: —")
        self._lbl_ip.setObjectName("subtitle")
        self._lbl_clients = QLabel("Клиентов: —")
        self._lbl_clients.setObjectName("subtitle")

        lay.addLayout(row)
        lay.addSpacing(2)
        lay.addWidget(self._lbl_ssid)
        lay.addWidget(self._lbl_ip)
        lay.addWidget(self._lbl_clients)

        fade_lay = QVBoxLayout(self._fade)
        fade_lay.setContentsMargins(0, 0, 0, 0)
        fade_lay.addWidget(self._status_card)

        self._layout.addWidget(self._fade)

    def _build_controls(self):
        col = QVBoxLayout()
        col.setSpacing(8)

        self._btn_start = QPushButton("Запустить хот-спот")
        self._btn_start.setObjectName("btn_start")
        self._btn_start.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_start.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self._btn_start.clicked.connect(self._on_start_clicked)

        self._btn_stop = QPushButton("Остановить")
        self._btn_stop.setObjectName("btn_stop")
        self._btn_stop.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_stop.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self._btn_stop.setEnabled(False)
        self._btn_stop.clicked.connect(self.sig_stop)

                       
        self._lbl_error = QLabel("")
        self._lbl_error.setObjectName("error_label")
        self._lbl_error.setWordWrap(True)
        self._lbl_error.hide()

        col.addWidget(self._btn_start)
        col.addWidget(self._btn_stop)
        col.addWidget(self._lbl_error)

        self._layout.addLayout(col)

    def _build_config(self, wifi_interfaces: list, all_interfaces: list):
        col = QVBoxLayout()
        col.setSpacing(12)

        col.addWidget(_section_header("НАСТРОЙКИ"))
        col.addSpacing(6)

              
        col.addWidget(_field_label("Имя сети (SSID)"))
        self._edit_ssid = QLineEdit("PyHotspot")
        self._edit_ssid.setPlaceholderText("Введите SSID…")
        col.addWidget(self._edit_ssid)

                
        col.addWidget(_field_label("Пароль"))
        pwd_row = QHBoxLayout()
        pwd_row.setSpacing(6)
        self._edit_pwd = QLineEdit("mypassword123")
        self._edit_pwd.setEchoMode(QLineEdit.EchoMode.Password)
        self._edit_pwd.setPlaceholderText("Минимум 8 символов")

        self._btn_eye = QPushButton("Показать")
        self._btn_eye.setObjectName("btn_secondary")
        self._btn_eye.setFixedWidth(74)
        self._btn_eye.setFixedHeight(34)
        self._btn_eye.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_eye.clicked.connect(self._toggle_password_vis)

        pwd_row.addWidget(self._edit_pwd)
        pwd_row.addWidget(self._btn_eye)
        col.addLayout(pwd_row)

                  
        col.addWidget(_field_label("Диапазон"))
        self._combo_band = QComboBox()
        for display, _ in self._BANDS:
            self._combo_band.addItem(display)
        col.addWidget(self._combo_band)

                         
        col.addWidget(_field_label("Wi-Fi интерфейс"))
        self._combo_iface = QComboBox()
        for iface in wifi_interfaces:
            self._combo_iface.addItem(iface)
        col.addWidget(self._combo_iface)

                                              
        col.addWidget(_field_label("Интернет-интерфейс"))
        self._combo_source = QComboBox()
        self._combo_source.addItem("Авто")
        for iface in all_interfaces:
            self._combo_source.addItem(iface)
        col.addWidget(self._combo_source)

        self._layout.addLayout(col)

    def _build_autostart(self):
        col = QVBoxLayout()
        col.setSpacing(10)
        col.addWidget(_section_header("СИСТЕМА"))
        col.addSpacing(4)

        row = QHBoxLayout()
        row.setSpacing(10)

        lbl_col = QVBoxLayout()
        lbl_col.setSpacing(2)
        lbl_main = QLabel("Автозапуск")
        lbl_main.setObjectName("subtitle")
        lbl_main.setStyleSheet(
            f"font-size: 13px; color: {C['text_primary']}; background: transparent;"
        )
        lbl_sub = QLabel("Запускать при старте системы")
        lbl_sub.setObjectName("subtitle")
        lbl_col.addWidget(lbl_main)
        lbl_col.addWidget(lbl_sub)

        self._toggle_autostart = ToggleSwitch()
        self._toggle_autostart.toggled.connect(self.sig_autostart_changed)

        row.addLayout(lbl_col)
        row.addStretch()
        row.addWidget(self._toggle_autostart)
        col.addLayout(row)

        self._layout.addLayout(col)

                                                                            

    def _toggle_password_vis(self):
        if self._edit_pwd.echoMode() == QLineEdit.EchoMode.Password:
            self._edit_pwd.setEchoMode(QLineEdit.EchoMode.Normal)
            self._btn_eye.setText("Скрыть")
        else:
            self._edit_pwd.setEchoMode(QLineEdit.EchoMode.Password)
            self._btn_eye.setText("Показать")

    def _on_start_clicked(self):
        self._lbl_error.hide()
        ssid   = self._edit_ssid.text().strip()
        pwd    = self._edit_pwd.text()
        band   = self._BANDS[self._combo_band.currentIndex()][1]
        iface  = self._combo_iface.currentText()
        source = self._combo_source.currentText()

        if not ssid:
            self.show_error("Имя сети не может быть пустым")
            return
        if len(pwd) < 8:
            self.show_error("Пароль должен содержать минимум 8 символов")
            return

        self.sig_start.emit(ssid, pwd, band, iface, source)

                                                                            

    def set_active(self, active: bool, ssid: str = None, ip: str = None):
        def _update():
            if active:
                self._status_card.setObjectName("card_success")
                self._dot.set_color(C["success"])
                self._dot.start_pulse()
                self._lbl_status.setObjectName("status_active")
                self._lbl_status.setText("Активен")
                self._lbl_ssid.setText(f"Сеть: {ssid or '—'}")
                self._lbl_ip.setText(f"IP: {ip or '—'}")
                self._lbl_clients.setText("Клиентов: 0")
            else:
                self._status_card.setObjectName("card_danger")
                self._dot.set_color(C["danger"])
                self._dot.stop_pulse()
                self._lbl_status.setObjectName("status_inactive")
                self._lbl_status.setText("Остановлен")
                self._lbl_ssid.setText("Сеть: —")
                self._lbl_ip.setText("IP: —")
                self._lbl_clients.setText("Клиентов: —")

                                                        
            self._status_card.style().unpolish(self._status_card)
            self._status_card.style().polish(self._status_card)
            self._lbl_status.style().unpolish(self._lbl_status)
            self._lbl_status.style().polish(self._lbl_status)

            self._btn_start.setEnabled(not active)
            self._btn_stop.setEnabled(active)

        self._fade.fade_update(_update)

    def set_busy(self, busy: bool):
        self._btn_start.setEnabled(not busy)
        self._btn_stop.setEnabled(not busy)
        if busy:
            self._lbl_status.setObjectName("status_busy")
            self._lbl_status.setText("Загрузка…")
            self._lbl_status.style().unpolish(self._lbl_status)
            self._lbl_status.style().polish(self._lbl_status)
            self._spinner.start()
        else:
            self._spinner.stop()

    def show_error(self, msg: str):
        self._lbl_error.setText(msg)
        self._lbl_error.show()

    def set_clients_count(self, n: int):
        suffix = "устройство" if n == 1 else (
            "устройства" if 2 <= n <= 4 else "устройств"
        )
        self._lbl_clients.setText(f"Клиентов: {n} {suffix}")

    def set_autostart(self, enabled: bool):
        self._toggle_autostart.setChecked(enabled)

    def get_config(self) -> dict:
        return {
            "ssid":      self._edit_ssid.text().strip(),
            "password":  self._edit_pwd.text(),
            "band":      self._BANDS[self._combo_band.currentIndex()][1],
            "interface": self._combo_iface.currentText(),
        }
