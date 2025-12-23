import resources_rc


from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLineEdit,
                               QPushButton, QHBoxLayout, QDialogButtonBox,
                               QMessageBox, QFileDialog, QLabel,
                               QSizePolicy, QFrame, QMainWindow, QWidget,
                               QStackedWidget, QComboBox, QCheckBox, QGridLayout)
import os
from pathlib import Path

from App.Pages.Prediction import get_program_data
from App.PageTamplate import ModuleTab
from App.TabTemplate import ModuleTabContainer
from App.themes import LIGHT_THEME, DARK_THEME
from App.app_state import AppState
from App.translations import TRANSLATIONS
from App.Pages.HomePage import get_program_data as get_home_data




class SettingsWindow(QDialog, AppState):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # Load current config from main window
        self.current_language = main_window.current_language
        self.current_theme = main_window.current_theme

        self.setWindowTitle(self.tr_text("settings_title"))
        self.setWindowIcon(QIcon(":/App/Icons/settings.png"))
        self.resize(640, 360)
        self.setMaximumSize(850, 480)

        self.init_ui()
        self.apply_current_theme()

        # Center dialog on parent window
        self.center_on_parent()

    def center_on_parent(self):
        """Center the dialog on the parent window"""
        if self.main_window:
            parent_geometry = self.main_window.frameGeometry()
            dialog_geometry = self.frameGeometry()
            center_point = parent_geometry.center()
            dialog_geometry.moveCenter(center_point)
            self.move(dialog_geometry.topLeft())

    def tr_text(self, key):
        return TRANSLATIONS.get(self.current_language, TRANSLATIONS["English"]).get(key, key)

    def get_config_path(self):
        """Get the path to config.txt"""
        appdata_path = os.getenv('APPDATA')
        if not appdata_path:
            return None
        return Path(appdata_path) / 'GPCtools' / 'Configs' / 'config.txt'

    def save_config_file(self):
        """Save settings to config.txt"""
        config_path = self.get_config_path()
        if not config_path:
            return False

        try:
            config_path.parent.mkdir(parents=True, exist_ok=True)

            with open(config_path, 'w', encoding='utf-8') as f:
                f.write(f"language={self.current_language}\n")
                f.write(f"theme={self.current_theme}\n")
                f.write(f"terms_accepted=True\n")

            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(25)

        # Language label - centered
        lang_title = QLabel(self.tr_text("language_label"))
        lang_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        lang_title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(lang_title)

        # Language combo - centered
        lang_combo_widget = QWidget()
        lang_combo_layout = QHBoxLayout(lang_combo_widget)

        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "Polski", "Deutsch", "Français", "Español", "Italiano", "עברית"])
        self.language_combo.setCurrentText(self.current_language)
        self.language_combo.currentTextChanged.connect(self.on_language_changed)

        lang_combo_layout.addStretch()
        lang_combo_layout.addWidget(self.language_combo)
        lang_combo_layout.addStretch()

        main_layout.addWidget(lang_combo_widget)

        # Spacer between sections
        main_layout.addSpacing(20)

        # Theme label - centered
        theme_title = QLabel(self.tr_text("theme_label"))
        theme_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        theme_title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(theme_title)

        # Theme switch - centered
        theme_switch_widget = QWidget()
        theme_switch_layout = QHBoxLayout(theme_switch_widget)
        theme_switch_layout.setSpacing(15)

        light_label = QLabel("☀️")
        light_label.setStyleSheet("font-size: 18px;")

        self.theme_checkbox = QCheckBox()
        self.theme_checkbox.setChecked(self.current_theme == "dark")
        self.theme_checkbox.stateChanged.connect(self.on_theme_changed)

        dark_label = QLabel("🌙")
        dark_label.setStyleSheet("font-size: 18px;")

        theme_switch_layout.addStretch()
        theme_switch_layout.addWidget(light_label)
        theme_switch_layout.addWidget(self.theme_checkbox)
        theme_switch_layout.addWidget(dark_label)
        theme_switch_layout.addStretch()

        main_layout.addWidget(theme_switch_widget)

        # Spacer to push buttons to bottom
        main_layout.addStretch()

        # Buttons - centered
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.setSpacing(15)

        self.cancel_button = QPushButton(self.tr_text("cancel_button"))
        self.cancel_button.setMinimumWidth(100)
        self.cancel_button.clicked.connect(self.reject)

        self.apply_button = QPushButton(self.tr_text("apply_button"))
        self.apply_button.setMinimumWidth(100)
        self.apply_button.clicked.connect(self.apply_settings)

        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.apply_button)
        button_layout.addStretch()

        main_layout.addWidget(button_widget)
        self.setLayout(main_layout)

        # Store references for translations
        self.lang_title = lang_title
        self.theme_title = theme_title

    def on_language_changed(self, language):
        self.current_language = language
        self.update_translations()

    def on_theme_changed(self, state):
        checked = (state == Qt.Checked or state == 2)
        self.current_theme = "dark" if checked else "light"
        self.apply_current_theme()

    def update_translations(self):
        """Update all text elements with current language"""
        self.setWindowTitle(self.tr_text("settings_title"))
        self.lang_title.setText(self.tr_text("language_label"))
        self.theme_title.setText(self.tr_text("theme_label"))
        self.apply_button.setText(self.tr_text("apply_button"))
        self.cancel_button.setText(self.tr_text("cancel_button"))

    def apply_current_theme(self):
        """Apply current theme to settings window"""
        theme = DARK_THEME if self.current_theme == "dark" else LIGHT_THEME

        # Apply main theme
        self.setStyleSheet(theme.get("main", "") + theme.get("dialog", ""))

        # Apply combobox theme
        if hasattr(self, 'language_combo'):
            self.language_combo.setStyleSheet(theme.get("combobox", ""))

        # Apply checkbox theme (for theme switch)
        if hasattr(self, 'theme_checkbox'):
            switch_style = """
                QCheckBox {
                    spacing: 0px;
                }
                QCheckBox::indicator {
                    width: 60px;
                    height: 30px;
                    border-radius: 15px;
                    background-color: %s;
                }
                QCheckBox::indicator:checked {
                    background-color: %s;
                }
                QCheckBox::indicator:unchecked {
                    background-color: %s;
                }
            """ % (
                "#555" if self.current_theme == "dark" else "#ccc",
                "#999" if self.current_theme == "dark" else "#4a4a4a",
                "#666" if self.current_theme == "dark" else "#d6d6c2"
            )
            self.theme_checkbox.setStyleSheet(switch_style)

    def apply_settings(self):
        if self.save_config_file():
            AppState.set_language(self.current_language)
            AppState.set_theme(self.current_theme)

            self.main_window.apply_theme(self.current_theme)
            self.main_window.current_language = self.current_language

            # ODŚWIEŻ AKTYWNĄ ZAKŁADKĘ
            current_widget = self.main_window.stacked_widget.currentWidget()
            if hasattr(current_widget, "refresh_all"):
                current_widget.refresh_all()

            QMessageBox.information(
                self,
                self.tr_text("success_title"),
                self.tr_text("settings_applied")
            )
            self.accept()

        else:
            QMessageBox.critical(
                self,
                "Error" if self.current_language == "English" else "Błąd",
                "Failed to save settings!" if self.current_language == "English"
                else "Nie udało się zapisać ustawień!"
            )


