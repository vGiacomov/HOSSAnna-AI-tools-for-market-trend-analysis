# App/themes.py

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
    "nav_menu": """
        QFrame {
            background-color: #d6d6c2;
            border-right: 1px solid #e0e0e0;
            border-radius: 15px;
            margin:  25 0 25; 

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
            background-color: #d6d6c2;
        }
    """,

                  "panel_style": {
    "style": """
        QGroupBox {
            background-color: #ffffff;
            border: 1px solid rgba(0, 0, 0, 0.08); /* Bardzo delikatna czarna ramka (8%) */
            border-radius: 12px;
        }
    """
},


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

    "nav_menu": """
    QFrame {
        background-color: #2b2b2b;
        border-right: 1px solid #1a1a1a;
        border-radius: 15px;
        margin:  25 0 25; 
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

    "panel_style": {
        "style": """
        QGroupBox {
            background-color: #1e1e1e; /* Tło modułu */
            border: 1px solid rgba(255, 255, 255, 0.08); /* Bardzo delikatna biała ramka (8%) */
            border-radius: 12px;
        }
    """
    },

}
