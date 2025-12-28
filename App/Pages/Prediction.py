import yfinance as yf
import pandas as pd
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import mplfinance as mpf
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox, QSizePolicy
)
from PySide6.QtCore import QThread, Signal, Qt

from App.theme_system import ( ThemeManager, AutoRefreshWidget, SmartLabel,
                               SmartButton, SmartLineEdit, SmartComboBox, LayoutHelper)



PREDICTION_RANGES = {
    "5m": {"period": "2d", "interval": "5m", "dt_format": "%H:%M", "tail": 80},
    "15m": {"period": "3d", "interval": "15m", "dt_format": "%H:%M", "tail": 80},
    "1h": {"period": "2wk", "interval": "60m", "dt_format": "%H:%M", "tail": 80},
    "1d": {"period": "3mo", "interval": "1d", "dt_format": "%Y-%m-%d", "tail": 80},
    "7d": {"period": "1y", "interval": "1wk", "dt_format": "%Y-%m-%d", "tail": 80},
    "30d": {"period": "5y", "interval": "1mo", "dt_format": "%Y-%m-%d", "tail": 80},
}


class StockPricePredictor:

    def __init__(self, config=None):
        self.config = {
        "units": 64,
        "epochs": 20,
        "batch_size": 32,
        "train_split": 0.8,
        "min_seq_len": 30,
        }


        self.scaler = MinMaxScaler()
        self.model = None
        self.accuracy_metrics = {}

    def prepare_data(self, df):
        scaled = self.scaler.fit_transform(df[["Close"]])
        seq_len = min(self.config["min_seq_len"], len(scaled) // 3)

        X, y = [], []
        for i in range(len(scaled) - seq_len):
            X.append(scaled[i:i + seq_len])
            y.append(scaled[i + seq_len])

        X, y = np.array(X), np.array(y)
        train_size = int(len(X) * self.config["train_split"])

        return X[:train_size], y[:train_size], X[train_size:], y[train_size:], seq_len, scaled

    def build_model(self, seq_len):
        self.model = Sequential([
            LSTM(self.config["units"], return_sequences=False, input_shape=(seq_len, 1)),
            Dense(1)
        ])
        self.model.compile(optimizer="adam", loss="mse")

    def train(self, X_train, y_train):
        self.model.fit(
            X_train, y_train,
            epochs=self.config["epochs"],
            batch_size=self.config["batch_size"],
            verbose=0
        )

    def calculate_accuracy(self, X_test, y_test):
        if len(X_test) == 0:
            return {"accuracy": 0.0, "rmse": 0.0, "mape": 0.0}

        predictions = self.model.predict(X_test, verbose=0)

        y_test_actual = self.scaler.inverse_transform(y_test)
        predictions_actual = self.scaler.inverse_transform(predictions)


        rmse = np.sqrt(mean_squared_error(y_test_actual, predictions_actual))
        mape = mean_absolute_percentage_error(y_test_actual, predictions_actual) * 100

        accuracy = max(0, 100 - mape)

        self.accuracy_metrics = {
            "accuracy": accuracy,
            "rmse": rmse,
            "mape": mape
        }

        return self.accuracy_metrics

    def predict_next(self, scaled_data, seq_len):
        last_seq = scaled_data[-seq_len:].reshape(1, seq_len, 1)
        pred_scaled = self.model.predict(last_seq, verbose=0)
        return self.scaler.inverse_transform(pred_scaled)[0][0]



class PredictionWorker(QThread):
    finished = Signal(dict)
    error = Signal(str)
    progress = Signal(str)

    REQUIRED_COLUMNS = ["Open", "High", "Low", "Close", "Volume"]
    MIN_DATA_POINTS = 30

    def __init__(self, symbol, period, interval):
        super().__init__()
        self.symbol = symbol
        self.period = period
        self.interval = interval
        self.predictor = StockPricePredictor()

    def fetch_and_validate(self):
        df = yf.download(self.symbol, period=self.period, interval=self.interval)

        if df.empty:
            raise ValueError(f"No data for {self.symbol}")

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [c[0] for c in df.columns]

        for col in self.REQUIRED_COLUMNS:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.dropna()

        if len(df) < self.MIN_DATA_POINTS:
            raise ValueError(f"Insufficient data (need at least {self.MIN_DATA_POINTS} points)")

        return df

    def get_company_name(self):
        try:
            ticker = yf.Ticker(self.symbol)
            info = ticker.info
            return info.get('longName', info.get('shortName', self.symbol.upper()))
        except:
            return self.symbol.upper()

    def run(self):
        try:
            self.progress.emit("loading")
            df = self.fetch_and_validate()

            company_name = self.get_company_name()

            self.progress.emit("calculating")
            X_train, y_train, X_test, y_test, seq_len, scaled = self.predictor.prepare_data(df)

            self.predictor.build_model(seq_len)
            self.predictor.train(X_train, y_train)
            accuracy_metrics = self.predictor.calculate_accuracy(X_test, y_test)
            next_price = self.predictor.predict_next(scaled, seq_len)
            current_price = df["Close"].iloc[-1]

            self.finished.emit({
                "df": df,
                "next_price": next_price,
                "current_price": current_price,
                "symbol": self.symbol,
                "company_name": company_name,  # Dodane!
                "accuracy": accuracy_metrics["accuracy"],
                "rmse": accuracy_metrics["rmse"],
                "mape": accuracy_metrics["mape"]
            })

        except Exception as e:
            self.error.emit(str(e))

# --- Custom Widgety ---

class PlaceholderWidget(AutoRefreshWidget):

    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        self.label = SmartLabel(
            tr_key="placeholder_message",
            alignment="center"
        )
        layout.addWidget(self.label)


class ChartWidget(AutoRefreshWidget):
    def __init__(self):
        super().__init__()
        self.chart_cfg = ThemeManager.get_current_theme().get("chart", {})
        self._setup_canvas()
        self.hide()

    def _setup_canvas(self):
        self.figure = Figure(facecolor=self.chart_cfg.get("bg_color", "white"))
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.canvas)

    def _refresh_content(self):
        self.chart_cfg = ThemeManager.get_current_theme().get("chart", {})
        self.figure.patch.set_facecolor(self.chart_cfg.get("bg_color", "white"))
        if self.isVisible():
            self.canvas.draw()

    def update_chart(self, df, next_price, selected_range="15m"):
        self.figure.clear()

        range_config = PREDICTION_RANGES.get(selected_range, PREDICTION_RANGES["15m"])
        df_plot = df.tail(range_config["tail"]).copy()
        df_plot["Prediction"] = np.nan
        df_plot.iloc[-1, df_plot.columns.get_loc("Prediction")] = next_price

        cfg = self.chart_cfg

        try:
            ax = self.figure.add_axes([0.05, 0.05, 0.97, 0.99])

            mc = mpf.make_marketcolors(
                up=cfg.get("mpf_colors", {}).get("up", "#00aa00"),
                down=cfg.get("mpf_colors", {}).get("down", "#cc0000"),
                wick=cfg.get("mpf_colors", {}).get("wick", "#333"),
                edge=cfg.get("mpf_colors", {}).get("edge", "#333"),
                volume=cfg.get("mpf_colors", {}).get("volume", "in"),
            )

            style_config = cfg.get("mpf_style_config", {})
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
                df_plot["Prediction"],
                scatter=True,
                markersize=cfg.get("prediction_marker", {}).get("size", 200),
                marker=cfg.get("prediction_marker", {}).get("marker", "*"),
                color=cfg.get("prediction_color", "gold"),
                ax=ax,
            )

            mpf.plot(
                df_plot, type="candle", style=style, ylabel="", xrotation=0,
                datetime_format=range_config["dt_format"], addplot=add_plot,
                volume=False, ax=ax, tight_layout=False
            )

            axis_color = style_config.get("edgecolor", "black")
            ax.tick_params(axis='x', colors=axis_color)
            ax.tick_params(axis='y', colors=axis_color)
            for spine in ax.spines.values():
                spine.set_edgecolor(axis_color)

            self.figure.subplots_adjust(0, 0, 1, 1)
            self.figure.patch.set_facecolor(cfg.get("bg_color", "white"))
            self.canvas.draw()
            self.show()

        except Exception as e:
            print(f"Chart error: {e}")


