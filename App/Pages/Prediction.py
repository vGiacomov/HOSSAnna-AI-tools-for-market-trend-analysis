import yfinance as yf
import pandas as pd
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import mplfinance as mpf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox,
    QLabel, QSizePolicy, QFrame, QLineEdit, QComboBox, QPushButton
)
from PySide6.QtCore import QThread, Signal, Qt

from App.app_state import AppState
from App.translations import TRANSLATIONS
from App.Pages.PredictionThemes import LIGHT_THEME, DARK_THEME


# --- Helpery ---

def get_tr(key):
    lang = AppState.get_language()
    return TRANSLATIONS.get(lang, {}).get(key, key)


def get_theme_cfg():
    return DARK_THEME if AppState.get_theme() == "dark" else LIGHT_THEME


def get_style_str(theme, key):
    # Prosta funkcja wyciągająca styl ze słownika motywu
    val = theme.get(key, "")
    if isinstance(val, dict):
        return val.get("style", "")
    return val


# --- Background Worker ---

class PredictionWorker(QThread):
    finished = Signal(dict)
    error = Signal(str)
    progress = Signal(str)

    def __init__(self, symbol, period, interval):
        super().__init__()
        self.symbol = symbol
        self.period = period
        self.interval = interval

    def run(self):
        try:
            self.progress.emit("loading")
            df = yf.download(self.symbol, period=self.period, interval=self.interval)
            if df.empty: raise ValueError(f"No data for {self.symbol}")

            if isinstance(df.columns, pd.MultiIndex):
                df.columns = [c[0] for c in df.columns]

            for col in ["Open", "High", "Low", "Close", "Volume"]:
                if col in df.columns: df[col] = pd.to_numeric(df[col], errors="coerce")

            df = df.dropna()
            if len(df) < 50: raise ValueError("Insufficient data")

            self.progress.emit("calculating")
            scaler = MinMaxScaler()
            scaled = scaler.fit_transform(df[["Close"]])
            seq_len = min(30, len(scaled) // 3)

            X, y = [], []
            for i in range(len(scaled) - seq_len):
                X.append(scaled[i:i + seq_len])
                y.append(scaled[i + seq_len])

            X, y = np.array(X), np.array(y)
            train_size = int(len(X) * 0.8)

            model = Sequential([
                LSTM(64, return_sequences=False, input_shape=(seq_len, 1)),
                Dense(1)
            ])
            model.compile(optimizer="adam", loss="mse")
            model.fit(X[:train_size], y[:train_size], epochs=20, batch_size=32, verbose=0)

            last_seq = scaled[-seq_len:].reshape(1, seq_len, 1)
            pred_scaled = model.predict(last_seq, verbose=0)
            next_price = scaler.inverse_transform(pred_scaled)[0][0]
            current_price = df["Close"].iloc[-1]

            self.finished.emit({
                "df": df,
                "next_price": next_price,
                "current_price": current_price,
                "symbol": self.symbol
            })
        except Exception as e:
            self.error.emit(str(e))


# --- Custom Widgety ---

class PlaceholderWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        AppState.state_changed.connect(self.refresh_ui)
        self.refresh_ui()

    def refresh_ui(self):
        self.label.setText(get_tr("placeholder_message"))
        theme = get_theme_cfg()
        style = theme.get("placeholder", {}).get("text_style", "")
        self.label.setStyleSheet(style)


class ChartWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.chart_cfg = get_theme_cfg().get("chart", {})
        self.figure = Figure(facecolor=self.chart_cfg.get("bg_color", "white"))
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.canvas)
        self.hide()
        AppState.state_changed.connect(self.refresh_ui)

    def refresh_ui(self):
        theme = get_theme_cfg()
        self.chart_cfg = theme.get("chart", {})
        self.figure.patch.set_facecolor(self.chart_cfg.get("bg_color", "white"))
        if self.isVisible(): self.canvas.draw()

    def update_chart(self, df, next_price, selected_range="15m"):
        self.figure.clear()
        df_plot = df.tail(80).copy()
        df_plot["Prediction"] = np.nan
        df_plot.iloc[-1, df_plot.columns.get_loc("Prediction")] = next_price
        theme_cfg = get_theme_cfg()
        cfg = self.chart_cfg
        style_config = cfg.get("mpf_style_config", {})
        dt_format = '%H:%M' if selected_range in ["5m", "15m", "1h"] else '%Y-%m-%d'

        try:
            ax = self.figure.add_axes([0.05, 0.05, 0.97, 0.99])
            mc = mpf.make_marketcolors(
                up=cfg.get("mpf_colors", {}).get("up", "#00aa00"),
                down=cfg.get("mpf_colors", {}).get("down", "#cc0000"),
                wick=cfg.get("mpf_colors", {}).get("wick", "#333"),
                edge=cfg.get("mpf_colors", {}).get("edge", "#333"),
                volume=cfg.get("mpf_colors", {}).get("volume", "in"),
            )
            style = mpf.make_mpf_style(
                base_mpf_style=cfg.get("mpf_style_base", "yahoo"),
                marketcolors=mc,
                gridcolor=style_config.get("gridcolor", "#ddd"),
                gridstyle=style_config.get("gridstyle", "-"),
                facecolor=style_config.get("facecolor", "white"),
                edgecolor=style_config.get("edgecolor", "black"),
                figcolor=style_config.get("figcolor", "white"),
                y_on_right=False
            )
            add_plot = mpf.make_addplot(
                df_plot["Prediction"], scatter=True,
                markersize=cfg.get("prediction_marker", {}).get("size", 200),
                marker=cfg.get("prediction_marker", {}).get("marker", "*"),
                color=cfg.get("prediction_color", "gold"), ax=ax,
            )
            mpf.plot(
                df_plot, type="candle", style=style, ylabel="", xrotation=0,
                datetime_format=dt_format, addplot=add_plot, volume=False, ax=ax, tight_layout=False
            )
            axis_color = style_config.get("edgecolor", "black")
            ax.tick_params(axis='x', colors=axis_color)
            ax.tick_params(axis='y', colors=axis_color)
            for spine in ax.spines.values(): spine.set_edgecolor(axis_color)
            self.figure.subplots_adjust(0, 0, 1, 1)
            self.figure.patch.set_facecolor(cfg.get("bg_color", "white"))
            self.canvas.draw()
            self.show()
        except Exception as e:
            print(f"Chart error: {e}")


