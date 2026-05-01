COLORS = {
    "bg_window":      "#0d1117",
    "bg_panel":       "#161b22",
    "bg_card":        "#1c2230",
    "bg_input":       "#21262d",
    "bg_hover":       "#2d333b",
    "border":         "#30363d",
    "border_focus":   "#58a6ff",

    "text_primary":   "#e6edf3",
    "text_secondary": "#8b949e",
    "text_muted":     "#484f58",

    "accent":         "#58a6ff",
    "accent_hover":   "#79c0ff",
    "accent_dim":     "#1f4068",

    "success":        "#3fb950",
    "success_dim":    "#152a19",
    "success_hover":  "#56d364",
    "success_border": "#2ea043",

    "danger":         "#f85149",
    "danger_dim":     "#2d0f0e",
    "danger_hover":   "#ff7b72",
    "danger_border":  "#da3633",

    "warning":        "#e3b341",
    "warning_dim":    "#2e220a",
}

C = COLORS


def get_stylesheet() -> str:
    return f"""

/* ── Базовые ─────────────────────────────────────────────────────────── */

* {{
    box-sizing: border-box;
}}

QWidget {{
    background-color: {C['bg_window']};
    color: {C['text_primary']};
    font-family: "Inter", "SF Pro Display", "Segoe UI", "Ubuntu", sans-serif;
    font-size: 13px;
    border: none;
    outline: none;
}}

QMainWindow {{
    background-color: {C['bg_window']};
}}

/* ── Левая панель ────────────────────────────────────────────────────── */

QFrame#sidebar {{
    background-color: {C['bg_panel']};
    border-right: 1px solid {C['border']};
}}

/* ── Карточки ────────────────────────────────────────────────────────── */

QFrame#card {{
    background-color: {C['bg_card']};
    border: 1px solid {C['border']};
    border-radius: 10px;
}}

QFrame#card_success {{
    background-color: {C['success_dim']};
    border: 1px solid {C['success_border']};
    border-radius: 10px;
}}

QFrame#card_danger {{
    background-color: {C['danger_dim']};
    border: 1px solid {C['danger_border']};
    border-radius: 10px;
}}

QFrame#card_accent {{
    background-color: {C['accent_dim']};
    border: 1px solid {C['border_focus']};
    border-radius: 10px;
}}

QFrame#separator {{
    background-color: {C['border']};
    max-height: 1px;
    min-height: 1px;
    border: none;
}}

/* ── Метки ───────────────────────────────────────────────────────────── */

QLabel {{
    background: transparent;
    color: {C['text_primary']};
}}

QLabel#app_title {{
    font-size: 17px;
    font-weight: 700;
    color: {C['text_primary']};
    letter-spacing: -0.3px;
    background: transparent;
}}

QLabel#page_title {{
    font-size: 20px;
    font-weight: 700;
    color: {C['text_primary']};
    letter-spacing: -0.5px;
    background: transparent;
}}

QLabel#subtitle {{
    font-size: 12px;
    color: {C['text_secondary']};
    background: transparent;
}}

QLabel#section_header {{
    font-size: 10px;
    font-weight: 600;
    color: {C['text_muted']};
    letter-spacing: 1.2px;
    text-transform: uppercase;
    background: transparent;
}}

QLabel#status_active {{
    font-size: 13px;
    font-weight: 600;
    color: {C['success']};
    background: transparent;
}}

QLabel#status_inactive {{
    font-size: 13px;
    font-weight: 600;
    color: {C['text_secondary']};
    background: transparent;
}}

QLabel#status_busy {{
    font-size: 13px;
    font-weight: 600;
    color: {C['warning']};
    background: transparent;
}}

QLabel#big_value {{
    font-size: 30px;
    font-weight: 700;
    letter-spacing: -0.5px;
    background: transparent;
}}

QLabel#small_label {{
    font-size: 11px;
    color: {C['text_secondary']};
    background: transparent;
}}

QLabel#error_label {{
    color: {C['danger']};
    font-size: 12px;
    background: transparent;
    padding: 4px 0px;
}}

QLabel#info_key {{
    font-size: 12px;
    color: {C['text_muted']};
    background: transparent;
}}

QLabel#info_val {{
    font-size: 12px;
    color: {C['text_primary']};
    background: transparent;
    font-weight: 500;
}}

/* ── Кнопки ──────────────────────────────────────────────────────────── */

QPushButton {{
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 13px;
    font-weight: 500;
    border: none;
    min-height: 10px;
}}

QPushButton#btn_start {{
    background-color: {C['success']};
    color: #ffffff;
    font-size: 14px;
    font-weight: 600;
    padding: 11px 20px;
    border-radius: 10px;
    min-height: 10px;
}}
QPushButton#btn_start:hover {{
    background-color: {C['success_hover']};
}}
QPushButton#btn_start:pressed {{
    background-color: {C['success']};
}}
QPushButton#btn_start:disabled {{
    background-color: {C['bg_hover']};
    color: {C['text_muted']};
}}

QPushButton#btn_stop {{
    background-color: {C['danger']};
    color: #ffffff;
    font-size: 14px;
    font-weight: 600;
    padding: 11px 20px;
    border-radius: 10px;
    min-height: 10px;
}}
QPushButton#btn_stop:hover {{
    background-color: {C['danger_hover']};
}}
QPushButton#btn_stop:pressed {{
    background-color: {C['danger']};
}}
QPushButton#btn_stop:disabled {{
    background-color: {C['bg_hover']};
    color: {C['text_muted']};
}}

QPushButton#btn_primary {{
    background-color: {C['accent']};
    color: #ffffff;
}}
QPushButton#btn_primary:hover {{
    background-color: {C['accent_hover']};
}}
QPushButton#btn_primary:disabled {{
    background-color: {C['bg_hover']};
    color: {C['text_muted']};
}}

QPushButton#btn_secondary {{
    background-color: transparent;
    color: {C['text_secondary']};
    border: 1px solid {C['border']};
    border-radius: 8px;
    padding: 7px 14px;
    min-height: 32px;
}}
QPushButton#btn_secondary:hover {{
    background-color: {C['bg_hover']};
    color: {C['text_primary']};
    border-color: {C['text_muted']};
}}
QPushButton#btn_secondary:pressed {{
    background-color: {C['bg_card']};
}}

QPushButton#btn_icon {{
    background-color: transparent;
    color: {C['text_secondary']};
    padding: 5px;
    border-radius: 6px;
    min-width: 28px;
    max-width: 28px;
    min-height: 28px;
    max-height: 28px;
    font-size: 14px;
    font-weight: 600;
}}
QPushButton#btn_icon:hover {{
    background-color: {C['bg_hover']};
    color: {C['text_primary']};
}}

/* ── Поля ввода ──────────────────────────────────────────────────────── */

QLineEdit {{
    background-color: {C['bg_input']};
    border: 1px solid {C['border']};
    border-radius: 8px;
    padding: 8px 12px;
    color: {C['text_primary']};
    font-size: 13px;
    selection-background-color: {C['accent_dim']};
    selection-color: {C['accent']};
    min-height: 15px;
}}
QLineEdit:focus {{
    border-color: {C['border_focus']};
    background-color: {C['bg_card']};
}}
QLineEdit:disabled {{
    color: {C['text_muted']};
    background-color: {C['bg_window']};
    border-color: {C['bg_hover']};
}}

/* ── Комбобокс ───────────────────────────────────────────────────────── */

QComboBox {{
    background-color: {C['bg_input']};
    border: 1px solid {C['border']};
    border-radius: 8px;
    padding: 8px 12px;
    color: {C['text_primary']};
    font-size: 13px;
    min-height: 34px;
    selection-background-color: transparent;
}}
QComboBox:focus {{
    border-color: {C['border_focus']};
}}
QComboBox:disabled {{
    color: {C['text_muted']};
    background-color: {C['bg_window']};
}}
QComboBox::drop-down {{
    border: none;
    padding-right: 10px;
    width: 20px;
}}
QComboBox::down-arrow {{
    image: none;
    width: 0;
    height: 0;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid {C['text_secondary']};
}}
QComboBox QAbstractItemView {{
    background-color: {C['bg_card']};
    border: 1px solid {C['border']};
    border-radius: 8px;
    color: {C['text_primary']};
    selection-background-color: {C['accent_dim']};
    selection-color: {C['accent']};
    outline: none;
    padding: 4px;
}}
QComboBox QAbstractItemView::item {{
    padding: 8px 12px;
    border-radius: 6px;
    min-height: 30px;
}}
QComboBox QAbstractItemView::item:selected {{
    background-color: {C['accent_dim']};
}}

/* ── Вкладки (правая область) ────────────────────────────────────────── */

QTabWidget {{
    background: transparent;
}}
QTabWidget::pane {{
    background-color: {C['bg_window']};
    border: none;
    border-top: 1px solid {C['border']};
}}
QTabBar {{
    background: {C['bg_window']};
}}
QTabBar::tab {{
    background: transparent;
    color: {C['text_secondary']};
    padding: 11px 22px;
    font-size: 13px;
    font-weight: 500;
    border: none;
    border-bottom: 2px solid transparent;
}}
QTabBar::tab:selected {{
    color: {C['accent']};
    border-bottom: 2px solid {C['accent']};
    font-weight: 600;
}}
QTabBar::tab:hover:!selected {{
    color: {C['text_primary']};
    background-color: {C['bg_hover']};
}}

/* ── Таблица устройств ───────────────────────────────────────────────── */

QTableWidget {{
    background-color: transparent;
    border: 1px solid {C['border']};
    border-radius: 10px;
    gridline-color: {C['bg_hover']};
    color: {C['text_primary']};
    selection-background-color: {C['accent_dim']};
    selection-color: {C['accent']};
    alternate-background-color: {C['bg_card']};
}}
QTableWidget::item {{
    padding: 10px 14px;
    border: none;
}}
QTableWidget::item:selected {{
    background-color: {C['accent_dim']};
    color: {C['accent']};
}}
QHeaderView {{
    background: transparent;
}}
QHeaderView::section {{
    background-color: {C['bg_card']};
    color: {C['text_muted']};
    padding: 10px 14px;
    border: none;
    border-bottom: 1px solid {C['border']};
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
}}
QHeaderView::section:first {{
    border-top-left-radius: 10px;
}}
QHeaderView::section:last {{
    border-top-right-radius: 10px;
}}

/* ── Скроллбар ───────────────────────────────────────────────────────── */

QScrollBar:vertical {{
    background: transparent;
    width: 5px;
    border-radius: 2px;
}}
QScrollBar::handle:vertical {{
    background: {C['bg_hover']};
    border-radius: 2px;
    min-height: 24px;
}}
QScrollBar::handle:vertical:hover {{
    background: {C['text_muted']};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
QScrollBar:horizontal {{
    background: transparent;
    height: 5px;
    border-radius: 2px;
}}
QScrollBar::handle:horizontal {{
    background: {C['bg_hover']};
    border-radius: 2px;
    min-width: 24px;
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0;
}}

/* ── QScrollArea ─────────────────────────────────────────────────────── */

QScrollArea {{
    background: transparent;
    border: none;
}}
QScrollArea > QWidget > QWidget {{
    background: transparent;
}}

/* ── Текстовый редактор (логи) ───────────────────────────────────────── */

QTextEdit {{
    background-color: {C['bg_card']};
    border: 1px solid {C['border']};
    border-radius: 10px;
    color: {C['text_primary']};
    font-family: "JetBrains Mono", "Cascadia Code", "Fira Code", monospace;
    font-size: 12px;
    padding: 12px;
    selection-background-color: {C['accent_dim']};
}}

/* ── Тултипы ─────────────────────────────────────────────────────────── */

QToolTip {{
    background-color: {C['bg_card']};
    color: {C['text_primary']};
    border: 1px solid {C['border']};
    border-radius: 6px;
    padding: 5px 10px;
    font-size: 12px;
}}

/* ── Диалоги ─────────────────────────────────────────────────────────── */

QMessageBox {{
    background-color: {C['bg_card']};
}}
QMessageBox QLabel {{
    color: {C['text_primary']};
    font-size: 13px;
}}
QMessageBox QPushButton {{
    min-width: 80px;
}}
"""