class ControlPanelWidget(AutoRefreshWidget):
    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(5, 5, 5, 5)

        self.inp_symbol = SmartLineEdit(placeholder_key="enter_symbol_placeholder")
        self.cmb_range = SmartComboBox(items=list(PREDICTION_RANGES.keys()))

        CONTROLLER.set_symbol_input(self.inp_symbol)
        CONTROLLER.set_range_combo(self.cmb_range)

        grid = LayoutHelper.create_form_grid([
            ("symbol_label", self.inp_symbol),
            ("prediction_range", self.cmb_range),
        ])
        layout.addLayout(grid)

        self.btn_calc = SmartButton(
            tr_key="calculate_button",
            on_click=CONTROLLER.on_calculate
        )
        CONTROLLER.set_calc_button(self.btn_calc)
        layout.addWidget(self.btn_calc)

        layout.addStretch(1)

    def _refresh_content(self):
        pass


class PriceSummaryWidget(AutoRefreshWidget):
    def __init__(self):
        super().__init__()
        self._current_price = None
        self._predicted_price = None
        self._symbol = None
        self._company_name = None
        self._accuracy = None
        self._setup_ui()
        self.hide()

    def _setup_ui(self):
        theme = ThemeManager.get_current_theme()
        cfg = theme.get("price_summary", {})

        # Główny layout z większymi marginesami z themes
        layout = QVBoxLayout(self)
        margins = cfg.get("margins", (0,0,0,0))
        spacing = cfg.get("spacing", 5)
        layout.setContentsMargins(*margins)
        layout.setSpacing(spacing)

        # RZĄD 1: Nazwa spółki (32px) i dokładność (22px)
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)

        from PySide6.QtWidgets import QLabel as QLabel_native

        # Nazwa spółki - zastosuj symbol_style (32px)
        self.company_name = QLabel_native("")
        self.company_name.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        header_layout.addWidget(self.company_name)

        # Dokładność w nawiasie (22px)
        self.accuracy_label = QLabel_native("")
        self.accuracy_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        header_layout.addWidget(self.accuracy_label)

        header_layout.addStretch()
        layout.addLayout(header_layout)

        # RZĄD 2: Ceny w jednym rzędzie
        prices_layout = QHBoxLayout()
        prices_layout.setSpacing(40)

        # Current Price (lewy blok)
        current_block = QHBoxLayout()
        current_block.setSpacing(10)

        # Tytuł - używa label_style (18px)
        self.current_title = SmartLabel(tr_key="current_price", alignment="left")

        # Wartość - QLabel dla pełnej kontroli
        self.current_value = QLabel_native("--")
        self.current_value.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        current_block.addWidget(self.current_title)
        current_block.addWidget(self.current_value)

        # Predicted Price (prawy blok)
        predicted_block = QHBoxLayout()
        predicted_block.setSpacing(10)

        # Tytuł - używa label_style (18px)
        self.predicted_title = SmartLabel(tr_key="predicted_price", alignment="left")

        # Wartość - QLabel dla pełnej kontroli
        self.predicted_value = QLabel_native("--")
        self.predicted_value.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        predicted_block.addWidget(self.predicted_title)
        predicted_block.addWidget(self.predicted_value)

        # Dodaj oba bloki
        prices_layout.addLayout(current_block)
        prices_layout.addLayout(predicted_block)
        prices_layout.addStretch()

        layout.addLayout(prices_layout)
        layout.addStretch(1)

    def _refresh_content(self):
        theme = ThemeManager.get_current_theme()
        cfg = theme.get("price_summary", {})

        # Styl kontenera (jeśli jest zdefiniowany)
        container_style = cfg.get("container_style", "")
        if container_style:
            self.setStyleSheet(container_style)

        # Zastosuj label_style do tytułów (18px z themes)
        label_style = cfg.get("label_style")
        self.current_title.setStyleSheet(label_style)
        self.predicted_title.setStyleSheet(label_style)

        # PRZYWRÓĆ dane jeśli były wcześniej ustawione
        if self._current_price is not None and self._predicted_price is not None:
            self._apply_display_update()

    def _update_accuracy_display(self, accuracy):

        theme = ThemeManager.get_current_theme()
        cfg = theme.get("price_summary", {})

        acc_text = ThemeManager.get_translation("prediction_accuracy")
        display_text = f"({acc_text}: {accuracy:.1f}%)"

        # Kolorowanie w zależności od wartości
        if accuracy >= 70:
            color = "#00aa00"  # Zielony
        elif accuracy >= 50:
            color = "#ff9900"  # Pomarańczowy
        else:
            color = "#cc0000"  # Czerwony

        base_color = cfg.get("text_color", "#333")

        # Styl dla accuracy (22px z themes - większe niż 20px)
        style = f"font-size: 22px; font-weight: bold; color: {color};"
        self.accuracy_label.setText(display_text)
        self.accuracy_label.setStyleSheet(style)

    def _apply_display_update(self):
        theme = ThemeManager.get_current_theme()
        cfg = theme.get("price_summary", {})

        # Nazwa spółki - zastosuj symbol_style (32px z themes)
        display_name = self._company_name if self._company_name else (self._symbol.upper() if self._symbol else "")
        company_style = cfg.get("symbol_style", "font-size: 32px; font-weight: bold;")
        self.company_name.setText(display_name)
        self.company_name.setStyleSheet(company_style)

        # Dokładność (22px, kolorowana)
        if self._accuracy is not None:
            self._update_accuracy_display(self._accuracy)
        else:
            self.accuracy_label.setText("")

        # Current Price - zastosuj value_style (24px z themes)
        if self._current_price is not None:
            current_text = f"${self._current_price:.2f}"
            value_style = cfg.get("value_style", "font-size: 24px; font-weight: bold;")
            self.current_value.setText(current_text)
            self.current_value.setStyleSheet(value_style)

        # Predicted Price - zastosuj positive_style/negative_style (24px z themes)
        if self._predicted_price is not None:
            predicted_text = f"${self._predicted_price:.2f}"
            self.predicted_value.setText(predicted_text)

            # Kolorowanie z themes
            diff = self._predicted_price - self._current_price

            if diff > 0:
                # Użyj positive_style z themes (24px, zielony)
                style = cfg.get("positive_style", "color: #00aa00; font-size: 24px; font-weight: bold;")
            elif diff < 0:
                # Użyj negative_style z themes (24px, czerwony)
                style = cfg.get("negative_style", "color: #cc0000; font-size: 24px; font-weight: bold;")
            else:
                # Użyj value_style z themes (24px, neutralny)
                style = cfg.get("value_style", "font-size: 24px; font-weight: bold;")

            self.predicted_value.setStyleSheet(style)

    def update_prices(self, current, predicted, symbol, company_name=None, accuracy=None):
        self._current_price = current
        self._predicted_price = predicted
        self._symbol = symbol
        self._company_name = company_name

        # Ekstrakcja accuracy z dict
        if accuracy is not None:
            if isinstance(accuracy, dict) and "accuracy" in accuracy:
                self._accuracy = accuracy["accuracy"]
            elif isinstance(accuracy, (int, float)):
                self._accuracy = accuracy
            else:
                self._accuracy = None
        else:
            self._accuracy = None

        self._apply_display_update()

        self.show()

