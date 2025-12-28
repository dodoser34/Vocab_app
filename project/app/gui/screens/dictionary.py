from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QScrollArea, QPushButton
)
from PyQt6.QtCore import Qt
from ...logic import get_words


class DictionaryScreen(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.setStyleSheet("background:#232323; color:white;")

        layout = QVBoxLayout(self)

        title = QLabel("словарь")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size:26px;")
        layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        self.words_layout = QVBoxLayout(container)
        scroll.setWidget(container)

        back = QPushButton("назад")
        back.clicked.connect(main.show_menu)

        layout.addWidget(scroll)
        layout.addWidget(back)

    def refresh(self):
        while self.words_layout.count():
            item = self.words_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for w in get_words(1000):
            self.words_layout.addWidget(
                QLabel(f"{w[1]} → {w[2]}")
            )
