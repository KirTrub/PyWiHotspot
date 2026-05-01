from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTextEdit, QPushButton,
)
from PyQt6.QtGui import QTextCursor

from widgets.styles import COLORS as C


_LEVEL_COLORS = {
    "INFO":    C["text_secondary"],
    "SUCCESS": C["success"],
    "ERROR":   C["danger"],
    "WARNING": C["warning"],
}


class LogWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(24, 22, 24, 22)
        lay.setSpacing(0)

               
        top = QHBoxLayout()
        top.setSpacing(12)

        title = QLabel("Журнал событий")
        title.setObjectName("page_title")
        top.addWidget(title)
        top.addStretch()

        btn_clear = QPushButton("Очистить")
        btn_clear.setObjectName("btn_secondary")
        btn_clear.setCursor(__import__("PyQt6.QtCore", fromlist=["Qt"]).Qt.CursorShape.PointingHandCursor)
        btn_clear.clicked.connect(self.clear)
        top.addWidget(btn_clear)

        lay.addLayout(top)
        lay.addSpacing(16)

                  
        self.editor = QTextEdit()
        self.editor.setReadOnly(True)
        lay.addWidget(self.editor)

                             
        self.log("Журнал событий запущен", "INFO")

    def log(self, message: str, level: str = "INFO"):
        ts    = datetime.now().strftime("%H:%M:%S")
        color = _LEVEL_COLORS.get(level, C["text_primary"])

                                                                
        level_padded = f"[{level}]".ljust(9)

        html = (
            f'<span style="color:{C["text_muted"]};font-family:monospace;">'
            f'[{ts}]</span> '
            f'<span style="color:{color};font-family:monospace;font-weight:600;">'
            f'{level_padded}</span> '
            f'<span style="color:{C["text_primary"]};">{message}</span>'
        )
        self.editor.append(html)
        self.editor.moveCursor(QTextCursor.MoveOperation.End)

    def clear(self):
        self.editor.clear()
