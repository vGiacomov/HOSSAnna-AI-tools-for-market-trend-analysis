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

    "combobox": """
        QComboBox {
            font-size: 16px;
            padding: 10px;
            border: 2px solid #ccc;
            border-radius: 5px;
            background-color: white;
            min-width: 300px;
        }
        QComboBox:hover {
            border: 2px solid #d6d6c2;
        }
        QComboBox::drop-down {
            border: none;
            width: 30px;
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

    "checkbox_accept": """
        QCheckBox {
            font-size: 14px;
            color: #333;
            font-weight: bold;
        }
        QCheckBox:disabled {
            color: #999;
        }
        QCheckBox:enabled {
            color: #008800;
        }
    """,

    "textedit": """
        QTextEdit {
            border: 2px solid #ccc;
            border-radius: 5px;
            padding: 10px;
            font-size: 12px;
            background-color: #f9f9f9;
        }
    """,

    "finish_button": """
        QPushButton {
            background-color: #d6d6c2;
            font-size: 16px;
            font-weight: bold;
            padding: 15px 30px;
            min-width: 200px;
        }
        QPushButton:hover {
            background-color: #c5c5b0;
        }
    """
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

    "combobox": """
        QComboBox {
            font-size: 16px;
            padding: 10px;
            border: 2px solid #555;
            border-radius: 5px;
            background-color: #2b2b2b;
            color: white;
            min-width: 300px;
        }
        QComboBox:hover {
            border: 2px solid #777;
        }
        QComboBox::drop-down {
            border: none;
            width: 30px;
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

    "checkbox_accept": """
        QCheckBox {
            font-size: 14px;
            color: #cccccc;
            font-weight: bold;
        }
        QCheckBox:disabled {
            color: #777;
        }
        QCheckBox:enabled {
            color: #55ff55;
        }
    """,

    "textedit": """
        QTextEdit {
            border: 2px solid #555;
            border-radius: 5px;
            padding: 10px;
            font-size: 12px;
            background-color: #2b2b2b;
            color: white;
        }
    """,

    "finish_button": """
        QPushButton {
            background-color: #444;
            font-size: 16px;
            font-weight: bold;
            padding: 15px 30px;
            min-width: 200px;
            color: white;
        }
        QPushButton:hover {
            background-color: #555;
        }
    """
}