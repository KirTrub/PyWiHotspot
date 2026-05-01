from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QPushButton, QFrame,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont

from widgets.styles import COLORS as C


class DeviceListWidget(QWidget):

    sig_refresh = pyqtSignal()

    COLUMNS = ["IP-адрес", "MAC-адрес", "Имя устройства"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(24, 22, 24, 22)
        lay.setSpacing(0)

               
        top = QHBoxLayout()
        top.setSpacing(12)

        title = QLabel("Подключённые устройства")
        title.setObjectName("page_title")

        self._lbl_count = QLabel("0 устройств")
        self._lbl_count.setObjectName("subtitle")
        self._lbl_count.setStyleSheet(
            f"background: {C['bg_hover']}; color: {C['text_secondary']};"
            " border-radius: 10px; padding: 2px 10px; font-size: 11px;"
            " font-weight: 600;"
        )

        btn_refresh = QPushButton("Обновить")
        btn_refresh.setObjectName("btn_secondary")
        btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_refresh.clicked.connect(self.sig_refresh)

        top.addWidget(title)
        top.addWidget(self._lbl_count, alignment=Qt.AlignmentFlag.AlignVCenter)
        top.addStretch()
        top.addWidget(btn_refresh)
        lay.addLayout(top)
        lay.addSpacing(18)

                 
        self._table = QTableWidget(0, len(self.COLUMNS))
        self._table.setHorizontalHeaderLabels(self.COLUMNS)
        self._table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self._table.horizontalHeader().setHighlightSections(False)
        self._table.verticalHeader().setVisible(False)
        self._table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self._table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._table.setAlternatingRowColors(True)
        self._table.setShowGrid(False)
        self._table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        lay.addWidget(self._table)

                     
        self._placeholder = self._make_placeholder()
        lay.addWidget(self._placeholder)

        self._placeholder.show()
        self._table.hide()

    def _make_placeholder(self) -> QFrame:
        frame = QFrame()
        frame.setObjectName("card")
        frame.setSizePolicy(
            frame.sizePolicy().horizontalPolicy(),
            frame.sizePolicy().Policy.Expanding,
        )

        lay = QVBoxLayout(frame)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.setContentsMargins(40, 60, 40, 60)
        lay.setSpacing(10)

                                                         
        icon_frame = QFrame()
        icon_frame.setFixedSize(56, 56)
        icon_frame.setStyleSheet(
            f"background: {C['bg_hover']}; border-radius: 14px; border: none;"
        )
        icon_lbl = QLabel("—")
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_lbl.setStyleSheet(
            f"color: {C['text_muted']}; font-size: 22px; font-weight: 700;"
            " background: transparent;"
        )
        icon_lay = QVBoxLayout(icon_frame)
        icon_lay.setContentsMargins(0, 0, 0, 0)
        icon_lay.addWidget(icon_lbl)

        lbl = QLabel("Нет подключённых устройств")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet(
            f"font-size: 15px; font-weight: 600; color: {C['text_primary']};"
            " background: transparent;"
        )

        hint = QLabel(
            "Устройства появятся здесь, когда подключатся к хот-споту"
        )
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint.setObjectName("subtitle")
        hint.setWordWrap(True)

        lay.addWidget(icon_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        lay.addSpacing(4)
        lay.addWidget(lbl)
        lay.addWidget(hint)
        return frame

    def update_devices(self, devices: list):
        if not devices:
            self._table.hide()
            self._placeholder.show()
            self._lbl_count.setText("0 устройств")
            return

        self._placeholder.hide()
        self._table.show()

        n = len(devices)
        suffix = "устройство" if n == 1 else (
            "устройства" if 2 <= n <= 4 else "устройств"
        )
        self._lbl_count.setText(f"{n} {suffix}")

        self._table.setRowCount(n)
        for row, dev in enumerate(devices):
            self._table.setRowHeight(row, 46)

            ip_item   = QTableWidgetItem(dev.ip)
            ip_item.setForeground(QColor(C["accent"]))
            font = ip_item.font()
            font.setFamily("JetBrains Mono, Cascadia Code, monospace")
            ip_item.setFont(font)

            mac_item  = QTableWidgetItem(dev.mac)
            mac_item.setForeground(QColor(C["text_muted"]))
            mac_item.setFont(font)

            host_item = QTableWidgetItem(dev.hostname)
            host_item.setForeground(QColor(C["text_primary"]))

            for col, item in enumerate([ip_item, mac_item, host_item]):
                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
                )
                self._table.setItem(row, col, item)
