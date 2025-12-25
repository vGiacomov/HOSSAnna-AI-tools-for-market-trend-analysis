LIGHT_THEME = {
    "main": """
        QWidget {
            background-color: white;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        QLabel {
            color: #333;
        }
        QPushButton {
            background-color: #d6d6c2;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 14px;
            color: #333;
            min-width: 120px;
        }
        QPushButton:hover {
            background-color: #c5c5b0;
        }
        QPushButton:pressed {
            background-color: #b5b5a0;
        }
        QPushButton:disabled {
            background-color: #e0e0e0;
            color: #999;
        }
    """,

    "frame": """
        QFrame {
            background-color: #f5f5f5;
            border-radius: 5px;
        }
    """,

    "dialog": """
        QDialog {
            background-color: white;
        }
    """,

    "combobox": """
        QComboBox {
            font-size: 14px;
            padding: 8px;
            border: 2px solid #ccc;
            border-radius: 5px;
            background-color: white;
            color: #333;
            min-width: 200px;
        }
        QComboBox:hover {
            border: 2px solid #d6d6c2;
        }
        QComboBox::drop-down {
            border: none;
            width: 30px;
        }
        QComboBox QAbstractItemView {
            background-color: white;
            color: #333;
            selection-background-color: #d6d6c2;
        }
    """,

    "checkbox": """
        QCheckBox {
            spacing: 10px;
            color: #333;
        }
        QCheckBox::indicator {
            width: 20px;
            height: 20px;
            border-radius: 3px;
            border: 2px solid #ccc;
            background-color: white;
        }
        QCheckBox::indicator:checked {
            background-color: #d6d6c2;
            border-color: #b5b5a0;
        }
    """,

    "theme_switch": """
        QCheckBox {
            spacing: 0px;
        }
        QCheckBox::indicator {
            width: 60px;
            height: 30px;
            border-radius: 15px;
            background-color: #ccc;
        }
        QCheckBox::indicator:checked {
            background-color: #4a4a4a;
        }
        QCheckBox::indicator:unchecked {
            background-color: #d6d6c2;
        }
    """,

    "nav_menu": """
        QFrame {
            background-color: #d6d6c2;
            border-right: 1px solid #e0e0e0;
            border-radius: 15px;
            margin: 25px 0px 25px 0px;
        }
    """,

    "nav_button": """
        QPushButton {
            background-color: transparent;
            border: none;
            border-radius: 8px;
            padding: 8px;
            min-width: 40px;
            min-height: 40px;
            max-width: 40px;
            max-height: 40px;
        }
        QPushButton:hover {
            background-color: #e8e8e8;
        }
        QPushButton:pressed {
            background-color: #c5c5b0;
        }
    """,

    "panel": """
        QGroupBox {
            background-color: #ffffff;
            border: 1px solid rgba(0, 0, 0, 0.08);
            border-radius: 12px;
            padding: 15px;
            margin-top: 10px;
        }
        QGroupBox::title {
            color: #333;
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 5px;
            font-weight: bold;
        }
    """,

    "scrollarea": """
        QScrollArea {
            background-color: white;
            border: none;
        }
        QScrollBar:vertical {
            background-color: #f5f5f5;
            width: 12px;
            border-radius: 6px;
        }
        QScrollBar::handle:vertical {
            background-color: #d6d6c2;
            border-radius: 6px;
            min-height: 20px;
        }
        QScrollBar::handle:vertical:hover {
            background-color: #c5c5b0;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        QScrollBar:horizontal {
            background-color: #f5f5f5;
            height: 12px;
            border-radius: 6px;
        }
        QScrollBar::handle:horizontal {
            background-color: #d6d6c2;
            border-radius: 6px;
            min-width: 20px;
        }
        QScrollBar::handle:horizontal:hover {
            background-color: #c5c5b0;
        }
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            width: 0px;
        }
    """,

    "lineedit": """
        QLineEdit {
            background-color: white;
            border: 2px solid #ccc;
            border-radius: 5px;
            padding: 8px;
            font-size: 14px;
            color: #333;
        }
        QLineEdit:focus {
            border: 2px solid #d6d6c2;
        }
        QLineEdit:disabled {
            background-color: #f5f5f5;
            color: #999;
        }
    """,

    "textedit": """
        QTextEdit, QPlainTextEdit {
            background-color: white;
            border: 2px solid #ccc;
            border-radius: 5px;
            padding: 8px;
            font-size: 14px;
            color: #333;
        }
        QTextEdit:focus, QPlainTextEdit:focus {
            border: 2px solid #d6d6c2;
        }
    """,

    "table": """
        QTableWidget, QTableView {
            background-color: white;
            alternate-background-color: #f9f9f9;
            gridline-color: #e0e0e0;
            border: 1px solid #ccc;
            border-radius: 5px;
            color: #333;
        }
        QTableWidget::item, QTableView::item {
            padding: 5px;
        }
        QTableWidget::item:selected, QTableView::item:selected {
            background-color: #d6d6c2;
            color: #333;
        }
        QHeaderView::section {
            background-color: #f5f5f5;
            color: #333;
            padding: 8px;
            border: none;
            border-bottom: 2px solid #d6d6c2;
            font-weight: bold;
        }
    """,

    "tooltip": """
        QToolTip {
            background-color: #333;
            color: white;
            border: 1px solid #555;
            padding: 5px;
            border-radius: 3px;
        }
    """,
}

