"""
themes.py
=========
Plik z motywami dla aplikacji - wszystkie style w jednym miejscu.
"""

LIGHT_THEME = {
    "placeholder": {
        "text_color": "#666",
        "text_style": "font-size: 22px; color: #666; font-weight: bold; font-style: italic"
    },

    "price_summary": {
        "min_height": 120,
        "max_height": 300,
        "margins": (10, 20, 30, 10),
        "spacing": 5,
        "border": "radius: 10px",
        "background": "white",
        "text_color": "#333",
        "border_color": "#000",

        # Nazwa spółki (większa)
        "symbol_style": "font-size: 32px; color: #333; font-weight: bold; border: none;",

        # Tytuły cen (Current Price, Predicted Price)
        "label_style": "font-size: 18px; color: #666; font-weight: bold; border: none;",

        # Wartości cen (neutralne)
        "value_style": "font-size: 24px; color: #333; font-weight: bold; border: none;",

        # Przewidywana cena (wzrost)
        "positive_style": "font-size: 24px; color: #00cc00; font-weight: bold; border: none;",

        # Przewidywana cena (spadek)
        "negative_style": "font-size: 24px; color: #cc0000; font-weight: bold; border: none;"
    },

    "chart": {
        "bg_color": "white",
        "text_color": "#333",
        "font-style": "italic",
        "prediction_color": "gold",
        "min_width": 10,
        "min_height": 6,
        "margins": {
            "left": 0.08,
            "right": 0.98,
            "top": 0.95,
            "bottom": 0.08
        },
        "prediction_marker": {
            "size": 200,
            "marker": "*"
        },
        "mpf_colors": {
            "up": "#00aa00",
            "down": "#cc0000",
            "wick": "#333",
            "edge": "#333",
            "volume": "in"
        },
        "mpf_style_base": "yahoo",
        "mpf_style_config": {
            "gridcolor": "rgba(221, 221, 221, 0.8)",
            "gridstyle": "--",
            "facecolor": "white",
            "edgecolor": "#333",
            "figcolor": "white"
        }
    },

    "fallback_chart": {
        "bg_color": "white",
        "text_color": "#333",
        "line_color": "#0066cc",
        "prediction_color": "gold",
        "prediction_edge": "orange"
    },

    "label": {
        "style": "font-size: 15px; font-weight: bold; color: #333333;"
    },

    "lineedit_style": """
        QLineEdit {
            border: 1px solid #cccccc;
            border-radius: 4px;
            background: #ffffff;
            color: #333333;
            font-size: 16px;
            padding: 8px;
        }
    """,

    "combobox_style": """
        QComboBox {
            background-color: #ffffff;
            border: 1px solid #cccccc;
            border-radius: 4px;
            color: #333333;
            font-size: 16px;
            padding: 8px;
        }
        QComboBox QAbstractItemView {
            background-color: #ffffff;
            border: 1px solid #cccccc;
            selection-background-color: #f0f0f0;
            selection-color: #000000;
            font-size: 15px;
        }
    """,

    "button_style": """
        QPushButton {
            font-size: 15px;
            font-weight: bold;
            padding: 10px 16px;
            border-radius: 6px;
            background-color: #d6d6c2;
            color: #333333;
            border: none;
        }
        QPushButton:hover {
            background-color: #c5c5b0;
        }
        QPushButton:pressed {
            background-color: #b5b5a0;
        }
        QPushButton:disabled {
            background-color: #e0e0e0;
            color: #999999;
        }
    """,

    # Style dla Home Page
    "home_card": {
        "style": """
        QFrame#Card {
            background-color: #ffffff;
            border: 2px solid #000000;
            border-radius: 15px;
        }
    """
    },
    "home_text_primary": {"style": "color: #000000; font-weight: bold; font-size: 16px;"},
    "home_text_secondary": {"style": "color: #333333; font-size: 15px;"},
    "home_header": {"style": "color: #000000; font-size: 24px; font-weight: 900; letter-spacing: 1px;"},

    "home_btn_outline": {
        "style": """
        QPushButton {
            background-color: transparent;
            color: #000000;
            border: 2px solid #000000;
            border-radius: 25px;
            font-size: 18px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #000000;
            color: #ffffff;
        }
    """
    },
    "home_btn_action": {
        "style": """
        QPushButton {
            background-color: transparent;
            color: #000000;
            border: none;
            font-size: 16px;
            font-weight: bold;
        }
        QPushButton:hover { color: #666; }
    """
    },
}