class PredictionController:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.symbol_input = None
        self.calc_btn = None
        self.selected_range = "15m"
        self.placeholder = None
        self.chart = None
        self.price_summary = None
        self.worker = None

        self._initialized = True

    def set_symbol_input(self, widget):
        self.symbol_input = widget
        widget.textChanged.connect(self._on_symbol_changed)

    def set_calc_button(self, widget):
        self.calc_btn = widget

    def set_range_combo(self, widget):
        widget.setCurrentText("15m")
        widget.currentTextChanged.connect(self._on_range_changed)

    def set_placeholder(self, widget):
        self.placeholder = widget

    def set_chart(self, widget):
        self.chart = widget

    def set_price_summary(self, widget):
        self.price_summary = widget

    def _on_symbol_changed(self, text):
        if self.calc_btn:
            self.calc_btn.setEnabled(bool(text.strip()))

    def _on_range_changed(self, text):
        self.selected_range = text

    def on_calculate(self):
        if not self.symbol_input:
            return

        symbol = self.symbol_input.text().strip().upper()
        if not symbol:
            QMessageBox.warning(
                None,
                ThemeManager.get_translation("error_title"),
                ThemeManager.get_translation("error_no_symbol")
            )
            return

        range_config = PREDICTION_RANGES.get(self.selected_range, PREDICTION_RANGES["15m"])

        if self.calc_btn:
            self.calc_btn.setEnabled(False)

        self.worker = PredictionWorker(symbol, range_config["period"], range_config["interval"])
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_finished(self, result):
        if self.calc_btn:
            self.calc_btn.setEnabled(True)
        if self.placeholder:
            self.placeholder.hide()
        if self.chart:
            self.chart.update_chart(result["df"], result["next_price"], self.selected_range)
        if self.price_summary:
            accuracy_metrics = {
                "accuracy": result.get("accuracy", 0),
                "rmse": result.get("rmse", 0),
                "mape": result.get("mape", 0)
            }
            self.price_summary.update_prices(
                result["current_price"],
                result["next_price"],
                result["symbol"],
                company_name=result.get("company_name"),
                accuracy=accuracy_metrics

            )

    def on_error(self, error_msg):
        if self.calc_btn:
            self.calc_btn.setEnabled(True)

        QMessageBox.critical(
            None,
            ThemeManager.get_translation("error_title"),
            f"{ThemeManager.get_translation('error_prediction')}: {error_msg}"
        )


CONTROLLER = PredictionController()



def get_program_data():
    top_panel = [
        {
            "type": "custom_widget",
            "widget_class": PlaceholderWidget,
            "on_create": CONTROLLER.set_placeholder
        },
        {
            "type": "custom_widget",
            "widget_class": ChartWidget,
            "on_create": CONTROLLER.set_chart
        },
    ]

    bottom_left_panel = [
        {"type": "custom_widget", "widget_class": ControlPanelWidget},
    ]

    bottom_right_panel = [
        {
            "type": "custom_widget",
            "widget_class": PriceSummaryWidget,
            "on_create": CONTROLLER.set_price_summary
        },
    ]

    return "Stock Price Prediction", {
        "gui_type": "top_bottom_split",
        "icon_path": ":/App/Icons/prediction.png",
        "tab_type": "prediction",
        "title": ThemeManager.get_translation("prediction_title"),
        "top_panel": top_panel,
        "bottom_left_panel": bottom_left_panel,
        "bottom_right_panel": bottom_right_panel,
    }