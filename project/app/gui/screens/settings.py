from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt


class SettingsScreen(QWidget):
    def __init__(self, main):
        super().__init__()
        self.setStyleSheet("background:#232323; color:white;")

        layout = QVBoxLayout(self)

        title = QLabel("настройки")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size:26px;")
        layout.addWidget(title)

        layout.addWidget(QLabel("• тема интерфейса"))
        layout.addWidget(QLabel("• количество слов в тренировке"))
        layout.addWidget(QLabel("• язык интерфейса"))

        back = QPushButton("назад")
        back.clicked.connect(main.show_menu)
        layout.addWidget(back)
