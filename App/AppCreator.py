import resources_rc

from App.Pages.Prediction import get_program_data
from App.PageTamplate import ModuleTab
from App.themes import LIGHT_THEME, DARK_THEME
from App.App_state import AppState
from App.translations import TRANSLATIONS, languagesList
from App.Pages.HomePage import get_program_data as get_home_data
from Launcher.ConfigManager import ConfigManager
from AppConfigurator import InitialSettings, AppSettings

from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QPushButton, QHBoxLayout,
                               QMessageBox, QLabel, QSizePolicy, QFrame,
                               QMainWindow, QWidget, QStackedWidget, QComboBox,
                               QCheckBox)


class SettingsWindow(QDialog, AppState):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        config = ConfigManager.load_config()
        self.current_language = config["language"]
        self.current_theme = config["theme"]

        self.setWindowTitle(self.tr_text("settings_title"))
        self.setWindowIcon(QIcon(":/Icons/Logo.ico"))
        self.setFixedSize(640, 360)

        self.init_ui()
        self.apply_current_theme()
        self.center_on_parent()

    def center_on_parent(self):
        if self.main_window:
            dialog_geometry = self.frameGeometry()
            dialog_geometry.moveCenter(self.main_window.frameGeometry().center())
            self.move(dialog_geometry.topLeft())

    def tr_text(self, key):
        return TRANSLATIONS.get(self.current_language, TRANSLATIONS["English"]).get(key, key)

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(25)

        # Language section
        self.lang_title = self._create_section_label(self.tr_text("language_label"))
        main_layout.addWidget(self.lang_title)

        self.language_combo = QComboBox()
        self.language_combo.addItems(languagesList)
        self.language_combo.setCurrentText(self.current_language)
        self.language_combo.currentTextChanged.connect(self.on_language_changed)
        main_layout.addWidget(self._center_widget(self.language_combo))

        main_layout.addSpacing(20)

        # Theme section
        self.theme_title = self._create_section_label(self.tr_text("theme_label"))
        main_layout.addWidget(self.theme_title)

        self.theme_checkbox = QCheckBox()
        self.theme_checkbox.setChecked(self.current_theme == "dark")
        self.theme_checkbox.stateChanged.connect(self.on_theme_changed)

        theme_switch = self._create_theme_switch()
        main_layout.addWidget(theme_switch)

        main_layout.addStretch()

        # Buttons
        button_widget = self._create_button_row()
        main_layout.addWidget(button_widget)

    def _create_section_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("font-size: 16px; font-weight: bold;")
        label.setAlignment(Qt.AlignCenter)
        return label

    def _center_widget(self, widget):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.addStretch()
        layout.addWidget(widget)
        layout.addStretch()
        return container

    def _create_theme_switch(self):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setSpacing(15)

        light_label = QLabel("☀️")
        light_label.setStyleSheet("font-size: 18px;")
        dark_label = QLabel("🌙")
        dark_label.setStyleSheet("font-size: 18px;")

        layout.addStretch()
        layout.addWidget(light_label)
        layout.addWidget(self.theme_checkbox)
        layout.addWidget(dark_label)
        layout.addStretch()

        return container

    def _create_button_row(self):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setSpacing(15)

        self.cancel_button = QPushButton(self.tr_text("cancel_button"))
        self.cancel_button.setMinimumWidth(100)
        self.cancel_button.clicked.connect(self.reject)

        self.apply_button = QPushButton(self.tr_text("apply_button"))
        self.apply_button.setMinimumWidth(100)
        self.apply_button.clicked.connect(self.apply_settings)

        layout.addStretch()
        layout.addWidget(self.cancel_button)
        layout.addWidget(self.apply_button)
        layout.addStretch()

        return container

    def on_language_changed(self, language):
        self.current_language = language
        self.update_translations()

    def on_theme_changed(self, state):
        self.current_theme = "dark" if state in (Qt.Checked, 2) else "light"
        self.apply_current_theme()

    def update_translations(self):
        self.setWindowTitle(self.tr_text("settings_title"))
        self.lang_title.setText(self.tr_text("language_label"))
        self.theme_title.setText(self.tr_text("theme_label"))
        self.apply_button.setText(self.tr_text("apply_button"))
        self.cancel_button.setText(self.tr_text("cancel_button"))

    def apply_current_theme(self):
        theme = DARK_THEME if self.current_theme == "dark" else LIGHT_THEME

        combined_style = theme.get("main", "") + theme.get("dialog", "")
        self.setStyleSheet(combined_style)

        if hasattr(self, 'language_combo'):
            self.language_combo.setStyleSheet(theme.get("combobox", ""))

        if hasattr(self, 'theme_checkbox'):
            self.theme_checkbox.setStyleSheet(theme.get("theme_switch", ""))

    def apply_settings(self):
        if ConfigManager.save_config(self.current_language, self.current_theme, terms_accepted=True):
            AppState.set_language(self.current_language)
            AppState.set_theme(self.current_theme)

            self.main_window.apply_theme(self.current_theme)
            self.main_window.current_language = self.current_language

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
            error_msg = ("Failed to save settings!" if self.current_language == "English"
                         else "Nie udało się zapisać ustawień!")
            QMessageBox.critical(
                self,
                "Error" if self.current_language == "English" else "Błąd",
                error_msg
            )


