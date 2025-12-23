import os
import json
import yfinance as yf
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QInputDialog, QMessageBox, QScrollArea, QSizePolicy
)
from PySide6.QtCore import Qt, QThread, Signal, QUrl, QStandardPaths
from PySide6.QtGui import QDesktopServices, QIcon, QPixmap

from App.app_state import AppState
from App.translations import TRANSLATIONS
from App.Pages.PredictionThemes import LIGHT_THEME, DARK_THEME


# --- Helpery ---

def get_tr(key):
    lang = AppState.get_language()
    local_map = {
        "welcome_title": {"English": "Your AI trading companion", "Polski": "Twój asystent AI"},
        "open_repo": {"English": "Learn more", "Polski": "Dowiedz się więcej"},
        "favorites_title": {"English": "Favorites", "Polski": "Ulubione"},
        "top_picks_title": {"English": "Top Picks", "Polski": "Polecane"},
        "edit_favorites": {"English": "Edit", "Polski": "Edytuj"},
        "add_ticker_msg": {"English": "Enter ticker symbol (e.g. NVDA, BTC-USD):",
                           "Polski": "Podaj symbol (np. NVDA, BTC-USD):"},
        "add_ticker_title": {"English": "Add Favorite", "Polski": "Dodaj Ulubione"},
    }
    if key in local_map:
        return local_map[key].get(lang, local_map[key]["English"])
    return TRANSLATIONS.get(lang, {}).get(key, key)


def get_theme_cfg():
    return DARK_THEME if AppState.get_theme() == "dark" else LIGHT_THEME


def get_style(key):
    theme = get_theme_cfg()
    val = theme.get(key, "")
    return val.get("style", "") if isinstance(val, dict) else val


# --- Zarządzanie Configiem (Ulubione) ---

CONFIG_DIR = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
FAV_FILE = os.path.join(CONFIG_DIR, "favorites.json")


def load_favorites():
    if not os.path.exists(CONFIG_DIR): os.makedirs(CONFIG_DIR)
    if not os.path.exists(FAV_FILE): return ["BTC-USD", "NVDA", "SPY"]
    try:
        with open(FAV_FILE, 'r') as f:
            data = json.load(f)
            return data.get("tickers", [])
    except:
        return []


def save_favorites(tickers):
    if not os.path.exists(CONFIG_DIR): os.makedirs(CONFIG_DIR)
    try:
        with open(FAV_FILE, 'w') as f:
            json.dump({"tickers": tickers}, f)
    except Exception as e:
        print(f"Error saving favs: {e}")


# --- Worker ---

class MarketWorker(QThread):
    finished = Signal(dict)

    def __init__(self, tickers):
        super().__init__()
        self.tickers = tickers

    def run(self):
        if not self.tickers:
            self.finished.emit({})
            return
        try:
            tickers_str = " ".join(self.tickers)
            df = yf.download(tickers_str, period="2d", interval="1d", progress=False)
            data = {}
            if not df.empty:
                if "Close" in df:
                    closes = df["Close"]
                    for t in self.tickers:
                        try:
                            if len(self.tickers) > 1:
                                if t in closes.columns:
                                    current = closes[t].iloc[-1]
                                    prev = closes[t].iloc[-2]
                                else:
                                    continue
                            else:
                                current = closes.iloc[-1]
                                prev = closes.iloc[-2]

                            change_pct = ((current - prev) / prev) * 100
                            data[t] = {"price": current, "change": change_pct}
                        except:
                            data[t] = {"price": 0.0, "change": 0.0}
            self.finished.emit(data)
        except Exception as e:
            print(f"Market data error: {e}")
            self.finished.emit({})


# --- Widgety ---

