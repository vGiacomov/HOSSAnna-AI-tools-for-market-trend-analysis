import os
from datetime import datetime
from pathlib import Path
import yfinance as yf
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QInputDialog, QScrollArea, QSizePolicy
)
from PySide6.QtCore import Qt, QThread, Signal, QUrl, QTimer
from PySide6.QtGui import QDesktopServices, QPixmap

from App.App_state import AppState
from App.translations import TRANSLATIONS
from App.Pages.HomeThemes import LIGHT_THEME, DARK_THEME
from Launcher.ConfigManager import ConfigManager


# --- Helpery ---

def get_tr(key):
    lang = AppState.get_language()
    local_map = {
        "welcome_title": {"English": "Your AI trading companion", "Polski": "Twój asystent AI"},
        "open_repo": {"English": "Learn more", "Polski": "Dowiedz się więcej"},
        "favorites_title": {"English": "Favorites", "Polski": "Ulubione"},
        "market_indices_title": {"English": "Market Indices", "Polski": "Indeksy giełdowe"},
        "add_ticker_msg": {"English": "Enter ticker symbol (e.g. NVDA, BTC-USD):",
                           "Polski": "Podaj symbol (np. NVDA, BTC-USD):"},
        "add_ticker_title": {"English": "Add Favorite", "Polski": "Dodaj Ulubione"},
        "quick_actions": {"English": "QUICK ACTIONS", "Polski": "SZYBKIE AKCJE"},
        "new_analysis": {"English": "New Analysis", "Polski": "Nowa analiza"},
        "market_scan": {"English": "Market Scanner", "Polski": "Skaner rynku"},
    }
    if key in local_map:
        return local_map[key].get(lang, local_map[key]["English"])
    return TRANSLATIONS.get(lang, {}).get(key, key)


def get_theme():
    return DARK_THEME if AppState.get_theme() == "dark" else LIGHT_THEME


# --- Rozszerzenie ConfigManager ---