DARK_THEME = {
    "main": """
        QWidget {
            background-color: #1e1e1e;
            color: white;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        QLabel {
            color: white;
        }
        QPushButton {
            background-color: #444;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 14px;
            color: white;
            min-width: 120px;
        }
        QPushButton:hover {
            background-color: #555;
        }
        QPushButton:pressed {
            background-color: #666;
        }
        QPushButton:disabled {
            background-color: #333;
            color: #777;
        }
    """,

    "frame": """
        QFrame {
            background-color: #2b2b2b;
            border-radius: 5px;
        }
    """,

    "dialog": """
        QDialog {
            background-color: #1e1e1e;
        }
    """,

    "combobox": """
        QComboBox {
            font-size: 14px;
            padding: 8px;
            border: 2px solid #555;
            border-radius: 5px;
            background-color: #2b2b2b;
            color: white;
            min-width: 200px;
        }
        QComboBox:hover {
            border: 2px solid #777;
        }
        QComboBox::drop-down {
            border: none;
            width: 30px;
        }
        QComboBox QAbstractItemView {
            background-color: #2b2b2b;
            color: white;
            selection-background-color: #444;
        }
    """,

    "checkbox": """
        QCheckBox {
            spacing: 10px;
            color: white;
        }
        QCheckBox::indicator {
            width: 20px;
            height: 20px;
            border-radius: 3px;
            border: 2px solid #555;
            background-color: #2b2b2b;
        }
        QCheckBox::indicator:checked {
            background-color: #666;
            border-color: #888;
        }
    """,

    "theme_switch": """
        QCheckBox {
            spacing: 0px;
        }
        QCheckBox::indicator {
            width: 60px;
            height: 30px;
            border-radius: 15px;
            background-color: #555;
        }
        QCheckBox::indicator:checked {
            background-color: #999;
        }
        QCheckBox::indicator:unchecked {
            background-color: #666;
        }
    """,

    "nav_menu": """
        QFrame {
            background-color: #2b2b2b;
            border-right: 1px solid #1a1a1a;
            border-radius: 15px;
            margin: 25px 0px 25px 0px;
        }
    """,

    "nav_button": """
        QPushButton {
            background-color: transparent;
            border: none;
            border-radius: 8px;
            padding: 8px;
            min-width: 40px;
            min-height: 40px;
            max-width: 40px;
            max-height: 40px;
        }
        QPushButton:hover {
            background-color: #3a3a3a;
        }
        QPushButton:pressed {
            background-color: #4a4a4a;
        }
    """,

    "panel": """
        QGroupBox {
            background-color: #1e1e1e;
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 15px;
            margin-top: 10px;
        }
        QGroupBox::title {
            color: white;
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 5px;
            font-weight: bold;
        }
    """,

    "scrollarea": """
        QScrollArea {
            background-color: #1e1e1e;
            border: none;
        }
        QScrollBar:vertical {
            background-color: #2b2b2b;
            width: 12px;
            border-radius: 6px;
        }
        QScrollBar::handle:vertical {
            background-color: #444;
            border-radius: 6px;
            min-height: 20px;
        }
        QScrollBar::handle:vertical:hover {
            background-color: #555;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        QScrollBar:horizontal {
            background-color: #2b2b2b;
            height: 12px;
            border-radius: 6px;
        }
        QScrollBar::handle:horizontal {
            background-color: #444;
            border-radius: 6px;
            min-width: 20px;
        }
        QScrollBar::handle:horizontal:hover {
            background-color: #555;
        }
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            width: 0px;
        }
    """,

    "lineedit": """
        QLineEdit {
            background-color: #2b2b2b;
            border: 2px solid #555;
            border-radius: 5px;
            padding: 8px;
            font-size: 14px;
            color: white;
        }
        QLineEdit:focus {
            border: 2px solid #777;
        }
        QLineEdit:disabled {
            background-color: #1e1e1e;
            color: #666;
        }
    """,

    "textedit": """
        QTextEdit, QPlainTextEdit {
            background-color: #2b2b2b;
            border: 2px solid #555;
            border-radius: 5px;
            padding: 8px;
            font-size: 14px;
            color: white;
        }
        QTextEdit:focus, QPlainTextEdit:focus {
            border: 2px solid #777;
        }
    """,

    "table": """
        QTableWidget, QTableView {
            background-color: #1e1e1e;
            alternate-background-color: #2b2b2b;
            gridline-color: #444;
            border: 1px solid #555;
            border-radius: 5px;
            color: white;
        }
        QTableWidget::item, QTableView::item {
            padding: 5px;
        }
        QTableWidget::item:selected, QTableView::item:selected {
            background-color: #444;
            color: white;
        }
        QHeaderView::section {
            background-color: #2b2b2b;
            color: white;
            padding: 8px;
            border: none;
            border-bottom: 2px solid #555;
            font-weight: bold;
        }
    """,

    "tooltip": """
        QToolTip {
            background-color: #f5f5f5;
            color: #333;
            border: 1px solid #ccc;
            padding: 5px;
            border-radius: 3px;
        }
    """,
}
