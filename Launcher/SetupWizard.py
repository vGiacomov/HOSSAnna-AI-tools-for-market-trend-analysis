# setup_wizard.py
import os
from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QComboBox, QPushButton,
    QHBoxLayout, QTextEdit, QCheckBox, QApplication, QStackedWidget)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QPixmap
from pathlib import Path
from PySide6.QtCore import QFile, QIODevice, QTextStream

from Launcher.LauncherThemes import LIGHT_THEME, DARK_THEME
from Launcher.translations import TRANSLATIONS


class ConfigManager:
    @staticmethod
    def create_appdata_structure():
        appdata_path = os.getenv('APPDATA')
        if not appdata_path:
            return False
        base_path = Path(appdata_path) / 'GPCtools'
        configs_path = base_path / 'Configs'
        logs_path = base_path / 'logs'
        try:
            configs_path.mkdir(parents=True, exist_ok=True)
            logs_path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception:
            return False

    @staticmethod
    def save_config(language, theme, terms_accepted):
        appdata_path = os.getenv('APPDATA')
        if not appdata_path:
            return False
        config_path = Path(appdata_path) / 'GPCtools' / 'Configs' / 'config.txt'
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                f.write(f"language={language}\n")
                f.write(f"theme={theme}\n")
                f.write(f"terms_accepted={terms_accepted}\n")
            return True
        except Exception:
            return False