# ----------------------NAV MENU---------------------------------------
class NavMenu(QFrame, AppState):
    def __init__(self, buttons_config, settings_callback, theme_name="light"):
        super().__init__()
        self.setFixedWidth(60)
        self.current_theme = theme_name

        # Apply theme from themes.py
        self.apply_theme(theme_name)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 5, 0, 5)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(0)

        layout.addWidget(self._create_spacer(30))

        self.buttons = {}
        for config in buttons_config:
            button = self._create_nav_button(config["icon"])
            if "name" in config:
                self.buttons[config["name"]] = button
            button.clicked.connect(config["callback"])
            layout.addWidget(button)

        layout.addWidget(self._create_spacer(0, expanding=True))

        # Ustawienia
        self.settings_button = self._create_nav_button(":/App/Icons/settings.png")
        self.settings_button.clicked.connect(settings_callback)
        layout.addWidget(self.settings_button)

    def apply_theme(self, theme_name):
        """Apply theme to navigation menu"""
        self.current_theme = theme_name
        theme = DARK_THEME if theme_name == "dark" else LIGHT_THEME

        # Apply nav menu styles
        self.setStyleSheet(theme.get("nav_menu", ""))

        # Update all buttons with new theme
        if hasattr(self, 'buttons'):
            for button in self.buttons.values():
                button.setStyleSheet(theme.get("nav_button", ""))

        if hasattr(self, 'settings_button'):
            self.settings_button.setStyleSheet(theme.get("nav_button", ""))

    def _create_nav_button(self, icon_path):
        button = QPushButton()

        button.setFixedSize(40, 40)
        button.setIconSize(QSize(24, 24))

        # Ustaw ikonę
        icon = QIcon(icon_path)
        if icon.isNull():
            print(f"⚠️ Icon not loaded: {icon_path}")
        button.setIcon(icon)

        theme = DARK_THEME if self.current_theme == "dark" else LIGHT_THEME
        button.setStyleSheet(theme.get("nav_button", ""))

        return button

    def _create_spacer(self, height=0, expanding=False):
        spacer = QFrame()
        spacer.setFrameShape(QFrame.NoFrame)
        spacer.setStyleSheet("background-color: transparent;")
        if expanding:
            spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        else:
            spacer.setFixedHeight(height)
        return spacer


