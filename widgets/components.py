import math
from PyQt6.QtWidgets import QWidget, QSizePolicy, QGraphicsOpacityEffect
from PyQt6.QtCore import (
    Qt, QTimer, QPropertyAnimation, QEasingCurve,
    pyqtProperty, pyqtSignal, QRectF, QSequentialAnimationGroup,
    QPauseAnimation,
)
from PyQt6.QtGui import (
    QPainter, QColor, QPainterPath, QPen, QBrush,
)


                                                                                

class ToggleSwitch(QWidget):

    toggled = pyqtSignal(bool)

    def __init__(self, parent=None, checked=False):
        super().__init__(parent)
        self._checked = checked
        self._thumb_pos = 1.0 if checked else 0.0

        self.setFixedSize(46, 26)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self._anim = QPropertyAnimation(self, b"thumb_pos", self)
        self._anim.setDuration(180)
        self._anim.setEasingCurve(QEasingCurve.Type.InOutCubic)

    @pyqtProperty(float)
    def thumb_pos(self):
        return self._thumb_pos

    @thumb_pos.setter
    def thumb_pos(self, value):
        self._thumb_pos = value
        self.update()

    def isChecked(self) -> bool:
        return self._checked

    def setChecked(self, checked: bool):
        if checked != self._checked:
            self._checked = checked
            self._animate_to(1.0 if checked else 0.0)

    def mousePressEvent(self, event):
        self._checked = not self._checked
        self._animate_to(1.0 if self._checked else 0.0)
        self.toggled.emit(self._checked)

    def _animate_to(self, target: float):
        self._anim.stop()
        self._anim.setStartValue(self._thumb_pos)
        self._anim.setEndValue(target)
        self._anim.start()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        r = h / 2

                                    
        off_c = QColor("#2d333b")
        on_c  = QColor("#3fb950")
        t = self._thumb_pos
        track_color = QColor(
            int(off_c.red()   + (on_c.red()   - off_c.red())   * t),
            int(off_c.green() + (on_c.green() - off_c.green()) * t),
            int(off_c.blue()  + (on_c.blue()  - off_c.blue())  * t),
        )

        p.setBrush(track_color)
        p.setPen(Qt.PenStyle.NoPen)
        path = QPainterPath()
        path.addRoundedRect(QRectF(0, 0, w, h), r, r)
        p.drawPath(path)

                  
        d = h - 4
        x = 2 + t * (w - d - 4)
        p.setBrush(QColor("#ffffff"))
        p.drawEllipse(QRectF(x, 2, d, d))

        p.end()


                                                                                

class StatusDot(QWidget):

    def __init__(self, color: str = "#3fb950", size: int = 10, parent=None):
        super().__init__(parent)
        self._color = QColor(color)
        self._dot_size = size
        self._pulse_step = 0.0
        self._pulsing = False

        extra = size * 2
        self.setFixedSize(size + extra, size + extra)

        self._timer = QTimer(self)
        self._timer.setInterval(30)           
        self._timer.timeout.connect(self._tick)

    def set_color(self, color: str):
        self._color = QColor(color)
        self.update()

    def start_pulse(self):
        self._pulsing = True
        self._pulse_step = 0.0
        self._timer.start()

    def stop_pulse(self):
        self._pulsing = False
        self._timer.stop()
        self._pulse_step = 0.0
        self.update()

    def _tick(self):
        self._pulse_step += 0.07
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(Qt.PenStyle.NoPen)

        cx = self.width() // 2
        cy = self.height() // 2
        r  = self._dot_size // 2

                             
        if self._pulsing:
            pulse_val = (math.sin(self._pulse_step) + 1) / 2        
            ring_r = r + int(pulse_val * (r + 4))
            alpha  = int(60 * (1.0 - pulse_val))
            ring_c = QColor(self._color)
            ring_c.setAlpha(alpha)
            p.setBrush(ring_c)
            p.drawEllipse(cx - ring_r, cy - ring_r, ring_r * 2, ring_r * 2)

                                    
        glow = QColor(self._color)
        glow.setAlpha(30)
        p.setBrush(glow)
        p.drawEllipse(cx - r - 2, cy - r - 2, (r + 2) * 2, (r + 2) * 2)

                         
        p.setBrush(self._color)
        p.drawEllipse(cx - r, cy - r, r * 2, r * 2)

        p.end()


                                                                                

