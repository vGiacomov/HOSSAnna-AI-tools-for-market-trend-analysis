from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QPushButton, QLabel,
    QGridLayout, QScrollArea, QLineEdit, QComboBox, QSizePolicy)
from App.App_state import AppState
from App.Pages.PredictionThemes import LIGHT_THEME, DARK_THEME



def tr_dynamic(key):
    from App.translations import TRANSLATIONS
    lang = AppState.get_language()
    return TRANSLATIONS.get(lang, {}).get(key, key)


def get_theme_style(style_key):
    theme = DARK_THEME if AppState.get_theme() == "dark" else LIGHT_THEME
    val = theme.get(style_key, "")
    return val.get("style", "") if isinstance(val, dict) else val


# --- Inteligentne Widgety ---

class SmartGroupBox(QGroupBox):
    def __init__(self):
        super().__init__()
        AppState.state_changed.connect(self.update_ui)
        self.update_ui()

    def update_ui(self):
        # Pobieramy styl "panel_style" z themes.py
        # Jeśli nie ma go w themes, używamy domyślnego fallbacku
        style = get_theme_style("panel_style")
        if not style:
            # Fallback jeśli zapomnisz dodać do Themes
            border_col = "rgba(255,255,255,0.1)" if AppState.get_theme() == "dark" else "rgba(0,0,0,0.1)"
            bg_col = "#1e1e1e" if AppState.get_theme() == "dark" else "#ffffff"
            style = f"QGroupBox {{ border: 1px solid {border_col}; border-radius: 12px; background-color: {bg_col}; }}"

        self.setStyleSheet(style)


class SmartLabel(QLabel):
    def __init__(self, tr_key=None, text=None, style_key="label", alignment=None):
        super().__init__()
        self.tr_key = tr_key
        self.original_text = text
        self.style_key = style_key

        if alignment == "left":
            self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        elif alignment == "center":
            self.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        elif alignment == "right":
            self.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        AppState.state_changed.connect(self.update_ui)
        self.update_ui()

    def update_ui(self):
        if self.tr_key:
            self.setText(tr_dynamic(self.tr_key))
        elif self.original_text:
            self.setText(self.original_text)
        self.setStyleSheet(get_theme_style(self.style_key))


class SmartButton(QPushButton):
    def __init__(self, tr_key=None, text=None, style_key="button_style", icon=None):
        super().__init__()
        self.tr_key = tr_key
        self.original_text = text
        self.style_key = style_key
        if icon: self.setIcon(QIcon(icon))

        AppState.state_changed.connect(self.update_ui)
        self.update_ui()

    def update_ui(self):
        if self.tr_key:
            self.setText(tr_dynamic(self.tr_key))
        elif self.original_text:
            self.setText(self.original_text)
        self.setStyleSheet(get_theme_style(self.style_key))


# --- Główna Klasa ModuleTab ---

