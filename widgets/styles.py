COLORS = {
    # ── Фоны ──────────────────────────────────────────────────────────
    "bg_window":      "#080B10",   # глубокий чёрный, основной фон
    "bg_panel":       "#0C1018",   # боковая панель
    "bg_card":        "#0E1420",   # карточки / поверхности
    "bg_input":       "#111827",   # поля ввода
    "bg_hover":       "#1A2333",   # hover-состояния
    "bg_status":      "#0A1510",   # фон карточки статуса (зелёный тинт)

    # ── Границы ───────────────────────────────────────────────────────
    "border":         "#1A2030",   # базовая граница
    "border_focus":   "#4A90E2",   # фокус / акцент синий
    "border_success": "#1E3820",   # граница карточки статуса

    # ── Текст ─────────────────────────────────────────────────────────
    "text_primary":   "#E2E8F4",
    "text_secondary": "#5A7A9E",
    "text_muted":     "#2D3D50",

    # ── Акцент (Download / синий) ──────────────────────────────────────
    "accent":         "#4A90E2",
    "accent_hover":   "#6AAEF5",
    "accent_dim":     "#0D1E3A",

    # ── Успех (Upload / зелёный) ───────────────────────────────────────
    "success":        "#2ECC71",
    "success_dim":    "#0A1510",
    "success_hover":  "#4ADE88",
    "success_border": "#1E3820",

    # ── Опасность ─────────────────────────────────────────────────────
    "danger":         "#E05050",
    "danger_dim":     "#200A0A",
    "danger_hover":   "#F07070",
    "danger_border":  "#5A1A1A",

    # ── Предупреждение ─────────────────────────────────────────────────
    "warning":        "#E3B341",
    "warning_dim":    "#1E1608",
}

C = COLORS


