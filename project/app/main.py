import sys
from PyQt6.QtWidgets import QApplication
from project.app.db import init_db
from project.app.gui.main_window import MainWindow

if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())