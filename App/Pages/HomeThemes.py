"""
Motywy dla strony głównej HOSSAnna
Inspirowane Yahoo Finance - profesjonalny wygląd finansowy
"""

# Kolory Yahoo Finance
YAHOO_PURPLE = "#7000E3"  # Główny fiolet Yahoo
YAHOO_BLUE = "#0078FF"    # Niebieski akcent
GREEN_POSITIVE = "#16C784"  # Zielony dla dodatnich zmian
RED_NEGATIVE = "#EA3943"    # Czerwony dla ujemnych zmian

LIGHT_THEME = {
    # Główna karta (Card)
    "card": """
        QFrame#Card {
            background-color: #FFFFFF;
            border: 1px solid #E5E5E5;
            border-radius: 12px;
        }
    """,

    # Nagłówki sekcji
    "section_header": """
        font-size: 18px;
        font-weight: 600;
        color: #1A1A1A;
        border: none;
        padding: 5px 0px;
    """,

    # Przyciski akcji (dodawanie)
    "add_button": """
        QPushButton {
            background-color: transparent;
            color: #7000E3;
            border: 1.5px solid #7000E3;
            border-radius: 15px;
            font-weight: bold;
            font-size: 18px;
        }
        QPushButton:hover {
            background-color: rgba(112, 0, 227, 0.1);
        }
    """,

    # Market Item Widget (wiersz z akcją)
    "market_item": """
        QFrame#ItemFrame {
            background-color: transparent;
            border: 1px solid #F0F0F0;
            border-radius: 6px;
            padding: 2px;
        }
        QFrame#ItemFrame:hover {
            background-color: #F9F9F9;
            border: 1px solid #E0E0E0;
        }
    """,

    # Symbol tickera
    "ticker_symbol": """
        font-weight: 600;
        font-size: 14px;
        color: #1A1A1A;
        border: none;
    """,

    # Cena
    "price_label": """
        font-size: 14px;
        color: #1A1A1A;
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
        }
        QPushButton:hover {
            background-color: rgba(234, 57, 67, 0.1);
        }
    """,

    # Welcome Panel - przyciski akcji
    "action_button": """
        QPushButton {
            background-color: #7000E3;
            color: #FFFFFF;
            border: none;
            border-radius: 8px;
            padding: 12px;
            font-weight: 600;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #5C00BA;
        }
    """,

    # Statystyki rynkowe (małe widgety)
    "stats_widget": """
        QFrame#StatWidget {
            background-color: #F9F9F9;
            border: 1px solid #E5E5E5;
            border-radius: 8px;
        }
        QFrame#StatWidget:hover {
            background-color: #F5F5F5;
            border: 1px solid #D0D0D0;
        }
    """,

    # Info widget (status systemu)
    "info_widget": """
        QFrame#InfoWidget {
            background-color: #F9F9F9;
            border: 1px solid #E5E5E5;
            border-radius: 6px;
        }
    """,

    # Etykiety wartości
    "value_label": """
        font-size: 16px;
        font-weight: 600;
        color: #1A1A1A;
        border: none;
    """,

    # Tytuły w stats widget
    "stats_title": """
        font-size: 11px;
        color: #6B6B6B;
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
            border: none;
            background: #F5F5F5;
            width: 8px;
            border-radius: 4px;
        }
        QScrollBar::handle:vertical {
            background: #CCCCCC;
            border-radius: 4px;
            min-height: 20px;
        }
        QScrollBar::handle:vertical:hover {
            background: #AAAAAA;
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
            background-color: #1E1E1E;
            border: 1px solid #3A3A3A;
            border-radius: 12px;
        }
    """,

    # Nagłówki sekcji
    "section_header": """
        font-size: 18px;
        font-weight: 600;
        color: #FFFFFF;
        border: none;
        padding: 5px 0px;
    """,

    # Przyciski akcji (dodawanie)
    "add_button": """
        QPushButton {
            background-color: transparent;
            color: #9F7AEA;
            border: 1.5px solid #9F7AEA;
            border-radius: 15px;
            font-weight: bold;
            font-size: 18px;
        }
        QPushButton:hover {
            background-color: rgba(159, 122, 234, 0.15);
        }
    """,

    # Market Item Widget (wiersz z akcją)
    "market_item": """
        QFrame#ItemFrame {
            background-color: transparent;
            border: 1px solid #2A2A2A;
            border-radius: 6px;
            padding: 2px;
        }
        QFrame#ItemFrame:hover {
            background-color: #252525;
            border: 1px solid #3A3A3A;
        }
    """,

    # Symbol tickera
    "ticker_symbol": """
        font-weight: 600;
        font-size: 14px;
        color: #FFFFFF;
        border: none;
    """,

    # Cena
    "price_label": """
        font-size: 14px;
        color: #E0E0E0;
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
        }
        QPushButton:hover {
            background-color: rgba(234, 57, 67, 0.15);
        }
    """,

    # Welcome Panel - przyciski akcji
    "action_button": """
        QPushButton {
            background-color: #7000E3;
            color: #FFFFFF;
            border: none;
            border-radius: 8px;
            padding: 12px;
            font-weight: 600;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #8A2BE2;
        }
    """,

    # Statystyki rynkowe (małe widgety)
    "stats_widget": """
        QFrame#StatWidget {
            background-color: #2A2A2A;
            border: 1px solid #3A3A3A;
            border-radius: 8px;
        }
        QFrame#StatWidget:hover {
            background-color: #303030;
            border: 1px solid #4A4A4A;
        }
    """,

    # Info widget (status systemu)
    "info_widget": """
        QFrame#InfoWidget {
            background-color: #2A2A2A;
            border: 1px solid #3A3A3A;
            border-radius: 6px;
        }
    """,

    # Etykiety wartości
    "value_label": """
        font-size: 16px;
        font-weight: 600;
        color: #FFFFFF;
        border: none;
    """,

    # Tytuły w stats widget
    "stats_title": """
        font-size: 11px;
        color: #9B9B9B;
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
            border: none;
            background: #2A2A2A;
            width: 8px;
            border-radius: 4px;
        }
        QScrollBar::handle:vertical {
            background: #4A4A4A;
            border-radius: 4px;
            min-height: 20px;
        }
        QScrollBar::handle:vertical:hover {
            background: #5A5A5A;
        }
    """,

    # Kolory zmian
    "positive_color": GREEN_POSITIVE,
    "negative_color": RED_NEGATIVE,
}
