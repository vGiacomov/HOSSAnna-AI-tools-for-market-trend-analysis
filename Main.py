import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from Launcher.Launcher import LauncherWindow, NetworkCheck
from Launcher.SetupWizard import SetupWizard
from App.mainPage import MainWindow
import os
import json
import yfinance as yf
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QInputDialog, QMessageBox, QScrollArea, QSizePolicy
)
from PySide6.QtCore import Qt, QThread, Signal, QUrl, QStandardPaths
from PySide6.QtGui import QDesktopServices, QIcon, QPixmap
import sys
from pathlib import Path
from App.app_state import AppState
from App.translations import TRANSLATIONS
from App.Pages.PredictionThemes import LIGHT_THEME, DARK_THEME
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




class DummyStream:
    def write(self, *args, **kwargs): pass
    def flush(self): pass


if getattr(sys, "frozen", False):
    if sys.stdout is None:
        sys.stdout = DummyStream()
    if sys.stderr is None:
        sys.stderr = DummyStream()

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import tensorflow as tf
tf.get_logger().setLevel("ERROR")




class InitialSettings:
    def __init__(self):
        self.appFolderPath = Path(os.getenv('APPDATA')) / 'HOSSANNA'

        self.isAdmin = False
        self.isConfig = False
        self.isNetwork = False

    def set_admin_value(self, value: bool):
        self.isAdmin = value

    def set_first_start_value(self, value: bool):
        self.isConfig = value

    def set_network_value(self, value: bool):
        self.isNetwork = value





if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("Icons/Logo.ico"))

    # InitialSettings
    settings = InitialSettings()
    print(settings.appFolderPath)
    # Launcher
    launcher = LauncherWindow(settings)
    launcher.show()
    app.exec()

    # Open Setup Wizard if first start
    if not settings.isConfig:
        setupWizard = SetupWizard(settings.appFolderPath)
        setupWizard.show()
        app.exec()

    Aplication = MainWindow()
    Aplication.show()
    app.exec()

    sys.exit(0)



#pyside6-rcc resources.qrc -o resources_rc.py
#pyinstaller --noconfirm --clean --distpath "./dist" --workpath "./build" --name "HOSSAnna" --windowed --onefile --noconsole --icon="./Icons/Logo.ico" --hidden-import=resources_rc main.py
