import sys
from PyQt6.QtWidgets import QApplication
from app.db import init_db
from app.gui import MainWindow

if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
