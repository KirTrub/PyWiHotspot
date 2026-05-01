import io
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QFileDialog,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage

from widgets.styles import COLORS as C


class QRWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._ssid     = ""
        self._password = ""
        self._pixmap   = None
        self._build_ui()

    def _build_ui(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(24, 22, 24, 22)
        lay.setSpacing(0)

                   
        title = QLabel("QR-код для подключения")
        title.setObjectName("page_title")
        lay.addWidget(title)

        lay.addSpacing(6)
        sub = QLabel("Отсканируйте камерой телефона для мгновенного подключения")
        sub.setObjectName("subtitle")
        sub.setWordWrap(True)
        lay.addWidget(sub)

        lay.addStretch()

                                                     
        center = QHBoxLayout()
        center.addStretch()

                             
        self._card = QFrame()
        self._card.setObjectName("card")
        self._card.setFixedWidth(300)

        card_lay = QVBoxLayout(self._card)
        card_lay.setContentsMargins(28, 28, 28, 28)
        card_lay.setSpacing(16)
        card_lay.setAlignment(Qt.AlignmentFlag.AlignCenter)

                        
        self._qr_label = QLabel()
        self._qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._qr_label.setFixedSize(240, 240)
        self._qr_label.setStyleSheet(
            "background: #ffffff; border-radius: 10px;"
            " padding: 8px; border: none;"
        )

                 
        self._lbl_ssid = QLabel("—")
        self._lbl_ssid.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._lbl_ssid.setStyleSheet(
            f"font-size: 16px; font-weight: 700; color: {C['text_primary']};"
            " background: transparent;"
        )

        self._lbl_pass = QLabel("—")
        self._lbl_pass.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._lbl_pass.setStyleSheet(
            f"font-size: 12px; color: {C['text_secondary']};"
            " background: transparent; font-family: monospace;"
        )

                     
        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFixedHeight(1)

                           
        self._btn_save = QPushButton("Сохранить QR-код")
        self._btn_save.setObjectName("btn_secondary")
        self._btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_save.setEnabled(False)
        self._btn_save.clicked.connect(self._save_qr)

        card_lay.addWidget(self._qr_label,
                           alignment=Qt.AlignmentFlag.AlignCenter)
        card_lay.addWidget(self._lbl_ssid)
        card_lay.addWidget(self._lbl_pass)
        card_lay.addWidget(sep)
        card_lay.addWidget(self._btn_save)

        center.addWidget(self._card)

                             
        self._placeholder = QFrame()
        self._placeholder.setObjectName("card")
        self._placeholder.setFixedWidth(300)

        ph_lay = QVBoxLayout(self._placeholder)
        ph_lay.setContentsMargins(28, 48, 28, 48)
        ph_lay.setSpacing(12)
        ph_lay.setAlignment(Qt.AlignmentFlag.AlignCenter)

        ph_icon = QFrame()
        ph_icon.setFixedSize(60, 60)
        ph_icon.setStyleSheet(
            f"background: {C['bg_hover']}; border-radius: 16px; border: none;"
        )
        ph_icon_lbl = QLabel("QR")
        ph_icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ph_icon_lbl.setStyleSheet(
            f"color: {C['text_muted']}; font-size: 14px; font-weight: 800;"
            " background: transparent;"
        )
        ph_icon_lay = QVBoxLayout(ph_icon)
        ph_icon_lay.setContentsMargins(0, 0, 0, 0)
        ph_icon_lay.addWidget(ph_icon_lbl)

        ph_title = QLabel("QR-код не создан")
        ph_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ph_title.setStyleSheet(
            f"font-size: 15px; font-weight: 600; color: {C['text_primary']};"
            " background: transparent;"
        )

        ph_hint = QLabel("Запустите хот-спот, чтобы\nгенерировать QR-код")
        ph_hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ph_hint.setObjectName("subtitle")

        ph_lay.addWidget(ph_icon, alignment=Qt.AlignmentFlag.AlignCenter)
        ph_lay.addSpacing(4)
        ph_lay.addWidget(ph_title)
        ph_lay.addWidget(ph_hint)

        center.addWidget(self._placeholder)
        center.addStretch()

                             
        self._card.hide()
        self._placeholder.show()

        lay.addLayout(center)
        lay.addStretch()

    def generate(self, ssid: str, password: str):
        try:
            import qrcode
        except ImportError:
            self._qr_label.setText("Установите:\npip install qrcode Pillow")
            return

        self._ssid     = ssid
        self._password = password

        wifi_str = f"WIFI:T:WPA;S:{ssid};P:{password};;"

        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=8,
            border=2,
        )
        qr.add_data(wifi_str)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)

        qimg = QImage.fromData(buf.read())
        self._pixmap = QPixmap.fromImage(qimg)

        self._qr_label.setPixmap(
            self._pixmap.scaled(
                224, 224,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        self._lbl_ssid.setText(ssid)
        self._lbl_pass.setText(password)

        self._placeholder.hide()
        self._card.show()
        self._btn_save.setEnabled(True)

    def clear(self):
        self._card.hide()
        self._placeholder.show()
        self._btn_save.setEnabled(False)
        self._pixmap = None

    def _save_qr(self):
        if not self._pixmap:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить QR-код",
            f"qr_{self._ssid}.png",
            "PNG изображения (*.png)"
        )
        if path:
            self._pixmap.save(path)
