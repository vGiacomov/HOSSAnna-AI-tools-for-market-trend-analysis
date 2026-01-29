import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

import AppConfigurator
from Launcher.Launcher import LauncherWindow
from Launcher.SetupWizard import SetupWizard
from App.AppCreator import MainWindow
import os
from PySide6.QtGui import QDesktopServices, QIcon, QPixmap
import sys




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










if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("Launcher/Icons/Logo.ico"))

    launcher = LauncherWindow()
    launcher.show()
    app.exec()

    if not AppConfigurator.InitialSettings.isConfig:
        setupWizard = SetupWizard()
        setupWizard.show()
        app.exec()

    Aplication = MainWindow()
    Aplication.show()
    app.exec()


    sys.exit(0)