DARK_THEME = {
    "placeholder": {
        "text_color": "white",
        "text_style": "font-size: 22px; color: white; font-weight: bold; font-style: italic;"
    },

    "price_summary": {
        "min_height": 120,
        "max_height": 300,
        "margins": (10, 20, 30, 10),
        "spacing": 5,
        "border": "radius: 10px",
        "background": "#2b2b2b",
        "text_color": "white",
        "border_color": "#444",

        # Nazwa spółki (większa)
        "symbol_style": "font-size: 32px; color: white; font-weight: bold; border: none;",

        # Tytuły cen (Current Price, Predicted Price)
        "label_style": "font-size: 18px; color: #aaa; font-weight: bold; border: none;",

        # Wartości cen (neutralne)
        "value_style": "font-size: 24px; color: white; font-weight: bold; border: none;",

        # Przewidywana cena (wzrost)
        "positive_style": "font-size: 24px; color: #00cc00; font-weight: bold; border: none;",

        # Przewidywana cena (spadek)
        "negative_style": "font-size: 24px; color: #cc0000; font-weight: bold; border: none;"
    },

    "chart": {
        "bg_color": "#1e1e1e",
        "text_color": "#ffffff",
        "font-style": "italic",
        "prediction_color": "gold",
        "min_width": 10,
        "min_height": 6,
        "margins": {
            "left": 0.08,
            "right": 0.98,
            "top": 0.95,
            "bottom": 0.08
        },
        "prediction_marker": {
            "size": 200,
            "marker": "*"
        },
        "mpf_colors": {
            "up": "#00aa00",
            "down": "#cc0000",
            "wick": "#333",
            "edge": "#333",
            "volume": "in"
        },
        "mpf_style_base": "yahoo",
        "mpf_style_config": {
            "gridcolor": "#1e1e1e",
            "facecolor": "#1e1e1e",
            "edgecolor": "#eeeeee",
            "figcolor": "#1e1e1e"
        }
    },

    "fallback_chart": {
        "bg_color": "#1e1e1e",
        "text_color": "white",
        "line_color": "#0066cc",
        "prediction_color": "gold",
        "prediction_edge": "orange"
    },

    "label": {
        "style": "font-size: 15px; font-weight: bold; color: #ffffff;"
    },

    "lineedit_style": """
        QLineEdit {
            border: 1px solid #555555;
            border-radius: 4px;
            background: #2b2b2b;
            color: #ffffff;
            font-size: 16px;
            padding: 8px;
        }
    """,

    "combobox_style": """
        QComboBox {
            background-color: #2b2b2b;
            border: 1px solid #555555;
            border-radius: 4px;
            color: #ffffff;
            font-size: 16px;
            padding: 8px;
        }
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 18px;
            border-left: 1px solid #555555;
        }
        QComboBox::down-arrow {
            image: none;
            width: 8px;
            height: 8px;
        }
        QComboBox QAbstractItemView {
            background-color: #2b2b2b;
            border: 1px solid #555555;
            selection-background-color: #444444;
            selection-color: #ffffff;
            font-size: 15px;
        }
    """,

    "button_style": """
        QPushButton {
            font-size: 15px;
            font-weight: bold;
            padding: 10px 16px;
            border-radius: 6px;
            background-color: #444444;
            color: #ffffff;
            border: none;
        }
        QPushButton:hover {
            background-color: #555555;
        }
        QPushButton:pressed {
            background-color: #666666;
        }
        QPushButton:disabled {
            background-color: #333333;
            color: #777777;
        }
    """,

    # Style dla Home Page
    "home_card": {
        "style": """
        QFrame#Card {
            background-color: #1e1e1e;
            border: 2px solid #444444;
            border-radius: 15px;
        }
    """
    },
    "home_text_primary": {"style": "color: #ffffff; font-weight: bold; font-size: 16px;"},
    "home_text_secondary": {"style": "color: #cccccc; font-size: 15px;"},
    "home_header": {"style": "color: #ffffff; font-size: 24px; font-weight: 900; letter-spacing: 1px;"},

    "home_btn_outline": {
        "style": """
        QPushButton {
            background-color: transparent;
            color: #ffffff;
            border: 2px solid #ffffff;
            border-radius: 25px;
            font-size: 18px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #ffffff;
            color: #000000;
        }
    """
    },
    "home_btn_action": {
        "style": """
        QPushButton {
            background-color: transparent;
            color: #ffffff;
            border: none;
            font-size: 16px;
            font-weight: bold;
        }
        QPushButton:hover { color: #aaa; }
    """
    },
}