def get_stylesheet() -> str:
    return f"""

/* ── Базовые ──────────────────────────────────────────────────────────── */

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

/* ── Левая панель ─────────────────────────────────────────────────────── */

QFrame#sidebar {{
    background-color: {C['bg_panel']};
    border-right: 1px solid {C['border']};
}}

/* ── Логотип-бар ──────────────────────────────────────────────────────── */

QFrame#logo_bar {{
    background-color: {C['bg_panel']};
    border-bottom: 1px solid {C['border']};
    padding: 0 16px;
    min-height: 54px;
    max-height: 54px;
}}

QLabel#app_title {{
    font-size: 14px;
    font-weight: 600;
    color: {C['text_primary']};
    letter-spacing: 0.3px;
    background: transparent;
}}

QFrame#logo_icon {{
    background-color: #1A4FD8;
    border-radius: 7px;
    min-width: 30px;
    max-width: 30px;
    min-height: 30px;
    max-height: 30px;
}}

/* ── Карточка статуса ────────────────────────────────────────────────── */

QFrame#status_card {{
    background-color: {C['bg_status']};
    border: 1px solid {C['border_success']};
    border-radius: 8px;
    margin: 12px;
    padding: 4px;
}}

QFrame#status_card_inactive {{
    background-color: {C['bg_card']};
    border: 1px solid {C['border']};
    border-radius: 8px;
    margin: 12px;
    padding: 4px;
}}

/* ── Карточки ─────────────────────────────────────────────────────────── */

QFrame#card {{
    background-color: {C['bg_card']};
    border: 1px solid {C['border']};
    border-radius: 10px;
}}

QFrame#card_rx {{
    background-color: {C['bg_card']};
    border: 1px solid {C['border']};
    border-left: 3px solid {C['accent']};
    border-radius: 10px;
}}

QFrame#card_tx {{
    background-color: {C['bg_card']};
    border: 1px solid {C['border']};
    border-left: 3px solid {C['success']};
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

/* ── Метки ────────────────────────────────────────────────────────────── */

QLabel {{
    background: transparent;
    color: {C['text_primary']};
}}

QLabel#page_title {{
    font-size: 15px;
    font-weight: 700;
    color: {C['text_muted']};
    letter-spacing: 1.5px;
    background: transparent;
    text-transform: uppercase;
}}

QLabel#subtitle {{
    font-size: 12px;
    color: {C['text_secondary']};
    background: transparent;
}}

QLabel#section_header {{
    font-size: 9px;
    font-weight: 700;
    color: {C['text_muted']};
    letter-spacing: 1.5px;
    text-transform: uppercase;
    background: transparent;
    padding: 0 16px;
}}

QLabel#status_active {{
    font-size: 11px;
    font-weight: 700;
    color: {C['success']};
    letter-spacing: 1px;
    text-transform: uppercase;
    background: transparent;
}}

QLabel#status_inactive {{
    font-size: 11px;
    font-weight: 700;
    color: {C['text_secondary']};
    letter-spacing: 1px;
    text-transform: uppercase;
    background: transparent;
}}

QLabel#status_busy {{
    font-size: 11px;
    font-weight: 700;
    color: {C['warning']};
    letter-spacing: 1px;
    text-transform: uppercase;
    background: transparent;
}}

QLabel#big_value {{
    font-size: 26px;
    font-weight: 700;
    letter-spacing: -0.5px;
    font-family: "JetBrains Mono", "Cascadia Code", "Courier New", monospace;
    background: transparent;
}}

QLabel#big_value_rx {{
    font-size: 26px;
    font-weight: 700;
    letter-spacing: -0.5px;
    font-family: "JetBrains Mono", "Cascadia Code", "Courier New", monospace;
    color: {C['accent']};
    background: transparent;
}}

QLabel#big_value_tx {{
    font-size: 26px;
    font-weight: 700;
    letter-spacing: -0.5px;
    font-family: "JetBrains Mono", "Cascadia Code", "Courier New", monospace;
    color: {C['success']};
    background: transparent;
}}

QLabel#small_label {{
    font-size: 10px;
    color: {C['text_muted']};
    letter-spacing: 0.8px;
    text-transform: uppercase;
    background: transparent;
}}

QLabel#error_label {{
    color: {C['danger']};
    font-size: 12px;
    background: transparent;
    padding: 4px 0;
}}

QLabel#info_key {{
    font-size: 11px;
    color: {C['text_muted']};
    background: transparent;
}}

QLabel#info_val {{
    font-size: 11px;
    color: {C['text_secondary']};
    font-weight: 500;
    background: transparent;
}}

/* ── Кнопки ───────────────────────────────────────────────────────────── */

QPushButton {{
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 13px;
    font-weight: 500;
    border: none;
    min-height: 10px;
}}

QPushButton#btn_start {{
    background-color: {C['success_dim']};
    color: {C['success']};
    font-size: 13px;
    font-weight: 600;
    padding: 9px 20px;
    border-radius: 8px;
    border: 1px solid {C['success_border']};
    min-height: 10px;
}}
QPushButton#btn_start:hover {{
    background-color: #0F2015;
    border-color: {C['success']};
    color: {C['success_hover']};
}}
QPushButton#btn_start:pressed {{
    background-color: {C['success_dim']};
}}
QPushButton#btn_start:disabled {{
    background-color: {C['bg_card']};
    color: {C['text_muted']};
    border-color: {C['border']};
}}

QPushButton#btn_stop {{
    background-color: {C['danger_dim']};
    color: {C['danger']};
    font-size: 13px;
    font-weight: 600;
    padding: 9px 20px;
    border-radius: 8px;
    border: 1px solid {C['danger_border']};
    min-height: 10px;
}}
QPushButton#btn_stop:hover {{
    background-color: #2A1010;
    border-color: {C['danger']};
    color: {C['danger_hover']};
}}
QPushButton#btn_stop:pressed {{
    background-color: {C['danger_dim']};
}}
QPushButton#btn_stop:disabled {{
    background-color: {C['bg_card']};
    color: {C['text_muted']};
    border-color: {C['border']};
}}

QPushButton#btn_primary {{
    background-color: {C['accent_dim']};
    color: {C['accent']};
    border: 1px solid #1A3A6A;
}}
QPushButton#btn_primary:hover {{
    background-color: #0F2545;
    border-color: {C['accent']};
    color: {C['accent_hover']};
}}
QPushButton#btn_primary:disabled {{
    background-color: {C['bg_card']};
    color: {C['text_muted']};
    border-color: {C['border']};
}}

QPushButton#btn_secondary {{
    background-color: {C['bg_card']};
    color: {C['text_secondary']};
    border: 1px solid {C['border']};
    border-radius: 7px;
    padding: 7px 14px;
    min-height: 32px;
}}
QPushButton#btn_secondary:hover {{
    background-color: {C['bg_hover']};
    color: {C['text_primary']};
    border-color: {C['text_muted']};
}}
QPushButton#btn_secondary:pressed {{
    background-color: {C['bg_input']};
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
}}
QPushButton#btn_icon:hover {{
    background-color: {C['bg_hover']};
    color: {C['text_primary']};
}}

/* ── Поля ввода ───────────────────────────────────────────────────────── */

QLineEdit {{
    background-color: {C['bg_input']};
    border: 1px solid {C['border']};
    border-radius: 7px;
    padding: 7px 10px;
    color: {C['text_secondary']};
    font-size: 12px;
    font-family: "JetBrains Mono", "Courier New", monospace;
    selection-background-color: {C['accent_dim']};
    selection-color: {C['accent']};
    min-height: 15px;
}}
QLineEdit:focus {{
    border-color: {C['border_focus']};
    background-color: {C['bg_card']};
    color: {C['text_primary']};
}}
QLineEdit:disabled {{
    color: {C['text_muted']};
    background-color: {C['bg_window']};
    border-color: {C['border']};
}}

/* ── Комбобокс ────────────────────────────────────────────────────────── */

QComboBox {{
    background-color: {C['bg_input']};
    border: 1px solid {C['border']};
    border-radius: 7px;
    padding: 7px 10px;
    color: {C['text_secondary']};
    font-size: 12px;
    min-height: 32px;
    selection-background-color: transparent;
}}
QComboBox:focus {{
    border-color: {C['border_focus']};
    color: {C['text_primary']};
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
    border-top: 5px solid {C['text_muted']};
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
    min-height: 28px;
}}
QComboBox QAbstractItemView::item:selected {{
    background-color: {C['accent_dim']};
    color: {C['accent']};
}}

/* ── Вкладки ──────────────────────────────────────────────────────────── */

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
    color: {C['text_muted']};
    padding: 13px 20px;
    font-size: 12px;
    font-weight: 500;
    border: none;
    border-bottom: 2px solid transparent;
    letter-spacing: 0.2px;
}}
QTabBar::tab:selected {{
    color: {C['accent']};
    border-bottom: 2px solid {C['accent']};
    font-weight: 600;
}}
QTabBar::tab:hover:!selected {{
    color: {C['text_secondary']};
    background-color: {C['bg_hover']};
}}

/* ── Таблица устройств ────────────────────────────────────────────────── */

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
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 1.2px;
    text-transform: uppercase;
}}
QHeaderView::section:first {{
    border-top-left-radius: 10px;
}}
QHeaderView::section:last {{
    border-top-right-radius: 10px;
}}

/* ── Скроллбар ────────────────────────────────────────────────────────── */

QScrollBar:vertical {{
    background: transparent;
    width: 4px;
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
    height: 4px;
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

/* ── QScrollArea ──────────────────────────────────────────────────────── */

QScrollArea {{
    background: transparent;
    border: none;
}}
QScrollArea > QWidget > QWidget {{
    background: transparent;
}}

/* ── Текстовый редактор (логи) ────────────────────────────────────────── */

QTextEdit {{
    background-color: {C['bg_card']};
    border: 1px solid {C['border']};
    border-radius: 10px;
    color: {C['text_primary']};
    font-family: "JetBrains Mono", "Cascadia Code", "Fira Code", monospace;
    font-size: 12px;
    padding: 14px;
    selection-background-color: {C['accent_dim']};
    line-height: 1.6;
}}

/* ── Тултипы ──────────────────────────────────────────────────────────── */

QToolTip {{
    background-color: {C['bg_card']};
    color: {C['text_primary']};
    border: 1px solid {C['border']};
    border-radius: 6px;
    padding: 5px 10px;
    font-size: 12px;
}}

/* ── Диалоги ──────────────────────────────────────────────────────────── */

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