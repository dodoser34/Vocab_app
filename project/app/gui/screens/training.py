from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QProgressBar
)
from PyQt6.QtCore import Qt
from ...logic import get_words, update_progress


class TrainingScreen(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.setStyleSheet("background:#232323; color:white;")

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(15)

        self.word = QLabel("", alignment=Qt.AlignmentFlag.AlignCenter)
        self.word.setStyleSheet("font-size:28px;")

        self.answer = QLineEdit()
        self.answer.setPlaceholderText("введите перевод")

        submit = QPushButton("ответить")
        submit.clicked.connect(self.check)

        self.progress = QProgressBar()

        back = QPushButton("назад")
        back.clicked.connect(main.show_menu)

        for w in (self.word, self.answer, submit, self.progress, back):
            self.layout.addWidget(w)

        self.words = []
        self.index = 0

    def start(self, count=20):
        self.words = get_words(count)
        self.index = 0
        self.show_word()

    def show_word(self):
        if self.index >= len(self.words):
            self.main.show_menu()
            return

        self.current = self.words[self.index]
        self.word.setText(self.current[1])
        self.progress.setValue(
            int(100 * self.index / len(self.words))
        )

    def check(self):
        ok = self.answer.text().lower() == self.current[2].lower()
        update_progress(self.current[0], ok)
        self.answer.clear()
        self.index += 1
        self.show_word()