class SpinnerWidget(QWidget):

    def __init__(self, size: int = 20, color: str = "#58a6ff",
                 width: float = 2.5, parent=None):
        super().__init__(parent)
        self._color = QColor(color)
        self._line_width = width
        self._angle = 0
        self.setFixedSize(size, size)
        self.hide()

        self._timer = QTimer(self)
        self._timer.setInterval(16)           
        self._timer.timeout.connect(self._tick)

    def start(self):
        self._angle = 0
        self._timer.start()
        self.show()

    def stop(self):
        self._timer.stop()
        self.hide()

    def _tick(self):
        self._angle = (self._angle + 7) % 360
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        m = int(self._line_width) + 1
        rect = QRectF(m, m, w - m * 2, h - m * 2)

                               
        bg = QColor(self._color)
        bg.setAlpha(25)
        pen_bg = QPen(bg, self._line_width)
        pen_bg.setCapStyle(Qt.PenCapStyle.RoundCap)
        p.setPen(pen_bg)
        p.drawArc(rect, 0, 360 * 16)

                              
        pen = QPen(self._color, self._line_width)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        p.setPen(pen)
        start_angle = (-self._angle + 90) * 16
        span_angle  = -270 * 16
        p.drawArc(rect, start_angle, span_angle)

        p.end()


                                                                                

class SparklineWidget(QWidget):

    def __init__(self, color: str = "#58a6ff", parent=None):
        super().__init__(parent)
        self._data: list[float] = []
        self._color = QColor(color)
        self.setMinimumHeight(64)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def set_data(self, data: list):
        self._data = list(data)
        self.update()

    def paintEvent(self, event):
        if len(self._data) < 2:
                                                                
            p = QPainter(self)
            p.setRenderHint(QPainter.RenderHint.Antialiasing)
            pen = QPen(QColor(self._color.red(), self._color.green(),
                              self._color.blue(), 40), 1)
            pen.setDashPattern([4, 6])
            p.setPen(pen)
            y = self.height() - 6
            p.drawLine(6, y, self.width() - 6, y)
            p.end()
            return

        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h   = self.width(), self.height()
        pad    = 4
        data   = self._data[-(w // 3):]                      
        n      = len(data)
        mx     = max(data) or 1.0

        def xy(i, v):
            x = pad + i * (w - 2 * pad) / (n - 1)
            y = h - pad - (v / mx) * (h - 2 * pad)
            return x, y

                                                                       
        pts = [xy(i, v) for i, v in enumerate(data)]

        line_path = QPainterPath()
        fill_path = QPainterPath()
        line_path.moveTo(*pts[0])
        fill_path.moveTo(pts[0][0], h - pad)
        fill_path.lineTo(*pts[0])

        for i in range(1, n):
            x0, y0 = pts[i - 1]
            x1, y1 = pts[i]
            cx = (x0 + x1) / 2
            line_path.cubicTo(cx, y0, cx, y1, x1, y1)
            fill_path.cubicTo(cx, y0, cx, y1, x1, y1)

        fill_path.lineTo(pts[-1][0], h - pad)
        fill_path.closeSubpath()

                                           
        fill_c = QColor(self._color)
        fill_c.setAlpha(28)
        p.setBrush(fill_c)
        p.setPen(Qt.PenStyle.NoPen)
        p.drawPath(fill_path)

                       
        line_pen = QPen(self._color, 2)
        line_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        line_pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        p.setPen(line_pen)
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawPath(line_path)

                                  
        last_x, last_y = pts[-1]
        p.setBrush(self._color)
        p.setPen(QPen(QColor(self._color.red(), self._color.green(),
                             self._color.blue(), 60), 3))
        p.drawEllipse(QRectF(last_x - 3.5, last_y - 3.5, 7, 7))

        p.end()


                                                                                

class FadeContainer(QWidget):


    def __init__(self, parent=None):
        super().__init__(parent)
        self._effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self._effect)
        self._effect.setOpacity(1.0)

        self._anim_out = QPropertyAnimation(self._effect, b"opacity", self)
        self._anim_out.setDuration(120)
        self._anim_out.setEasingCurve(QEasingCurve.Type.OutCubic)

        self._anim_in = QPropertyAnimation(self._effect, b"opacity", self)
        self._anim_in.setDuration(160)
        self._anim_in.setEasingCurve(QEasingCurve.Type.InCubic)

        self._pending_fn = None
        self._anim_out.finished.connect(self._on_out_finished)

    def fade_update(self, update_fn):

        self._pending_fn = update_fn
        self._anim_in.stop()
        self._anim_out.stop()
        self._anim_out.setStartValue(self._effect.opacity())
        self._anim_out.setEndValue(0.0)
        self._anim_out.start()

    def _on_out_finished(self):
        if self._pending_fn:
            self._pending_fn()
            self._pending_fn = None
        self._anim_in.setStartValue(0.0)
        self._anim_in.setEndValue(1.0)
        self._anim_in.start()