class ModuleTab(QScrollArea):
    def __init__(self, module_name, data_function, module_data):
        super().__init__()
        self.module_name = module_name
        self.module_data = module_data
        self.setup_ui()
        self.create_program_section()

    def setup_ui(self):
        self.setWidgetResizable(True)
        # Domyślny styl ScrollArea (przezroczysty)
        self.setStyleSheet(
            "QScrollArea { border: none; background-color: transparent; } QScrollBar:vertical { width: 0px; }")
        self.scroll_content = QWidget()
        self.main_layout = QVBoxLayout(self.scroll_content)
        self.main_layout.setSpacing(5)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.setWidget(self.scroll_content)

    def create_program_section(self):
        layout_type = self.module_data.get("gui_type", "littlebig")

        section = QWidget()


        if layout_type == "top_bottom_split":
            section_layout = QVBoxLayout(section)
            section_layout.setSpacing(15)
            section_layout.setContentsMargins(5, 5, 5, 5)

            # 1. Top Panel (Wykres)
            top_panel = self._create_panel(self.module_data.get("top_panel", []))
            section_layout.addWidget(top_panel, 1)

            # 2. Bottom Container
            bottom_container = QWidget()
            bottom_layout = QHBoxLayout(bottom_container)
            bottom_layout.setContentsMargins(0, 0, 0, 0)
            bottom_layout.setSpacing(15)  # Odstęp między lewym a prawym dolnym panelem

            # Dolny Lewy
            b_left = self._create_panel(self.module_data.get("bottom_left_panel", []))
            b_left.setFixedWidth(350)  # Stała szerokość panelu sterowania

            # Dolny Prawy
            b_right = self._create_panel(self.module_data.get("bottom_right_panel", []))

            bottom_layout.addWidget(b_left)
            bottom_layout.addWidget(b_right)

            section_layout.addWidget(bottom_container, 0)

        elif layout_type == "sidebar_main":
            section_layout = QHBoxLayout(section)
            section_layout.setSpacing(10)
            section_layout.setContentsMargins(0, 0, 0, 0)

            left_panel = self._create_panel(self.module_data.get("left_panel", []))
            left_panel.setFixedWidth(320)

            right_elements = self.module_data.get("right_panel", []) or self.module_data.get("main_panel", [])
            right_panel = self._create_panel(right_elements)

            section_layout.addWidget(left_panel)
            section_layout.addWidget(right_panel, 1)



        # ... w create_program_section
        elif layout_type == "full_width":
            section_layout = QVBoxLayout(section)
            section_layout.setContentsMargins(0, 0, 0, 0)

            # Tylko jeden główny panel
            main_panel = self._create_panel(self.module_data.get("main_panel", []))
            section_layout.addWidget(main_panel)

        else:
            # Fallback dla starych układów
            section_layout = QHBoxLayout(section)
            left_panel = self._create_panel(self.module_data.get("left_panel", []))
            right_panel = self._create_panel(self.module_data.get("rigthPanel", []))
            section_layout.addWidget(left_panel, 1)
            section_layout.addWidget(right_panel, 2)

        self.main_layout.addWidget(section)

    def _create_panel(self, elements):
        # Używamy SmartGroupBox zamiast zwykłego QGroupBox
        panel = SmartGroupBox()

        layout = QVBoxLayout(panel)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        for el in elements:
            w = self._create_element(el)
            if w: layout.addWidget(w)
        return panel

    def _create_element(self, config):
        if not isinstance(config, dict): return None

        etype = config.get("type")

        if etype == "label":
            return SmartLabel(
                tr_key=config.get("tr_key"),
                text=config.get("text"),
                style_key=config.get("style", "label"),
                alignment=config.get("alignment")
            )

        elif etype == "button":
            btn = SmartButton(
                tr_key=config.get("tr_key"),
                text=config.get("text"),
                style_key=config.get("style", "button_style"),
                icon=config.get("icon")
            )
            if "on_create" in config: config["on_create"](btn)
            if "action" in config: btn.clicked.connect(config["action"])
            return btn

        elif etype == "combobox":
            cb = QComboBox()
            cb.addItems(config.get("items", []))
            style_key = config.get("style", "combobox_style")
            cb.setStyleSheet(get_theme_style(style_key))
            if "on_create" in config: config["on_create"](cb)
            return cb

        elif etype == "lineedit":
            le = QLineEdit()
            le.setText(config.get("text", ""))
            style_key = config.get("style", "lineedit_style")
            le.setStyleSheet(get_theme_style(style_key))
            if "on_create" in config: config["on_create"](le)
            if "action" in config: le.textChanged.connect(config["action"])
            return le

        elif etype == "custom_widget":
            cls = config.get("widget_class")
            if cls:
                w = cls()
                if "on_create" in config: config["on_create"](w)
                return w

        elif etype == "spacer":
            s = QWidget()
            if config.get("expanding", False):
                s.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            else:
                s.setFixedHeight(config.get("height", 10))
                s.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            return s

        return None