class ControlPanelWidget(QWidget):
    """
    Widget panelu sterowania: Siatka inputów + przycisk na dole.
    """

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(5, 5, 5, 5)

        # Grid: Etykieta | Input
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.setColumnStretch(1, 1)  # Inputy szerokie

        # Rząd 1: Symbol
        self.lbl_symbol = QLabel()
        self.inp_symbol = QLineEdit("NVDA")
        CONTROLLER.set_symbol_input(self.inp_symbol)

        grid.addWidget(self.lbl_symbol, 0, 0)
        grid.addWidget(self.inp_symbol, 0, 1)

        # Rząd 2: Zakres
        self.lbl_range = QLabel()
        self.cmb_range = QComboBox()
        self.cmb_range.addItems(["5m", "15m", "1h", "1d", "7d", "14d", "30d"])
        CONTROLLER.set_range_combo(self.cmb_range)

        grid.addWidget(self.lbl_range, 1, 0)
        grid.addWidget(self.cmb_range, 1, 1)

        layout.addLayout(grid)

        # Przycisk na dole
        self.btn_calc = QPushButton()
        CONTROLLER.set_calc_button(self.btn_calc)
        layout.addWidget(self.btn_calc)

        layout.addStretch(1)

        AppState.state_changed.connect(self.refresh_ui)
        self.refresh_ui()

    def refresh_ui(self):
        theme = get_theme_cfg()

        # Tłumaczenia
        self.lbl_symbol.setText(get_tr("symbol_label"))
        self.lbl_range.setText(get_tr("prediction_range"))
        self.btn_calc.setText(get_tr("calculate_button"))

        # Style - używamy helpera get_style_str
        lbl_style = get_style_str(theme, "label")
        self.lbl_symbol.setStyleSheet(lbl_style)
        self.lbl_range.setStyleSheet(lbl_style)

        self.inp_symbol.setStyleSheet(get_style_str(theme, "lineedit_style"))
        self.cmb_range.setStyleSheet(get_style_str(theme, "combobox_style"))
        self.btn_calc.setStyleSheet(get_style_str(theme, "button_style"))


