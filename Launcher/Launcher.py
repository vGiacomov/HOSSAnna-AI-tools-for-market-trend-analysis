import sys
import ctypes
import os
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QProgressBar
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap
from pathlib import Path
import socket



class AdminCheck:
    @staticmethod
    def check_admin_permission():
        if sys.platform == "win32":
            try:
                is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
                return is_admin
            except Exception as e:
                return False
        else:
            return os.geteuid() == 0


class NetworkCheck:
    @staticmethod
    def check_network_connection(timeout=2):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=timeout)
            return True
        except OSError:
            return False


class FirstStartCheck():
    @staticmethod
    def check_first_start():
        appdata_path = os.getenv('APPDATA')
        if appdata_path:
            config_path = Path(appdata_path) / 'GPCtools' / 'Configs' / 'config.txt'

            if config_path.is_file():
                return True
            else:
                return False

        else:
            return False


class LauncherWindow(QWidget):
    def __init__(self, settings):
        super().__init__()

        self.settings = settings
        self.current_step = 0
        self.total_steps = 3  #Lancher Steps

        # Inicjalizacja okna
        self.resize(720, 480)
        self.setFixedSize(720, 480)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        # Ustawienie layoutu
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(50, 50, 50, 50)

        # Logo
        self.logo_label = QLabel()
        pixmap = QPixmap('Launcher/Icons/Logo.png')
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(scaled_pixmap)
        else:
            self.logo_label.setText("HOSSAnna")
            self.logo_label.setStyleSheet("font-size: 48px; font-weight: bold; color: #333;")
        self.logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.logo_label)

        # Status label
        self.status_label = QLabel("Inicjalizacja...")
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

        # Stylowanie okna
        self.setStyleSheet("""
            QWidget {
                background-color: white;
            }
        """)

        QTimer.singleShot(500, self.start_checks)

    def start_checks(self):
        self.check_admin()

    def check_admin(self):
        self.status_label.setText("Checking permissions...")
        self.settings.adminPermission = AdminCheck.check_admin_permission()

        self.current_step += 1
        self.update_progress()
        QTimer.singleShot(800, self.check_network)

    def check_network(self):
        self.status_label.setText("Checking network connection...")
        self.settings.networkConnection = NetworkCheck.check_network_connection()
        self.current_step += 1
        self.update_progress()
        QTimer.singleShot(1000, self.check_first_start)

    def check_first_start(self):
        self.status_label.setText("Checking the configuration...")
        self.settings.firstStart = FirstStartCheck.check_first_start()

        self.current_step += 1
        self.update_progress()

        QTimer.singleShot(1200, self.finish_loading)


    def update_progress(self):
        progress_value = int((self.current_step / self.total_steps) * 100)
        self.progress_bar.setValue(progress_value)

    def finish_loading(self):
        if FirstStartCheck() == True:
            self.status_label.setText("Preparing Setup Configurator")
        else:
            self.status_label.setText("Preparing App")

        self.progress_bar.setValue(100)
        QTimer.singleShot(500, self.close)
