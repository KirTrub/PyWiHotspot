import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


def check_dependencies() -> list:
    missing = []
    for pkg, import_name in [("PyQt6", "PyQt6"), ("qrcode", "qrcode"), ("Pillow", "PIL")]:
        try:
            __import__(import_name)
        except ImportError:
            missing.append(pkg)
    return missing


def main():
    missing = check_dependencies()
    if missing:
        print("Отсутствуют зависимости:", ", ".join(missing))
        print("Установите: pip install " + " ".join(missing))
        sys.exit(1)

    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import Qt
    from PyQt6.QtGui import QFont
    from ui.main_window import MainWindow

    os.environ.setdefault("QT_AUTO_SCREEN_SCALE_FACTOR", "1")

    app = QApplication(sys.argv)
    app.setApplicationName("PyHotspot")
    app.setApplicationDisplayName("PyHotspot")
    app.setOrganizationName("PyHotspot")

    font = QFont("Inter", 10)
    font.setHintingPreference(QFont.HintingPreference.PreferFullHinting)
    app.setFont(font)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
