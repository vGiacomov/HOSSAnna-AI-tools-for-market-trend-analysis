from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QComboBox
from PySide6.QtCore import Qt
from App.app_state import AppState
from App.translations import TRANSLATIONS
from App.themes import LIGHT_THEME, DARK_THEME



class ThemeManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    def get_current_theme():
        return DARK_THEME if AppState.get_theme() == "dark" else LIGHT_THEME

    @staticmethod
    def get_style(key, fallback=""):
        theme = ThemeManager.get_current_theme()
        val = theme.get(key, fallback)
        return val.get("style", fallback) if isinstance(val, dict) else val

    @staticmethod
    def get_translation(key, fallback=None):
        lang = AppState.get_language()
        return TRANSLATIONS.get(lang, {}).get(key, fallback or key)

    @staticmethod
    def apply_widget_style(widget, style_key, fallback=""):
        style = ThemeManager.get_style(style_key, fallback)
        if hasattr(widget, 'setStyleSheet'):
            widget.setStyleSheet(style)

    @staticmethod
    def apply_label_style(label, style_key="label"):
        ThemeManager.apply_widget_style(label, style_key)

    @staticmethod
    def apply_button_style(button, style_key="button_style"):
        ThemeManager.apply_widget_style(button, style_key)

    @staticmethod
    def apply_input_style(widget, style_key):
        ThemeManager.apply_widget_style(widget, style_key)

    @staticmethod
    def apply_theme_to_multiple(widgets_config):
        if isinstance(widgets_config, dict):
            widgets_config = widgets_config.items()

        for widget, style_key in widgets_config:
            ThemeManager.apply_widget_style(widget, style_key)



class AutoRefreshWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._connect_refresh_signal()

    def _connect_refresh_signal(self):
        AppState.state_changed.connect(self._auto_refresh)

    def _auto_refresh(self):
        self._refresh_content()

    def _refresh_content(self):
        pass


class SmartLabel(QLabel):
    def __init__(self, tr_key=None, text=None, style_key="label", alignment=None):
        super().__init__()
        self.tr_key = tr_key
        self.static_text = text
        self.style_key = style_key

        if alignment:
            alignment_map = {
                "left": Qt.AlignLeft | Qt.AlignVCenter,
                "center": Qt.AlignCenter,
                "right": Qt.AlignRight | Qt.AlignVCenter,
            }
            self.setAlignment(alignment_map.get(alignment, Qt.AlignLeft | Qt.AlignVCenter))

        AppState.state_changed.connect(self._update)
        self._update()

    def _update(self):
        if self.tr_key:
            self.setText(ThemeManager.get_translation(self.tr_key))
        elif self.static_text:
            self.setText(self.static_text)
        ThemeManager.apply_widget_style(self, self.style_key)


class SmartButton(QPushButton):
    def __init__(self, tr_key=None, text=None, style_key="button_style", on_click=None, icon=None):
        super().__init__()
        self.tr_key = tr_key
        self.static_text = text
        self.style_key = style_key

        if icon:
            from PySide6.QtGui import QIcon
            self.setIcon(QIcon(icon))

        if on_click:
            self.clicked.connect(on_click)

        AppState.state_changed.connect(self._update)
        self._update()

    def _update(self):
        if self.tr_key:
            self.setText(ThemeManager.get_translation(self.tr_key))
        elif self.static_text:
            self.setText(self.static_text)
        ThemeManager.apply_widget_style(self, self.style_key)


class SmartLineEdit(QLineEdit):
    def __init__(self, text="", placeholder_key=None, style_key="lineedit_style"):
        super().__init__(text)
        self.placeholder_key = placeholder_key
        self.style_key = style_key

        AppState.state_changed.connect(self._update)
        self._update()

    def _update(self):
        if self.placeholder_key:
            self.setPlaceholderText(ThemeManager.get_translation(self.placeholder_key))
        ThemeManager.apply_widget_style(self, self.style_key)


class SmartComboBox(QComboBox):
    def __init__(self, items=None, style_key="combobox_style"):
        super().__init__()
        self.style_key = style_key

        if items:
            self.addItems(items)

        AppState.state_changed.connect(self._update)
        self._update()

    def _update(self):
        ThemeManager.apply_widget_style(self, self.style_key)



class LayoutHelper:

    @staticmethod
    def create_label_input_row(label_text_or_key, input_widget, is_translation_key=True):
        if is_translation_key:
            label = SmartLabel(tr_key=label_text_or_key)
        else:
            label = SmartLabel(text=label_text_or_key)

        return label, input_widget

    @staticmethod
    def create_form_grid(fields_config):
        from PySide6.QtWidgets import QGridLayout

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.setColumnStretch(1, 1)

        for row, (label_key, widget) in enumerate(fields_config):
            label = SmartLabel(tr_key=label_key)
            grid.addWidget(label, row, 0)
            grid.addWidget(widget, row, 1)

        return grid
