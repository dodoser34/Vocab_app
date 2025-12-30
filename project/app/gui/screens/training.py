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
        self.layout.setContentsMargins(15, 15, 15, 15)

        # ---------- WORD ----------
        self.word = QLabel("", alignment=Qt.AlignmentFlag.AlignCenter)
        self.word.setStyleSheet("""
            font-size: 28px;
            background: #2b2b2b;
            padding: 15px;
            border-radius: 20px;
        """)
        self.layout.addWidget(self.word)

        # ---------- ANSWER FIELD ----------
        self.answer = QLineEdit()
        self.answer.setPlaceholderText("Enter translation")
        self.answer.setStyleSheet("""
            QLineEdit {
                background: #1f1f1f;
                border-radius: 15px;
                padding: 10px;
                font-size: 20px;
                color: white;
            }
        """)
        self.layout.addWidget(self.answer)

        # ---------- SUBMIT BUTTON ----------
        submit = QPushButton("Submit")
        submit.setStyleSheet("""
            QPushButton {
                background: #6f865f;
                border-radius: 25px;
                font-size: 22px;
                color: white;
                padding: 12px;
            }
            QPushButton:hover {
                background: #7a956d;
            }
        """)
        submit.clicked.connect(self.check)
        self.layout.addWidget(submit)

        # ---------- PROGRESS BAR ----------
        self.progress = QProgressBar()
        self.progress.setStyleSheet("""
            QProgressBar {
                background: #1f1f1f;
                border-radius: 10px;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background: #6f865f;
                border-radius: 10px;
            }
        """)
        self.layout.addWidget(self.progress)

        # ---------- BACK BUTTON ----------
        back = QPushButton("Back")
        back.setStyleSheet("""
            QPushButton {
                background: #7b2f2f;
                border-radius: 25px;
                font-size: 22px;
                color: white;
                padding: 12px;
            }
            QPushButton:hover {
                background: #8e3b3b;
            }
        """)
        back.clicked.connect(self.finish)
        self.layout.addWidget(back)

        self.words = []
        self.index = 0

    # ================= START TRAINING =================
    def start(self, count=20):
        self.words = get_words(count)
        self.index = 0
        self.show_word()

    def show_word(self):
        if self.index >= len(self.words):
            self.finish()
            return

        self.current = self.words[self.index]
        self.word.setText(self.current[1])
        self.progress.setValue(int(100 * self.index / len(self.words)))

    # ================= CHECK ANSWER =================
    def check(self):
        if not self.words:
            return

        ok = self.answer.text().strip().lower() == self.current[2].strip().lower()
        update_progress(self.current[0], ok)
        self.answer.clear()
        self.index += 1
        self.show_word()

    # ================= FINISH TRAINING =================
    def finish(self):
        # refresh dictionary to avoid frozen words
        self.main.dictionary.refresh()
        self.main.show_menu()