class MarketItemWidget(QFrame):
    """
    Pojedynczy wiersz z akcją/walutą.
    Teraz dziedziczy po QFrame, aby mieć własne obramowanie.
    """

    def __init__(self, symbol):
        super().__init__()
        self.setObjectName("ItemFrame")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)

        self.lbl_symbol = QLabel(symbol)
        self.lbl_symbol.setStyleSheet("font-weight: bold; font-size: 14px; border: none;")

        self.lbl_price = QLabel("...")
        self.lbl_price.setAlignment(Qt.AlignRight)
        self.lbl_price.setStyleSheet("font-size: 14px; border: none;")

        self.lbl_change = QLabel("")
        self.lbl_change.setFixedWidth(70)
        self.lbl_change.setAlignment(Qt.AlignRight)
        self.lbl_change.setStyleSheet("font-size: 14px; border: none;")

        layout.addWidget(self.lbl_symbol)
        layout.addStretch()
        layout.addWidget(self.lbl_price)
        layout.addWidget(self.lbl_change)

        AppState.state_changed.connect(self.update_style)
        self.update_style()

    def update_data(self, price, change):
        self.lbl_price.setText(f"{price:.2f}")
        self.lbl_change.setText(f"{change:+.2f}%")
        col = "#00cc00" if change >= 0 else "#ff3333"
        self.lbl_change.setStyleSheet(f"color: {col}; font-weight: bold; font-size: 14px; border: none;")
        self.lbl_price.setStyleSheet(f"color: {col}; font-size: 14px; border: none;")

    def update_style(self):
        # Ustawiamy ramkę dla każdego rekordu
        is_dark = AppState.get_theme() == "dark"
        border_col = "rgba(255, 255, 255, 0.1)" if is_dark else "rgba(0, 0, 0, 0.1)"
        bg_col = "transparent"
        text_col = "#ffffff" if is_dark else "#000000"

        self.setStyleSheet(f"""
            QFrame#ItemFrame {{
                background-color: {bg_col};
                border: 1px solid {border_col};
                border-radius: 8px;
            }}
        """)
        self.lbl_symbol.setStyleSheet(f"font-weight: bold; font-size: 14px; color: {text_col}; border: none;")


class CardFrame(QFrame):
    """Ramka główna panelu (Karta)."""

    def __init__(self):
        super().__init__()
        self.setObjectName("Card")
        AppState.state_changed.connect(self.update_style)
        self.update_style()

    def update_style(self):
        is_dark = AppState.get_theme() == "dark"

        # Kolory tła i ramki (Wyraźna ramka 2px jak na schemacie)
        bg = "#1e1e1e" if is_dark else "#ffffff"
        border = "#555" if is_dark else "#000"

        self.setStyleSheet(f"""
            QFrame#Card {{
                background-color: {bg};
                border: 2px solid {border};
                border-radius: 15px;
            }}
        """)