# ----------------------MAIN WINDOW---------------------------------------
class MainWindow(QMainWindow, AppState):
    def __init__(self):
        super().__init__()

        # Load configuration
        self.load_config()

        # Synchronizuj z globalnym stanem
        AppState.set_language(self.current_language)
        AppState.set_theme(self.current_theme)

        self.setWindowTitle("HOSSAnna")
        self.setWindowIcon(QIcon(":/Icons/Logo.ico"))
        self.resize(1280, 720)
        self.setMinimumSize(1280, 720)

        # Konfiguracja przycisków
        buttons_config = [
            {
                "name": "home",
                "icon": ":/App/Icons/home.png",  # Upewnij się, że masz ikonę home.png lub użyj innej
                "callback": lambda: self.change_tab(0)  # Index 0 to teraz Home
            },
            {
                "name": "prediction",
                "icon": ":/App/Icons/prediction.png",
                "callback": lambda: self.change_tab(1)  # Index 1 to Prediction
            },
        ]

        self.menu = NavMenu(buttons_config, settings_callback=self.open_settings, theme_name=self.current_theme)

        # Układ główny
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Widżety
        self.stacked_widget = QStackedWidget()

        # 1. HOME TAB (Index 0)
        home_name, home_data = get_home_data()
        # Jeśli chcesz, by lewy panel był ukryty dla Home, można to obsłużyć w PageTemplate,
        # ale na razie zostawmy tak jak jest (będzie pusty pasek po lewej, co wygląda ok jako margines).
        self.home_tab = ModuleTab(home_name, "get_home_data", home_data)
        self.stacked_widget.addWidget(self.home_tab)

        # 2. PREDICTION TAB (Index 1)
        program_name, program_data = get_program_data()  # To import z Prediction
        self.prediction_tab = ModuleTab("Prediction", "get_program_data", program_data)
        self.stacked_widget.addWidget(self.prediction_tab)

        self.module_tabs = {}
        self.current_module_type = None

        # Dodajemy do layoutu
        main_layout.addWidget(self.menu)
        main_layout.addWidget(self.stacked_widget)

        # Apply initial theme
        self.apply_theme(self.current_theme)

    def load_config(self):
        """Load configuration from config.txt"""
        config_path = self.get_config_path()

        # Default values
        self.current_language = "English"
        self.current_theme = "light"

        if config_path and config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if '=' in line:
                            key, value = line.split('=', 1)
                            if key == "language":
                                self.current_language = value
                            elif key == "theme":
                                self.current_theme = value
            except Exception as e:
                print(f"Error loading config: {e}")

    def get_config_path(self):
        """Get the path to config.txt"""
        appdata_path = os.getenv('APPDATA')
        if not appdata_path:
            return None
        return Path(appdata_path) / 'GPCtools' / 'Configs' / 'config.txt'

    def apply_theme(self, theme_name):
        """Apply theme to entire application"""
        self.current_theme = theme_name
        AppState.set_theme(theme_name)
        theme = DARK_THEME if theme_name == "dark" else LIGHT_THEME

        # Apply to main window and all widgets
        self.setStyleSheet(theme.get("main", ""))

        # Apply to navigation menu
        self.menu.apply_theme(theme_name)

    def change_tab(self, index):
        self.stacked_widget.setCurrentIndex(index)

    def show_module_tab(self, tab_type, title, modules_config):
        if tab_type in self.module_tabs:
            tab = self.module_tabs[tab_type]
            tab.reset_to_main_page()
        else:
            tab = ModuleTabContainer(tab_type, title, modules_config)
            self.module_tabs[tab_type] = tab
            self.stacked_widget.addWidget(tab)

        index = self.stacked_widget.indexOf(tab)
        self.stacked_widget.setCurrentIndex(index)
        self.current_module_type = tab_type

    def open_settings(self):
        settings_window = SettingsWindow(self)
        settings_window.exec()