class NavMenu(QFrame, AppState):
    def __init__(self, buttons_config, settings_callback, theme_name="light"):
        super().__init__()
        self.setFixedWidth(60)
        self.current_theme = theme_name
        self.buttons = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 5, 0, 5)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(0)

        layout.addWidget(self._create_spacer(30))

        for config in buttons_config:
            button = self._create_nav_button(config["icon"])
            if "name" in config:
                self.buttons[config["name"]] = button
            button.clicked.connect(config["callback"])
            layout.addWidget(button)

        layout.addWidget(self._create_spacer(0, expanding=True))

        self.settings_button = self._create_nav_button(":/App/Icons/settings.png")
        self.settings_button.clicked.connect(settings_callback)
        layout.addWidget(self.settings_button)

        self.apply_theme(theme_name)

    def apply_theme(self, theme_name):
        self.current_theme = theme_name
        theme = DARK_THEME if theme_name == "dark" else LIGHT_THEME

        self.setStyleSheet(theme.get("nav_menu", ""))

        button_style = theme.get("nav_button", "")
        for button in list(self.buttons.values()) + [self.settings_button]:
            button.setStyleSheet(button_style)

    def _create_nav_button(self, icon_path):
        button = QPushButton()
        button.setFixedSize(50, 50)
        button.setIconSize(QSize(28, 28))
        button.setIcon(QIcon(icon_path))
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


class MainWindow(QMainWindow, AppState):
    def __init__(self):
        super().__init__()

        config = ConfigManager.load_config()
        self.current_language = config["language"]
        self.current_theme = config["theme"]

        self.setWindowTitle(AppSettings.appName)
        self.app_folder_path = AppSettings.app_folder_path
        self.config_path = AppSettings.config_path


        AppState.set_language(self.current_language)
        AppState.set_theme(self.current_theme)

        self.setWindowTitle(AppSettings.appName)
        self.setWindowIcon(QIcon(":/Icons/Logo.ico"))
        self.resize(1280, 720)
        self.setMinimumSize(1280, 720)

        self._init_ui()
        self.apply_theme(self.current_theme)

    def _init_ui(self):
        buttons_config = [
            {
                "name": "home",
                "icon": ":/App/Icons/home.png",
                "callback": lambda: self.change_tab(0)
            },
            {
                "name": "prediction",
                "icon": ":/App/Icons/prediction.png",
                "callback": lambda: self.change_tab(1)
            },
        ]

        self.menu = NavMenu(buttons_config, self.open_settings, self.current_theme)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        self.stacked_widget = QStackedWidget()

        home_name, home_data = get_home_data()
        self.home_tab = ModuleTab(home_name, "get_home_data", home_data)
        self.stacked_widget.addWidget(self.home_tab)

        program_name, program_data = get_program_data()
        self.prediction_tab = ModuleTab("Prediction", "get_program_data", program_data)
        self.stacked_widget.addWidget(self.prediction_tab)

        self.module_tabs = {}
        self.current_module_type = None

        main_layout.addWidget(self.menu)
        main_layout.addWidget(self.stacked_widget)

    def apply_theme(self, theme_name):
        self.current_theme = theme_name
        AppState.set_theme(theme_name)
        theme = DARK_THEME if theme_name == "dark" else LIGHT_THEME

        self.setStyleSheet(theme.get("main", ""))
        self.menu.apply_theme(theme_name)

    def change_tab(self, index):
        self.stacked_widget.setCurrentIndex(index)

    def open_settings(self):
        SettingsWindow(self).exec()


    """ 
     # not use in this project only as backup to not forger. I will remove it later ;)
     def show_module_tab(self, tab_type, title, modules_config):    
         if tab_type in self.module_tabs:
             tab = self.module_tabs[tab_type]
             tab.reset_to_main_page()
         else:
             tab = ModuleTabContainer(tab_type, title, modules_config)
             self.module_tabs[tab_type] = tab
             self.stacked_widget.addWidget(tab)

         self.stacked_widget.setCurrentIndex(self.stacked_widget.indexOf(tab))
         self.current_module_type = tab_type
 """