class SetupWizard(QWidget):
    finished = Signal()

    def __init__(self):
        super().__init__()

        # default values
        self.selected_language = "English"
        self.selected_theme = "light"
        self.terms_accepted = False
        self.scrolled_to_bottom = False
        self._widgets_to_style = {}

        # UI
        self.resize(720, 480)
        self.setFixedSize(720, 480)
        self.setWindowTitle("Setup Wizard")

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(50, 30, 50, 30)
        self.stacked_widget = QStackedWidget()

        self.theme = LIGHT_THEME if self.selected_theme == "light" else DARK_THEME

        self.create_language_step()
        self.create_theme_step()
        self.create_terms_step()
        self.create_final_step()

        self.main_layout.addWidget(self.stacked_widget)
        self.setLayout(self.main_layout)

        self.apply_theme_initial()
        self.update_translations()

    # -------------------------
    # Theme / styling
    # -------------------------
    def apply_theme_initial(self):
        self.setStyleSheet(self.theme.get("main", ""))
        for key, widget in self._widgets_to_style.items():
            if key == "language_combo":
                widget.setStyleSheet(self.theme.get("combobox", ""))
            elif key == "theme_switch":
                widget.setStyleSheet(self.theme.get("theme_switch", ""))
            elif key == "accept_checkbox":
                widget.setStyleSheet(self.theme.get("checkbox_accept", ""))
            elif key == "terms_text":
                widget.setStyleSheet(self.theme.get("textedit", ""))
            elif key == "finish_button":
                widget.setStyleSheet(self.theme.get("finish_button", ""))

    def apply_theme_when_toggled(self):
        self.theme = DARK_THEME if self.selected_theme == "dark" else LIGHT_THEME
        self.apply_theme_initial()

    # -------------------------
    # Steps
    # -------------------------
    def create_language_step(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        title = QLabel()
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        layout.addSpacing(30)

        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "Polski", "Deutsch", "Français", "Español", "Italiano","עברית"])
        self.language_combo.currentTextChanged.connect(self.on_language_changed)
        layout.addWidget(self.language_combo, alignment=Qt.AlignCenter)
        self._widgets_to_style["language_combo"] = self.language_combo

        layout.addSpacing(50)
        next_button = QPushButton()
        next_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        layout.addWidget(next_button, alignment=Qt.AlignCenter)

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

        layout.addSpacing(30)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)
        back_button = QPushButton()
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        buttons_layout.addWidget(back_button)

        next_button = QPushButton()
        next_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        buttons_layout.addWidget(next_button)
        layout.addLayout(buttons_layout)

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

        self.terms_text = QTextEdit()
        self.terms_text.setReadOnly(True)
        terms_content = self.load_terms_from_file()
        self.terms_text.setPlainText(terms_content or "Terms of Use not found. Please add a terms.txt file.")
        layout.addWidget(self.terms_text)
        self._widgets_to_style["terms_text"] = self.terms_text

        scrollbar = self.terms_text.verticalScrollBar()
        scrollbar.valueChanged.connect(self.check_scroll_position)
        scrollbar.rangeChanged.connect(self.check_scroll_position_on_load)

        self.info_label = QLabel()
        self.info_label.setStyleSheet("font-size: 13px; color: #444;")
        layout.addWidget(self.info_label)

        self.accept_checkbox = QCheckBox()
        self.accept_checkbox.setEnabled(False)
        self.accept_checkbox.stateChanged.connect(self.on_terms_accepted)
        layout.addWidget(self.accept_checkbox)
        self._widgets_to_style["accept_checkbox"] = self.accept_checkbox

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)

        back_button = QPushButton()
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        buttons_layout.addWidget(back_button)

        self.terms_next_button = QPushButton()
        self.terms_next_button.setEnabled(False)
        self.terms_next_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        buttons_layout.addWidget(self.terms_next_button)

        layout.addLayout(buttons_layout)
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
            logo_label.setText("GPCtools")
            logo_label.setStyleSheet("font-size: 48px; font-weight: bold;")
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        message = QLabel()
        message.setStyleSheet("font-size: 20px; font-weight: bold;")
        message.setAlignment(Qt.AlignCenter)
        layout.addWidget(message)

        finish_button = QPushButton()
        finish_button.clicked.connect(self.finish_setup)
        layout.addWidget(finish_button, alignment=Qt.AlignCenter)
        self._widgets_to_style["finish_button"] = finish_button

        widget.setLayout(layout)
        self.stacked_widget.addWidget(widget)

    # -------------------------
    # Helper functions
    # -------------------------
    def load_terms_from_file(self):
        file = QFile(":/Launcher/terms/terms.txt")
        if not file.open(QIODevice.ReadOnly | QIODevice.Text):
            return None

        stream = QTextStream(file)
        stream.setEncoding("UTF-8")
        content = stream.readAll()
        file.close()
        return content


    def check_scroll_position_on_load(self):
        QTimer.singleShot(100, self.check_scroll_position)

    def check_scroll_position(self):
        scrollbar = self.terms_text.verticalScrollBar()
        if scrollbar.maximum() == 0 or scrollbar.value() >= scrollbar.maximum() - 10:
            self.scrolled_to_bottom = True
            self.accept_checkbox.setEnabled(True)
            self.info_label.setText(TRANSLATIONS.get(self.selected_language, TRANSLATIONS["English"])["terms_scroll_info"])

    def on_language_changed(self, language):
        self.selected_language = language
        self.update_translations()

    def on_theme_changed(self, state):
        checked = (state == Qt.Checked or state == 2)
        new_theme = "dark" if checked else "light"
        if new_theme != self.selected_theme:
            self.selected_theme = new_theme
            self.apply_theme_when_toggled()

    def on_terms_accepted(self, state):
        self.terms_accepted = (state == Qt.Checked or state == 2)
        self.terms_next_button.setEnabled(self.terms_accepted)

    def update_translations(self):
        tr = TRANSLATIONS.get(self.selected_language, TRANSLATIONS["English"])
        # Language step
        w0 = self.stacked_widget.widget(0)
        w0.findChild(QLabel).setText(tr["select_language"])
        w0.findChild(QPushButton).setText(tr["next"])
        # Theme step
        w1 = self.stacked_widget.widget(1)
        w1.findChildren(QLabel)[0].setText(tr["select_theme"])
        w1.findChildren(QPushButton)[0].setText(tr["back"])
        w1.findChildren(QPushButton)[1].setText(tr["next"])
        self.theme_info_label.setText(tr["theme_info"])
        # Terms step
        w2 = self.stacked_widget.widget(2)
        w2.findChildren(QLabel)[0].setText(tr["terms_title"])
        self.info_label.setText(tr["terms_scroll_info"])
        self.accept_checkbox.setText(tr["terms_accept"])
        w2.findChildren(QPushButton)[0].setText(tr["back"])
        w2.findChildren(QPushButton)[1].setText(tr["next"])
        # Final step
        w3 = self.stacked_widget.widget(3)
        w3.findChildren(QLabel)[1].setText(tr["setup_done"])
        self._widgets_to_style["finish_button"].setText(tr["finish"])

    def update_translations(self):
        tr = TRANSLATIONS.get(self.selected_language, TRANSLATIONS["English"])

        # --- Language step ---
        language_widget = self.stacked_widget.widget(0)
        language_labels = language_widget.findChildren(QLabel)
        if language_labels:
            language_labels[0].setText(tr.get("select_language", "Select Language"))

        language_buttons = language_widget.findChildren(QPushButton)
        if language_buttons:
            language_buttons[0].setText(tr.get("next", "Next →"))

        # --- Theme step ---
        theme_widget = self.stacked_widget.widget(1)
        theme_labels = theme_widget.findChildren(QLabel)
        if theme_labels:
            theme_labels[0].setText(tr.get("select_theme", "Select Theme"))
            if hasattr(self, "theme_info_label"):
                self.theme_info_label.setText(tr.get("theme_info", ""))

        theme_buttons = theme_widget.findChildren(QPushButton)
        if theme_buttons:
            theme_buttons[0].setText(tr.get("back", "← Back"))
            theme_buttons[1].setText(tr.get("next", "Next →"))

        # --- Terms step ---
        terms_widget = self.stacked_widget.widget(2)
        terms_labels = terms_widget.findChildren(QLabel)
        if terms_labels:
            terms_labels[0].setText(tr.get("terms_title", "Terms of Use"))
            if hasattr(self, "info_label"):
                self.info_label.setText(tr.get("terms_scroll_info", ""))

        if hasattr(self, "accept_checkbox"):
            self.accept_checkbox.setText(tr.get("terms_accept", ""))

        terms_buttons = terms_widget.findChildren(QPushButton)
        if terms_buttons:
            terms_buttons[0].setText(tr.get("back", "← Back"))
            terms_buttons[1].setText(tr.get("next", "Next →"))

        # --- Final step ---
        final_widget = self.stacked_widget.widget(3)
        final_labels = final_widget.findChildren(QLabel)
        if final_labels:
            final_labels[1].setText(tr.get("setup_done", "Setup Completed!"))

        final_buttons = final_widget.findChildren(QPushButton)
        if final_buttons:
            final_buttons[0].setText(tr.get("finish", "Finish Setup"))

    def finish_setup(self):
        ConfigManager.create_appdata_structure()
        ConfigManager.save_config(
            self.selected_language,
            self.selected_theme,
            self.terms_accepted
        )
        self.finished.emit()
        self.close()
