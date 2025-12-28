import sys
import ctypes
import os
import socket
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QProgressBar
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap
import AppConfigurator

class AdminCheck:
    @staticmethod
    def check_admin_permission():
        if sys.platform == "win32":
            try:
                is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
                return is_admin
            except Exception:
                return False
        else:
            try:
                return os.geteuid() == 0
            except AttributeError:
                return False


class NetworkCheck:
    @staticmethod
    def check_network_connection(host="8.8.8.8", port=53, timeout=2):
        try:
            with socket.create_connection((host, port), timeout=timeout) as conn:
                return True
        except (socket.timeout, OSError):
            return False


class ConfigCheck:
    @staticmethod
    def config_exists(appFolderPath):
        if not appFolderPath:
            return False

        config_path = appFolderPath / 'Configs' / 'config.txt'
        return config_path.is_file()


class LauncherWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.current_step = 0

        self.steps = [
            (
                AdminCheck.check_admin_permission,
                AppConfigurator.InitialSettings.set_admin_value,
                200,
                "Checking permissions..."
            ),
            (
                NetworkCheck.check_network_connection,
                AppConfigurator.InitialSettings.set_network_value,
                400,
                "Checking network connection..."
            ),
            (
                lambda: ConfigCheck.config_exists(AppConfigurator.AppSettings.app_folder_path()),
                AppConfigurator.InitialSettings.set_first_start_value,
                600,
                "Checking configuration..."
            ),
        ]

        self.total_steps = len(self.steps)

        # Window initialization
        self.resize(720, 480)
        self.setFixedSize(720, 480)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        # Setup layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(50, 50, 50, 50)

        # Logo
        self.logo_label = QLabel()
        pixmap = QPixmap(':/Launcher/Icons/Logo.png')
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(scaled_pixmap)
        else:
            self.logo_label.setText(self.settings.appName)
            self.logo_label.setStyleSheet("font-size: 48px; font-weight: bold; color: #333;")
        self.logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.logo_label)

        # Status label
        self.status_label = QLabel("Initialization...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 14px; color: #666; margin: 20px;")
        layout.addWidget(self.status_label)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #ccc;
                border-radius: 5px;
                text-align: center;
                height: 30px;
                background-color: #f0f0f0;
            }
            QProgressBar::chunk {
                background-color: #d6d6c2;
                border-radius: 3px;
            }
        """)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)
        self.setStyleSheet("""QWidget {background-color: white;}""")

        # Start checks after 500ms
        QTimer.singleShot(500, self.execute_next_step)

    def execute_next_step(self):
        if self.current_step < self.total_steps:
            check_func, setter_func, delay, status_text = self.steps[self.current_step]
            self.status_label.setText(status_text)

            # Execute check and store result
            result = check_func()
            setter_func(result)

            self.update_progress()

            if self.current_step < self.total_steps:
                QTimer.singleShot(delay, self.execute_next_step)
            else:
                QTimer.singleShot(delay, self.finish_loading)

    def update_progress(self):
        self.current_step += 1
        progress_value = int((self.current_step / self.total_steps) * 100)
        self.progress_bar.setValue(progress_value)

    def finish_loading(self):
        if not AppConfigurator.InitialSettings.isConfig:
            self.status_label.setText("Preparing Setup Configurator...")
        else:
            self.status_label.setText("Preparing Application...")

        self.progress_bar.setValue(100)
        QTimer.singleShot(500, self.close)

    def return_values(self):
        return self.settings
