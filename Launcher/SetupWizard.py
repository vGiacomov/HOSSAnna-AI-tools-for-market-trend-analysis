import os
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QComboBox, QPushButton,
    QHBoxLayout, QTextEdit, QCheckBox, QStackedWidget
)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QPixmap

from Launcher.ConfigManager import ConfigManager
from Launcher.LauncherThemes import LIGHT_THEME, DARK_THEME
from Launcher.Launcher_translations import languagesList, TRANSLATIONS
from Launcher.TermsOfUse import TOU
from AppConfigurator import InitialSettings, AppSettings


class SetupWizard(QWidget):
    finished = Signal()

    STEP_LANGUAGE = 0
    STEP_THEME = 1
    STEP_TERMS = 2
    STEP_FINAL = 3

    def __init__(self):
        super().__init__()

        # Paths
        self.appFolderPath = AppSettings.app_folder_path()
        self.appName = AppSettings.appName

        # Default selections
        self.selected_language = "English"
        self.selected_theme = "light"
        self.terms_accepted = False

        # Widget references
        self._widgets_to_style = {}
        self._translatable_widgets = {}

        # UI setup
        self.resize(720, 480)
        self.setFixedSize(720, 480)
        self.setWindowTitle(f"{self.appName} Setup")

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(50, 30, 50, 30)
        self.stacked_widget = QStackedWidget()

        self.theme = LIGHT_THEME

        # Create steps
        self.create_language_step()
        self.create_theme_step()
        self.create_terms_step()
        self.create_final_step()

        self.main_layout.addWidget(self.stacked_widget)
        self.setLayout(self.main_layout)

        # Apply theme and translations
        self.apply_theme()
        self.update_translations()

    # Theme / styling
    def apply_theme(self):
        self.theme = DARK_THEME if self.selected_theme == "dark" else LIGHT_THEME
        self.setStyleSheet(self.theme.get("main", ""))

        style_map = {
            "language_combo": "combobox",
            "theme_switch": "theme_switch",
            "accept_checkbox": "checkbox_accept",
            "terms_text": "textedit",
            "finish_button": "finish_button"
        }

        for widget_key, theme_key in style_map.items():
            if widget_key in self._widgets_to_style:
                self._widgets_to_style[widget_key].setStyleSheet(self.theme.get(theme_key, ""))

    @staticmethod
    def is_checked(state):
        return state == Qt.Checked or state == 2

    # Navigation helper
    def create_navigation_buttons(self, back_index=None, next_index=None):
        layout = QHBoxLayout()
        layout.setSpacing(20)
        buttons = []

        if back_index is not None:
            back_btn = QPushButton()
            back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(back_index))
            layout.addWidget(back_btn)
            buttons.append(('back_btn', back_btn))

        if next_index is not None:
            next_btn = QPushButton()
            next_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(next_index))
            layout.addWidget(next_btn)
            buttons.append(('next_btn', next_btn))

        return layout, buttons

    # Steps
    def create_language_step(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        # Title
        title = QLabel()
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        self._translatable_widgets['lang_title'] = title

        layout.addSpacing(30)

        # Language combo
        self.language_combo = QComboBox()
        self.language_combo.addItems(languagesList)
        self.language_combo.currentTextChanged.connect(self.on_language_changed)
        layout.addWidget(self.language_combo, alignment=Qt.AlignCenter)
        self._widgets_to_style["language_combo"] = self.language_combo

        layout.addSpacing(50)

        # Next button
        next_button = QPushButton()
        next_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(self.STEP_THEME))
        layout.addWidget(next_button, alignment=Qt.AlignCenter)
        self._translatable_widgets['lang_next_btn'] = next_button

        widget.setLayout(layout)
        self.stacked_widget.addWidget(widget)

    def create_theme_step(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        title = QLabel()
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        self._translatable_widgets['theme_title'] = title

        layout.addSpacing(30)

        switch_container = QHBoxLayout()
        switch_container.setAlignment(Qt.AlignCenter)
        switch_container.setSpacing(15)

        light_label = QLabel("☀️")
        light_label.setStyleSheet("font-size: 16px;")
        switch_container.addWidget(light_label)

        self.theme_switch = QCheckBox()
        self.theme_switch.stateChanged.connect(self.on_theme_changed)
        switch_container.addWidget(self.theme_switch)
        self._widgets_to_style["theme_switch"] = self.theme_switch

        dark_label = QLabel("🌙")
        dark_label.setStyleSheet("font-size: 16px;")
        switch_container.addWidget(dark_label)

        layout.addLayout(switch_container)

        self.theme_info_label = QLabel()
        self.theme_info_label.setWordWrap(True)
        self.theme_info_label.setAlignment(Qt.AlignCenter)
        self.theme_info_label.setStyleSheet("font-size: 12px; color: #666;")
        layout.addWidget(self.theme_info_label)
        self._translatable_widgets['theme_info'] = self.theme_info_label

        nav_layout, buttons = self.create_navigation_buttons(self.STEP_LANGUAGE, self.STEP_TERMS)
        for key, btn in buttons:
            self._translatable_widgets[f'theme_{key}'] = btn
        layout.addLayout(nav_layout)

        widget.setLayout(layout)
        self.stacked_widget.addWidget(widget)

    def create_terms_step(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)

        title = QLabel()
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        self._translatable_widgets['terms_title'] = title

        # Terms text
        self.terms_text = QTextEdit()
        self.terms_text.setReadOnly(True)
        self.terms_text.setPlainText(TOU.Load_TOU() or "Terms of Use not found.")
        layout.addWidget(self.terms_text)
        self._widgets_to_style["terms_text"] = self.terms_text

        scrollbar = self.terms_text.verticalScrollBar()
        scrollbar.valueChanged.connect(self.check_scroll_position)
        scrollbar.rangeChanged.connect(self.check_scroll_position_on_load)

        # Info label
        self.info_label = QLabel()
        self.info_label.setStyleSheet("font-size: 13px; color: #444;")
        layout.addWidget(self.info_label)
        self._translatable_widgets['terms_info'] = self.info_label

        # Accept checkbox
        self.accept_checkbox = QCheckBox()
        self.accept_checkbox.setEnabled(False)
        self.accept_checkbox.stateChanged.connect(self.on_terms_accepted)
        layout.addWidget(self.accept_checkbox)
        self._widgets_to_style["accept_checkbox"] = self.accept_checkbox
        self._translatable_widgets['terms_accept_cb'] = self.accept_checkbox

        nav_layout, buttons = self.create_navigation_buttons(self.STEP_THEME, self.STEP_FINAL)
        for key, btn in buttons:
            if key == 'next_btn':
                btn.setEnabled(False)
                self.terms_next_button = btn
            self._translatable_widgets[f'terms_{key}'] = btn
        layout.addLayout(nav_layout)

        widget.setLayout(layout)
        self.stacked_widget.addWidget(widget)

    def create_final_step(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        logo_label = QLabel()
        pixmap = QPixmap('Launcher/Icons/Logo.png')
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(300, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        else:
            logo_label.setText(self.appName)
            logo_label.setStyleSheet("font-size: 48px; font-weight: bold;")
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        message = QLabel()
        message.setStyleSheet("font-size: 20px; font-weight: bold;")
        message.setAlignment(Qt.AlignCenter)
        layout.addWidget(message)
        self._translatable_widgets['final_message'] = message

        finish_button = QPushButton()
        finish_button.clicked.connect(self.finish_setup)
        layout.addWidget(finish_button, alignment=Qt.AlignCenter)
        self._widgets_to_style["finish_button"] = finish_button
        self._translatable_widgets['final_finish_btn'] = finish_button

        widget.setLayout(layout)
        self.stacked_widget.addWidget(widget)


    # Event handlers
    def check_scroll_position_on_load(self):
        QTimer.singleShot(100, self.check_scroll_position)

    def check_scroll_position(self):
        scrollbar = self.terms_text.verticalScrollBar()
        if scrollbar.maximum() == 0 or scrollbar.value() >= scrollbar.maximum() - 10:
            self.accept_checkbox.setEnabled(True)
            tr = TRANSLATIONS.get(self.selected_language, TRANSLATIONS["English"])
            self.info_label.setText(tr.get("terms_scroll_info", ""))

    def on_language_changed(self, language):
        self.selected_language = language
        self.update_translations()

    def on_theme_changed(self, state):
        new_theme = "dark" if self.is_checked(state) else "light"
        if new_theme != self.selected_theme:
            self.selected_theme = new_theme
            self.apply_theme()

    def on_terms_accepted(self, state):
        self.terms_accepted = self.is_checked(state)
        self.terms_next_button.setEnabled(self.terms_accepted)

    def update_translations(self):
        tr = TRANSLATIONS.get(self.selected_language, TRANSLATIONS["English"])

        translation_map = {
            'lang_title': 'select_language',
            'lang_next_btn': 'next',
            'theme_title': 'select_theme',
            'theme_info': 'theme_info',
            'theme_back_btn': 'back',
            'theme_next_btn': 'next',
            'terms_title': 'terms_title',
            'terms_info': 'terms_scroll_info',
            'terms_accept_cb': 'terms_accept',
            'terms_back_btn': 'back',
            'terms_next_btn': 'next',
            'final_message': 'setup_done',
            'final_finish_btn': 'finish'
        }

        for widget_key, translation_key in translation_map.items():
            if widget_key in self._translatable_widgets:
                text = tr.get(translation_key, "")
                if text:
                    self._translatable_widgets[widget_key].setText(text)

    # Finish setup
    def finish_setup(self):
        # Ustawienia klasowe
        InitialSettings.set_admin_value(True)
        InitialSettings.set_network_value(True)
        InitialSettings.set_first_start_value(True)

        # Tworzymy strukturę AppData
        ConfigManager.create_appdata_structure(AppSettings.app_folder_path())

        # Zapis konfiguracji
        ConfigManager.save_config(
            language=self.selected_language,
            theme=self.selected_theme,
            terms_accepted=self.terms_accepted,
            app_folder_path=AppSettings.app_folder_path()
        )

        self.finished.emit()
        self.close()
