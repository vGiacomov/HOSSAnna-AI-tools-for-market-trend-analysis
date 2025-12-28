"""
Motywy dla strony głównej HOSSAnna
Dopasowane do głównej palety aplikacji - beżowo-szara gama
"""

# Kolory zgodne z głównym motywem aplikacji
BEIGE_PRIMARY = "#d6d6c2"     # Główny beżowy
BEIGE_HOVER = "#c5c5b0"       # Ciemniejszy beżowy (hover)
BEIGE_PRESSED = "#b5b5a0"     # Jeszcze ciemniejszy (pressed)
GRAY_LIGHT = "#f5f5f5"        # Jasny szary
GRAY_BORDER = "#e0e0e0"       # Szara ramka
GREEN_POSITIVE = "#16C784"    # Zielony dla dodatnich zmian
RED_NEGATIVE = "#EA3943"      # Czerwony dla ujemnych zmian

LIGHT_THEME = {
    # Główna karta (Card)
    "card": """
        QFrame#Card {
            background-color: #FFFFFF;
            border: 1px solid #e0e0e0;
            border-radius: 12px;
        }
    """,

    # Nagłówki sekcji
    "section_header": """
        font-size: 18px;
        font-weight: 600;
        color: #333;
        border: none;
        padding: 5px 0px;
    """,

    # Przyciski akcji (dodawanie)
    "add_button": """
        QPushButton {
            background-color: transparent;
            color: #333;
            border: 1.5px solid #d6d6c2;
            border-radius: 15px;
            font-weight: bold;
            font-size: 18px;
        }
        QPushButton:hover {
            background-color: #d6d6c2;
        }
        QPushButton:pressed {
            background-color: #c5c5b0;
        }
    """,

    # Market Item Widget (wiersz z akcją)
    "market_item": """
        QFrame#ItemFrame {
            background-color: transparent;
            border: 1px solid #f5f5f5;
            border-radius: 6px;
            padding: 2px;
        }
        QFrame#ItemFrame:hover {
            background-color: #f9f9f9;
            border: 1px solid #e0e0e0;
        }
    """,

    # Symbol tickera
    "ticker_symbol": """
        font-weight: 600;
        font-size: 14px;
        color: #333;
        border: none;
    """,

    # Cena
    "price_label": """
        font-size: 14px;
        color: #333;
        border: none;
        font-weight: 500;
    """,

    # Przycisk usuwania
    "remove_button": """
        QPushButton {
            background-color: transparent;
            color: #EA3943;
            border: 1px solid #EA3943;
            border-radius: 12px;
            font-weight: bold;
            font-size: 16px;
            min-width: 25px;
            max-width: 25px;
            min-height: 25px;
            max-height: 25px;
            padding: 0px;
            margin: 0px;
        }
        QPushButton:hover {
            background-color: rgba(234, 57, 67, 0.1);
        }
    """,

    # Welcome Panel - przyciski akcji
    "action_button": """
        QPushButton {
            background-color: #d6d6c2;
            color: #333;
            border: none;
            border-radius: 8px;
            padding: 12px;
            font-weight: 600;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #c5c5b0;
        }
        QPushButton:pressed {
            background-color: #b5b5a0;
        }
    """,

    # Statystyki rynkowe (małe widgety)
    "stats_widget": """
        QFrame#StatWidget {
            background-color: #f5f5f5;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
        }
        QFrame#StatWidget:hover {
            background-color: #f0f0f0;
            border: 1px solid #d0d0d0;
        }
    """,

    # Info widget (status systemu)
    "info_widget": """
        QFrame#InfoWidget {
            background-color: #f5f5f5;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
        }
    """,

    # Etykiety wartości
    "value_label": """
        font-size: 16px;
        font-weight: 600;
        color: #333;
        border: none;
    """,

    # Tytuły w stats widget
    "stats_title": """
        font-size: 11px;
        color: #666;
        border: none;
        font-weight: 500;
    """,

    # ScrollArea
    "scroll_area": """
        QScrollArea {
            background: transparent;
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
    """,

    # Kolory zmian
    "positive_color": GREEN_POSITIVE,
    "negative_color": RED_NEGATIVE,
}


DARK_THEME = {
    # Główna karta (Card)
    "card": """
        QFrame#Card {
            background-color: #1e1e1e;
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
        }
    """,

    # Nagłówki sekcji
    "section_header": """
        font-size: 18px;
        font-weight: 600;
        color: white;
        border: none;
        padding: 5px 0px;
    """,

    # Przyciski akcji (dodawanie)
    "add_button": """
        QPushButton {
            background-color: transparent;
            color: white;
            border: 1.5px solid #666;
            border-radius: 15px;
            font-weight: bold;
            font-size: 18px;
        }
        QPushButton:hover {
            background-color: #444;
        }
        QPushButton:pressed {
            background-color: #555;
        }
    """,

    # Market Item Widget (wiersz z akcją)
    "market_item": """
        QFrame#ItemFrame {
            background-color: transparent;
            border: 1px solid #2b2b2b;
            border-radius: 6px;
            padding: 2px;
        }
        QFrame#ItemFrame:hover {
            background-color: #252525;
            border: 1px solid #3a3a3a;
        }
    """,

    # Symbol tickera
    "ticker_symbol": """
        font-weight: 600;
        font-size: 14px;
        color: white;
        border: none;
    """,

    # Cena
    "price_label": """
        font-size: 14px;
        color: white;
        border: none;
        font-weight: 500;
    """,

    # Przycisk usuwania
    "remove_button": """
        QPushButton {
            background-color: transparent;
            color: #EF4444;
            border: 1px solid #EF4444;
            border-radius: 12px;
            font-weight: bold;
            font-size: 16px;
            min-width: 25px;
            max-width: 25px;
            min-height: 25px;
            max-height: 25px;
            padding: 0px;
            margin: 0px;
        }
        QPushButton:hover {
            background-color: rgba(239, 68, 68, 0.15);
        }
    """,

    # Welcome Panel - przyciski akcji
    "action_button": """
        QPushButton {
            background-color: #444;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px;
            font-weight: 600;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #555;
        }
        QPushButton:pressed {
            background-color: #666;
        }
    """,

    # Statystyki rynkowe (małe widgety)
    "stats_widget": """
        QFrame#StatWidget {
            background-color: #2b2b2b;
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 8px;
        }
        QFrame#StatWidget:hover {
            background-color: #303030;
            border: 1px solid rgba(255, 255, 255, 0.12);
        }
    """,

    # Info widget (status systemu)
    "info_widget": """
        QFrame#InfoWidget {
            background-color: #2b2b2b;
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 6px;
        }
    """,

    # Etykiety wartości
    "value_label": """
        font-size: 16px;
        font-weight: 600;
        color: white;
        border: none;
    """,

    # Tytuły w stats widget
    "stats_title": """
        font-size: 11px;
        color: #999;
        border: none;
        font-weight: 500;
    """,

    # ScrollArea
    "scroll_area": """
        QScrollArea {
            background: transparent;
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
    """,

    # Kolory zmian
    "positive_color": GREEN_POSITIVE,
    "negative_color": RED_NEGATIVE,
}