class PriceSummaryWidget(QWidget):
    """
    Widget wyników: Symbol na górze, ceny obok siebie pod spodem.
    """

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        # 1. Symbol
        self.symbol_label = QLabel("")
        self.symbol_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.symbol_label)

        # 2. Ceny (HBox)
        prices_layout = QHBoxLayout()
        prices_layout.setSpacing(20)

        # Lewa: Obecna
        self.current_label = QLabel()
        self.current_label.setAlignment(Qt.AlignCenter)
        self.current_value = QLabel("--")
        self.current_value.setAlignment(Qt.AlignCenter)

        curr_box = QVBoxLayout()
        curr_box.addWidget(self.current_label)
        curr_box.addWidget(self.current_value)
        prices_layout.addLayout(curr_box)

        # Prawa: Przewidywana
        self.predicted_label = QLabel()
        self.predicted_label.setAlignment(Qt.AlignCenter)
        self.predicted_value = QLabel("--")
        self.predicted_value.setAlignment(Qt.AlignCenter)

        pred_box = QVBoxLayout()
        pred_box.addWidget(self.predicted_label)
        pred_box.addWidget(self.predicted_value)
        prices_layout.addLayout(pred_box)

        layout.addLayout(prices_layout)
        layout.addStretch(1)

        self.hide()
        AppState.state_changed.connect(self.refresh_ui)
        self.refresh_ui()

    def refresh_ui(self):
        theme = get_theme_cfg()
        cfg = theme.get("price_summary", {})

        self.setStyleSheet(cfg.get("container_style", ""))
        self.symbol_label.setStyleSheet(cfg.get("symbol_style", ""))

        self.current_label.setText(get_tr("current_price").upper())
        self.current_label.setStyleSheet(cfg.get("label_style", ""))
        self.current_value.setStyleSheet(cfg.get("value_style", ""))

        self.predicted_label.setText(get_tr("predicted_price").upper())
        self.predicted_label.setStyleSheet(cfg.get("label_style", ""))
        self.predicted_value.setStyleSheet(cfg.get("value_style", ""))

    def update_prices(self, current, predicted, symbol):
        self.symbol_label.setText(symbol.upper())
        self.current_value.setText(f"{current:.2f}$")
        self.predicted_value.setText(f"{predicted:.2f}$")
        theme = get_theme_cfg()
        cfg = theme.get("price_summary", {})
        diff = predicted - current
        style = cfg.get("positive_style", "") if diff > 0 else (
            cfg.get("negative_style", "") if diff < 0 else cfg.get("value_style", ""))
        self.predicted_value.setStyleSheet(style)
        self.show()


# --- Controller ---

class PredictionController:
    def __init__(self):
        self.symbol_input = None;
        self.calc_btn = None;
        self.selected_range = "15m"
        self.placeholder = None;
        self.chart = None;
        self.price_summary = None

    def set_symbol_input(self, w):
        self.symbol_input = w
        w.textChanged.connect(lambda t: self.calc_btn.setEnabled(bool(t.strip())) if self.calc_btn else None)

    def set_calc_button(self, w):
        self.calc_btn = w
        w.clicked.connect(self.on_calculate)

    def set_range_combo(self, w):
        w.setCurrentText("15m")
        w.currentTextChanged.connect(lambda t: setattr(self, 'selected_range', t))

    def set_placeholder(self, w):
        self.placeholder = w

    def set_chart(self, w):
        self.chart = w

    def set_price_summary(self, w):
        self.price_summary = w

    def on_calculate(self):
        if not self.symbol_input: return
        symbol = self.symbol_input.text().strip().upper()
        if not symbol: QMessageBox.warning(None, "Error", get_tr("error_no_symbol")); return

        prediction_ranges = {
            "5m": {"period": "2d", "interval": "5m"}, "15m": {"period": "3d", "interval": "15m"},
            "1h": {"period": "3d", "interval": "60m"}, "1d": {"period": "30d", "interval": "1d"},
            "7d": {"period": "180d", "interval": "1wk"}, "30d": {"period": "5y", "interval": "1mo"},
        }
        cfg = prediction_ranges.get(self.selected_range, prediction_ranges["15m"])
        if self.calc_btn: self.calc_btn.setEnabled(False)
        self.worker = PredictionWorker(symbol, cfg["period"], cfg["interval"])
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_finished(self, res):
        if self.calc_btn: self.calc_btn.setEnabled(True)
        if self.placeholder: self.placeholder.hide()
        if self.chart: self.chart.update_chart(res["df"], res["next_price"], self.selected_range)
        if self.price_summary: self.price_summary.update_prices(res["current_price"], res["next_price"], res["symbol"])

    def on_error(self, err):
        if self.calc_btn: self.calc_btn.setEnabled(True)
        QMessageBox.critical(None, "Error", f"{get_tr('error_prediction')}: {err}")


CONTROLLER = PredictionController()


def get_program_data():
    # --- PANEL GÓRNY (WYKRES) ---
    top_panel = [
        {"type": "custom_widget", "widget_class": PlaceholderWidget, "on_create": CONTROLLER.set_placeholder},
        {"type": "custom_widget", "widget_class": ChartWidget, "on_create": CONTROLLER.set_chart},
    ]

    # --- PANEL DOLNY LEWY (INPUTY - Custom Widget) ---
    bottom_left_panel = [
        {"type": "custom_widget", "widget_class": ControlPanelWidget},
    ]

    # --- PANEL DOLNY PRAWY (WYNIKI - Custom Widget) ---
    bottom_right_panel = [
        {"type": "custom_widget", "widget_class": PriceSummaryWidget, "on_create": CONTROLLER.set_price_summary},
    ]

    return "Stock Price Prediction", {
        "gui_type": "top_bottom_split",
        "icon_path": ":/App/Icons/prediction.png",
        "tab_type": "prediction",
        "title": get_tr("prediction_title"),
        "top_panel": top_panel,
        "bottom_left_panel": bottom_left_panel,
        "bottom_right_panel": bottom_right_panel,
    }