class HomeConfigExtension:
    """Rozszerzenie ConfigManager o funkcje specyficzne dla Home"""

    @staticmethod
    def _get_favorites_path():
        """Zwraca ścieżkę do pliku z ulubionymi"""
        return ConfigManager.APP_FOLDER_PATH / "Configs" / "favorites.txt"

    @staticmethod
    def _get_recently_analyzed_path():
        """Zwraca ścieżkę do pliku z ostatnio analizowanymi"""
        return ConfigManager.APP_FOLDER_PATH / "Configs" / "recently_analyzed.txt"

    @staticmethod
    def load_favorites():
        """Wczytuje ulubione symbole z pliku txt"""
        favorites_path = HomeConfigExtension._get_favorites_path()

        if not favorites_path.exists():
            default_favs = ["BTC-USD", "NVDA", "SPY"]
            HomeConfigExtension.save_favorites(default_favs)
            return default_favs

        try:
            with open(favorites_path, 'r', encoding='utf-8') as f:
                tickers = [line.strip() for line in f if line.strip()]
                return tickers if tickers else ["BTC-USD", "NVDA", "SPY"]
        except Exception as e:
            print(f"[HomeConfig] Error loading favorites: {e}")
            return ["BTC-USD", "NVDA", "SPY"]

    @staticmethod
    def save_favorites(tickers):
        """Zapisuje ulubione symbole do pliku txt"""
        try:
            favorites_path = HomeConfigExtension._get_favorites_path()
            favorites_path.parent.mkdir(parents=True, exist_ok=True)

            with open(favorites_path, 'w', encoding='utf-8') as f:
                for ticker in tickers:
                    f.write(f"{ticker}\n")
            return True
        except Exception as e:
            print(f"[HomeConfig] Error saving favorites: {e}")
            return False

    @staticmethod
    def add_recently_analyzed(ticker):
        """Dodaje symbol do ostatnio analizowanych"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        recently_path = HomeConfigExtension._get_recently_analyzed_path()

        recent = []
        if recently_path.exists():
            try:
                with open(recently_path, 'r', encoding='utf-8') as f:
                    recent = [line.strip() for line in f if line.strip()]
            except:
                pass

        recent = [line for line in recent if not line.startswith(f"{ticker}|")]
        recent.insert(0, f"{ticker}|{timestamp}")
        recent = recent[:20]

        try:
            recently_path.parent.mkdir(parents=True, exist_ok=True)
            with open(recently_path, 'w', encoding='utf-8') as f:
                for line in recent:
                    f.write(f"{line}\n")
            return True
        except Exception as e:
            print(f"[HomeConfig] Error saving recently analyzed: {e}")
            return False


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
            data = {}
            for ticker in self.tickers:
                try:
                    stock = yf.Ticker(ticker)
                    info = stock.info
                    hist = stock.history(period="2d")

                    if not hist.empty and len(hist) >= 2:
                        current = hist['Close'].iloc[-1]
                        prev = hist['Close'].iloc[-2]
                        change_pct = ((current - prev) / prev) * 100
                        data[ticker] = {"price": float(current), "change": float(change_pct)}
                    elif not hist.empty:
                        current = hist['Close'].iloc[-1]
                        data[ticker] = {"price": float(current), "change": 0.0}
                    else:
                        data[ticker] = {"price": 0.0, "change": 0.0}
                except Exception as e:
                    print(f"Error fetching {ticker}: {e}")
                    data[ticker] = {"price": 0.0, "change": 0.0}

            self.finished.emit(data)
        except Exception as e:
            print(f"Market data error: {e}")
            self.finished.emit({})


# --- Widgety ---

class MarketItemWidget(QFrame):
    """Pojedynczy wiersz z akcją/walutą"""

    def __init__(self, symbol, display_name=None, removable=False, on_remove=None):
        super().__init__()
        self.setObjectName("ItemFrame")
        self.symbol = symbol
        self.display_name = display_name or symbol

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)

        self.lbl_symbol = QLabel(self.display_name)
        self.lbl_symbol.setMinimumWidth(100)

        self.lbl_price = QLabel("...")
        self.lbl_price.setAlignment(Qt.AlignRight)

        self.lbl_change = QLabel("")
        self.lbl_change.setFixedWidth(80)
        self.lbl_change.setAlignment(Qt.AlignRight)

        layout.addWidget(self.lbl_symbol)
        layout.addStretch()
        layout.addWidget(self.lbl_price)
        layout.addWidget(self.lbl_change)

        if removable and on_remove:
            self.btn_remove = QPushButton("🗑️")
            self.btn_remove.setFixedSize(32, 32)
            self.btn_remove.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            self.btn_remove.setCursor(Qt.PointingHandCursor)
            self.btn_remove.clicked.connect(lambda: on_remove(symbol))
            layout.addWidget(self.btn_remove)

        AppState.state_changed.connect(self.update_style)
        self.update_style()

    def update_data(self, price, change):
        theme = get_theme()

        if price >= 1000:
            price_str = f"${price:,.2f}" if "USD" in self.symbol else f"{price:,.2f}"
        else:
            price_str = f"${price:.2f}" if "USD" in self.symbol else f"{price:.2f}"

        self.lbl_price.setText(price_str)
        self.lbl_change.setText(f"{change:+.2f}%")

        # Kolory
        color = theme["positive_color"] if change >= 0 else theme["negative_color"]
        self.lbl_change.setStyleSheet(f"color: {color}; font-weight: 600; font-size: 14px; border: none;")

        price_style = theme["price_label"]
        self.lbl_price.setStyleSheet(price_style)

    def update_style(self):
        theme = get_theme()
        self.setStyleSheet(theme["market_item"])
        self.lbl_symbol.setStyleSheet(theme["ticker_symbol"])
        self.lbl_price.setStyleSheet(theme["price_label"])

        if hasattr(self, 'btn_remove'):
            self.btn_remove.setStyleSheet(theme["remove_button"])


class CardFrame(QFrame):
    """Ramka główna panelu (Karta)"""

    def __init__(self):
        super().__init__()
        self.setObjectName("Card")
        AppState.state_changed.connect(self.update_style)
        self.update_style()

    def update_style(self):
        theme = get_theme()
        self.setStyleSheet(theme["card"])


class FavoritesPanel(CardFrame):
    """Panel z ulubionymi"""

    def __init__(self):
        super().__init__()
        self.tickers = HomeConfigExtension.load_favorites()
        self.items = {}

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(5, 5, 5, 5)

        # Nagłówek
        header_lay = QHBoxLayout()
        self.lbl_title = QLabel(get_tr("favorites_title").upper())
        self.lbl_title.setAlignment(Qt.AlignLeft)

        self.btn_add = QPushButton("+")
        self.btn_add.setFixedSize(30, 30)
        self.btn_add.setCursor(Qt.PointingHandCursor)
        self.btn_add.clicked.connect(self.add_ticker)

        header_lay.addWidget(self.lbl_title)
        header_lay.addStretch()
        header_lay.addWidget(self.btn_add)
        layout.addLayout(header_lay)

        # Lista
        self.list_container = QWidget()
        self.list_layout = QVBoxLayout(self.list_container)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(8)

        scroll = QScrollArea()
        scroll.setWidget(self.list_container)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)

        self.rebuild_list()

        AppState.state_changed.connect(self.update_ui)
        self.update_ui()
        self.refresh_data()

    def rebuild_list(self):
        for i in reversed(range(self.list_layout.count())):
            widget = self.list_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        self.items = {}
        for t in self.tickers:
            item = MarketItemWidget(t, removable=True, on_remove=self.remove_ticker)
            self.list_layout.addWidget(item)
            self.items[t] = item
        self.list_layout.addStretch()

    def refresh_data(self):
        if self.tickers:
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
            if symbol and symbol not in self.tickers:
                self.tickers.append(symbol)
                HomeConfigExtension.save_favorites(self.tickers)
                self.rebuild_list()
                self.refresh_data()

    def remove_ticker(self, symbol):
        if symbol in self.tickers:
            self.tickers.remove(symbol)
            HomeConfigExtension.save_favorites(self.tickers)
            self.rebuild_list()

    def update_ui(self):
        theme = get_theme()
        self.lbl_title.setText(get_tr("favorites_title").upper())
        self.lbl_title.setStyleSheet(theme["section_header"])
        self.btn_add.setStyleSheet(theme["add_button"])

        # Scroll area
        scroll = self.findChild(QScrollArea)
        if scroll:
            scroll.setStyleSheet(theme["scroll_area"])


class MarketIndicesPanel(CardFrame):
    """Panel z indeksami giełdowymi"""

    def __init__(self):
        super().__init__()

        self.tickers = [
            ("^GSPC", "S&P 500"),
            ("^DJI", "Dow Jones"),
            ("^IXIC", "NASDAQ"),
            ("^FTSE", "FTSE 100"),
            ("^GDAXI", "DAX"),
            ("^FCHI", "CAC 40"),
            ("^N225", "Nikkei 225"),
            ("000001.SS", "Shanghai"),
        ]

        self.items = {}

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(5, 5, 5, 5)

        self.lbl_title = QLabel(get_tr("market_indices_title").upper())
        self.lbl_title.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.lbl_title)

        list_container = QWidget()
        list_layout = QVBoxLayout(list_container)
        list_layout.setContentsMargins(0, 0, 0, 0)
        list_layout.setSpacing(8)

        for ticker, name in self.tickers:
            item = MarketItemWidget(ticker, display_name=name, removable=False)
            list_layout.addWidget(item)
            self.items[ticker] = item

        list_layout.addStretch()

        scroll = QScrollArea()
        scroll.setWidget(list_container)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)

        AppState.state_changed.connect(self.update_ui)
        self.update_ui()
        self.refresh_data()

        # Auto-refresh co 2 minuty
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_data)
        self.timer.start(120000)

    def refresh_data(self):
        ticker_symbols = [t[0] for t in self.tickers]
        self.worker = MarketWorker(ticker_symbols)
        self.worker.finished.connect(self.on_data_received)
        self.worker.start()

    def on_data_received(self, data):
        for ticker, values in data.items():
            if ticker in self.items:
                self.items[ticker].update_data(values["price"], values["change"])

    def update_ui(self):
        theme = get_theme()
        self.lbl_title.setText(get_tr("market_indices_title").upper())
        self.lbl_title.setStyleSheet(theme["section_header"])

        scroll = self.findChild(QScrollArea)
        if scroll:
            scroll.setStyleSheet(theme["scroll_area"])


class WelcomePanel(CardFrame):
    """Panel powitalny z quick actions"""

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(20)
        layout.setContentsMargins(5, 5, 5, 5)

        # Logo i tytuł
        header = QHBoxLayout()
        self.logo = QLabel()
        pixmap = QPixmap(":/Launcher/Icons/Logo.png")
        if not pixmap.isNull():
            self.logo.setPixmap(pixmap.scaled(70, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.logo.setText("📈")
            self.logo.setStyleSheet("font-size: 50px; border: none;")
        self.logo.setStyleSheet("border: none;")

        title_layout = QVBoxLayout()
        title_layout.setSpacing(5)

        self.lbl_title = QLabel("HOSSAnna")

        self.lbl_subtitle = QLabel(get_tr("welcome_title"))

        title_layout.addWidget(self.lbl_title)
        title_layout.addWidget(self.lbl_subtitle)

        header.addWidget(self.logo)
        header.addLayout(title_layout)
        header.addStretch()

        layout.addLayout(header)
        layout.addSpacing(30)

        # Quick Actions
        self.actions_label = QLabel(get_tr("quick_actions"))
        layout.addWidget(self.actions_label)

        actions_layout = QVBoxLayout()
        actions_layout.setSpacing(12)

        self.btn_analysis = QPushButton(f"🔍  {get_tr('new_analysis')}")
        self.btn_analysis.setCursor(Qt.PointingHandCursor)
        self.btn_analysis.setMinimumHeight(50)

        self.btn_scanner = QPushButton(f"📊  {get_tr('market_scan')}")
        self.btn_scanner.setCursor(Qt.PointingHandCursor)
        self.btn_scanner.setMinimumHeight(50)

        self.btn_repo = QPushButton(f"🌐  {get_tr('open_repo')}")
        self.btn_repo.setCursor(Qt.PointingHandCursor)
        self.btn_repo.setMinimumHeight(50)
        self.btn_repo.clicked.connect(self.open_repo)

        actions_layout.addWidget(self.btn_analysis)
        actions_layout.addWidget(self.btn_scanner)
        actions_layout.addWidget(self.btn_repo)

        layout.addLayout(actions_layout)
        layout.addStretch()

        AppState.state_changed.connect(self.update_ui)
        self.update_ui()

    def open_repo(self):
        QDesktopServices.openUrl(QUrl("https://github.com/vGiacomov/HOSSAnna---AI-tools-for-market-trend-analysis"))

    def update_ui(self):
        theme = get_theme()
        is_dark = AppState.get_theme() == "dark"

        self.lbl_subtitle.setText(get_tr("welcome_title"))
        self.actions_label.setText(get_tr("quick_actions"))

        # Tytuł
        title_color = "#FFFFFF" if is_dark else "#1A1A1A"
        self.lbl_title.setStyleSheet(f"font-size: 28px; font-weight: 700; color: {title_color}; border: none;")

        # Subtitle
        subtitle_color = "#9B9B9B" if is_dark else "#6B6B6B"
        self.lbl_subtitle.setStyleSheet(f"font-size: 14px; color: {subtitle_color}; border: none;")

        # Actions label
        self.actions_label.setStyleSheet(theme["section_header"])

        # Przyciski
        self.btn_analysis.setText(f"🔍  {get_tr('new_analysis')}")
        self.btn_scanner.setText(f"📊  {get_tr('market_scan')}")
        self.btn_repo.setText(f"🌐  {get_tr('open_repo')}")

        btn_style = theme["action_button"]
        self.btn_analysis.setStyleSheet(btn_style)
        self.btn_scanner.setStyleSheet(btn_style)
        self.btn_repo.setStyleSheet(btn_style)


# --- Główny Widget Home ---

class HomeWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(5, 5, 5, 5)

        # Welcome Panel (Lewo) - 30%
        self.welcome = WelcomePanel()

        # Favorites Panel (Środek) - 35%
        self.favorites = FavoritesPanel()

        # Market Indices (Prawo) - 35%
        self.market_indices = MarketIndicesPanel()

        layout.addWidget(self.welcome, 3)
        layout.addWidget(self.favorites, 4)
        layout.addWidget(self.market_indices, 4)


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