class FavoritesPanel(CardFrame):
    def __init__(self):
        super().__init__()
        self.tickers = load_favorites()
        self.items = {}

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        # Nagłówek z przyciskiem edycji
        header_lay = QHBoxLayout()
        self.lbl_title = QLabel(get_tr("favorites_title").upper())
        self.lbl_title.setAlignment(Qt.AlignCenter)
        self.lbl_title.setStyleSheet("border: none;")

        self.btn_edit = QPushButton("+")
        self.btn_edit.setFixedSize(30, 30)
        self.btn_edit.setCursor(Qt.PointingHandCursor)
        self.btn_edit.clicked.connect(self.add_ticker)

        header_lay.addWidget(self.lbl_title)
        header_lay.addWidget(self.btn_edit)
        layout.addLayout(header_lay)

        layout.addSpacing(10)

        # Lista
        self.list_container = QWidget()
        self.list_layout = QVBoxLayout(self.list_container)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(8)  # Odstęp między rekordami

        scroll = QScrollArea()
        scroll.setWidget(self.list_container)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")
        layout.addWidget(scroll)

        self.rebuild_list()

        AppState.state_changed.connect(self.update_ui)
        self.update_ui()
        self.refresh_data()

    def rebuild_list(self):
        for i in reversed(range(self.list_layout.count())):
            self.list_layout.itemAt(i).widget().setParent(None)
        self.items = {}
        for t in self.tickers:
            item = MarketItemWidget(t)
            self.list_layout.addWidget(item)
            self.items[t] = item
        self.list_layout.addStretch()

    def refresh_data(self):
        self.worker = MarketWorker(self.tickers)
        self.worker.finished.connect(self.on_data_received)
        self.worker.start()

    def on_data_received(self, data):
        for t, values in data.items():
            if t in self.items:
                self.items[t].update_data(values["price"], values["change"])

    def add_ticker(self):
        text, ok = QInputDialog.getText(self, get_tr("add_ticker_title"), get_tr("add_ticker_msg"))
        if ok and text:
            symbol = text.upper().strip()
            if symbol not in self.tickers:
                self.tickers.append(symbol)
                save_favorites(self.tickers)
                self.rebuild_list()
                self.refresh_data()

    def update_ui(self):
        self.lbl_title.setText(get_tr("favorites_title").upper())
        # Używamy stylu nagłówka z themes
        header_style = get_style("home_header")
        if not header_style:  # Fallback
            header_style = f"font-size: 18px; font-weight: bold; color: {'#fff' if AppState.get_theme() == 'dark' else '#000'}; border: none;"
        else:
            header_style += " border: none;"  # Fix dla dziedziczenia

        self.lbl_title.setStyleSheet(header_style)

        # Styl małego przycisku
        self.btn_edit.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {'#fff' if AppState.get_theme() == 'dark' else '#000'};
                border: 1px solid {'#555' if AppState.get_theme() == 'dark' else '#ccc'};
                border-radius: 15px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: rgba(128,128,128,0.2); }}
        """)


class TopPicksPanel(CardFrame):
    def __init__(self):
        super().__init__()
        self.tickers = ["BTC-USD", "ETH-USD", "EURUSD=X", "TSLA", "AMD"]
        self.items = {}

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        self.lbl_title = QLabel(get_tr("top_picks_title").upper())
        self.lbl_title.setAlignment(Qt.AlignCenter)
        self.lbl_title.setStyleSheet("border: none;")
        layout.addWidget(self.lbl_title)

        layout.addSpacing(10)

        # Kontener na listę
        list_container = QWidget()
        list_layout = QVBoxLayout(list_container)
        list_layout.setContentsMargins(0, 0, 0, 0)
        list_layout.setSpacing(8)

        for t in self.tickers:
            item = MarketItemWidget(t)
            list_layout.addWidget(item)
            self.items[t] = item

        list_layout.addStretch()

        # Dodajemy do głównego layoutu
        layout.addWidget(list_container)

        AppState.state_changed.connect(self.update_ui)
        self.update_ui()
        self.refresh_data()

    def refresh_data(self):
        self.worker = MarketWorker(self.tickers)
        self.worker.finished.connect(self.on_data_received)
        self.worker.start()

    def on_data_received(self, data):
        for t, values in data.items():
            if t in self.items:
                self.items[t].update_data(values["price"], values["change"])

    def update_ui(self):
        self.lbl_title.setText(get_tr("top_picks_title").upper())
        header_style = get_style("home_header")
        if not header_style:
            header_style = f"font-size: 18px; font-weight: bold; color: {'#fff' if AppState.get_theme() == 'dark' else '#000'}; border: none;"
        else:
            header_style += " border: none;"
        self.lbl_title.setStyleSheet(header_style)


class WelcomePanel(CardFrame):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(20)
        layout.setContentsMargins(25, 30, 25, 30)

        self.logo = QLabel()
        pixmap = QPixmap(":/Launcher/Icons/Logo.png")
        if not pixmap.isNull():
            self.logo.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.logo.setText("LOGO")
        self.logo.setStyleSheet("border: none;")
        self.logo.setAlignment(Qt.AlignCenter)

        layout.addSpacing(20)
        layout.addWidget(self.logo)

        self.lbl_title = QLabel(get_tr("welcome_title"))
        self.lbl_title.setAlignment(Qt.AlignCenter)
        self.lbl_title.setStyleSheet("border: none;")
        layout.addWidget(self.lbl_title)

        layout.addStretch()

        self.btn_repo = QPushButton(get_tr("open_repo"))
        self.btn_repo.setCursor(Qt.PointingHandCursor)
        self.btn_repo.setMinimumHeight(45)
        self.btn_repo.clicked.connect(self.open_repo)

        layout.addWidget(self.btn_repo)

        AppState.state_changed.connect(self.update_ui)
        self.update_ui()

    def open_repo(self):
        QDesktopServices.openUrl(QUrl("https://github.com/vGiacomov/HOSSAnna---AI-tools-for-market-trend-analysis"))

    def update_ui(self):
        self.lbl_title.setText(get_tr("welcome_title"))
        text_col = "#fff" if AppState.get_theme() == 'dark' else "#000"
        self.lbl_title.setStyleSheet(
            f"font-size: 24px; font-weight: bold; font-style: italic; margin-top: 20px; color: {text_col}; border: none;")

        self.btn_repo.setText(get_tr("open_repo"))

        # Używamy stylu przycisku 'Oblicz' z Prediction (button_style)
        btn_style = get_style("button_style")
        if not btn_style:
            # Fallback jeśli nie znaleziono stylu
            btn_style = """
                QPushButton {
                    background-color: #d5d5a3; color: #000; border-radius: 5px; padding: 10px; font-weight: bold;
                }
            """
        self.btn_repo.setStyleSheet(btn_style)


# --- Główny Widget Home ---

class HomeWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setSpacing(25)
        layout.setContentsMargins(30, 30, 30, 30)

        # 1. Logo & Info (Lewo)
        self.welcome = WelcomePanel()

        # 2. Favorites (Środek)
        self.favorites = FavoritesPanel()

        # 3. Top Picks (Prawo)
        self.top_picks = TopPicksPanel()

        # Dodajemy do layoutu
        layout.addWidget(self.welcome, 2)
        layout.addWidget(self.favorites, 3)
        layout.addWidget(self.top_picks, 3)


def get_program_data():
    main_content = [
        {"type": "custom_widget", "widget_class": HomeWidget}
    ]

    return "Home", {
        "gui_type": "full_width",
        "icon_path": ":/App/Icons/home.png",
        "tab_type": "home",
        "title": "Home",
        "main_panel": main_content
    }
