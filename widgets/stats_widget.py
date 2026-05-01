from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout,
)
from PyQt6.QtCore import Qt

from .components import SparklineWidget
from widgets.styles import COLORS as C


class StatsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(24, 22, 24, 22)
        lay.setSpacing(0)

                   
        header = QHBoxLayout()
        title = QLabel("Мониторинг трафика")
        title.setObjectName("page_title")
        header.addWidget(title)
        header.addStretch()
        lay.addLayout(header)
        lay.addSpacing(20)

                           
        grid = QGridLayout()
        grid.setSpacing(14)

        self.card_rx = self._make_stat_card(
            "Загрузка (Download)", C["accent"]
        )
        self.card_tx = self._make_stat_card(
            "Отдача (Upload)", C["success"]
        )

        grid.addWidget(self.card_rx["frame"], 0, 0)
        grid.addWidget(self.card_tx["frame"], 0, 1)
        lay.addLayout(grid)
        lay.addSpacing(28)

                         
        section = QLabel("АКТИВНОСТЬ СЕТИ")
        section.setObjectName("section_header")
        lay.addWidget(section)
        lay.addSpacing(14)

                          
        rx_label = QLabel("Входящий трафик (Rx)")
        rx_label.setObjectName("small_label")
        lay.addWidget(rx_label)
        lay.addSpacing(6)
        self.graph_rx = SparklineWidget(C["accent"])
        self.graph_rx.setMinimumHeight(70)
        lay.addWidget(self.graph_rx)
        lay.addSpacing(18)

                     
        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFixedHeight(1)
        lay.addWidget(sep)
        lay.addSpacing(18)

                           
        tx_label = QLabel("Исходящий трафик (Tx)")
        tx_label.setObjectName("small_label")
        lay.addWidget(tx_label)
        lay.addSpacing(6)
        self.graph_tx = SparklineWidget(C["success"])
        self.graph_tx.setMinimumHeight(70)
        lay.addWidget(self.graph_tx)

        lay.addStretch()

    def _make_stat_card(self, title: str, color: str) -> dict:
        frame = QFrame()
        frame.setObjectName("card")

        lay = QVBoxLayout(frame)
        lay.setContentsMargins(18, 16, 18, 16)
        lay.setSpacing(6)

        lbl_title = QLabel(title)
        lbl_title.setObjectName("small_label")

        lbl_val = QLabel("0.0 КБ/с")
        lbl_val.setObjectName("big_value")
        lbl_val.setStyleSheet(
            f"color: {color}; font-size: 28px; font-weight: 700;"
            " background: transparent;"
        )

        lbl_total = QLabel("Всего: 0 Б")
        lbl_total.setObjectName("subtitle")

                                       
        accent_bar = QFrame()
        accent_bar.setFixedHeight(3)
        accent_bar.setStyleSheet(
            f"background: {color}; border-radius: 2px;"
            " border: none;"
        )

                                                  
        outer = QVBoxLayout()
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        outer.addWidget(accent_bar)
        outer.addSpacing(14)
        outer.addWidget(lbl_title)
        outer.addSpacing(4)
        outer.addWidget(lbl_val)
        outer.addWidget(lbl_total)

                          
        for i in reversed(range(lay.count())):
            lay.itemAt(i).widget()
        while lay.count():
            lay.takeAt(0)

        lay.addLayout(outer)

        return {"frame": frame, "val": lbl_val, "total": lbl_total}

    def update_stats(self, stats, fmt_speed_func, fmt_bytes_func):
        self.card_rx["val"].setText(fmt_speed_func(stats.rx_speed))
        self.card_tx["val"].setText(fmt_speed_func(stats.tx_speed))
        self.card_rx["total"].setText(
            f"Всего: {fmt_bytes_func(stats.rx_bytes)}"
        )
        self.card_tx["total"].setText(
            f"Всего: {fmt_bytes_func(stats.tx_bytes)}"
        )
        self.graph_rx.set_data(stats.history_rx)
        self.graph_tx.set_data(stats.history_tx)
