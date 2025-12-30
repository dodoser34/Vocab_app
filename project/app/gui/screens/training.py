from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QProgressBar, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer
from ...logic.training_logic import get_training_words, update_progress, check_answer
from project.app.logic.translations import t
from project.app.logic.settings_logic import get_settings

class TrainingScreen(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.setStyleSheet("background:#232323; color:white;")
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(15, 15, 15, 15)

        # TITLE / WORD DISPLAY
        self.word = QLabel("", alignment=Qt.AlignmentFlag.AlignCenter)
        self.word.setStyleSheet("font-size:28px; background:#2b2b2b; padding:15px; border-radius:20px;")
        self.layout.addWidget(self.word)

        # ANSWER INPUT
        self.answer = QLineEdit()
        self.layout.addWidget(self.answer)

        # SUBMIT BUTTON
        self.submit_btn = QPushButton()
        self.submit_btn.setStyleSheet("background:#6f865f; border-radius:25px; font-size:22px; color:white; padding:12px;")
        self.submit_btn.clicked.connect(self.check)
        self.layout.addWidget(self.submit_btn)

        # PROGRESS BAR
        self.progress = QProgressBar()
        self.progress.setStyleSheet("""
            QProgressBar { background:#1f1f1f; border-radius:10px; text-align:center; color:white; }
            QProgressBar::chunk { background:#6f865f; border-radius:10px; }
        """)
        self.layout.addWidget(self.progress)

        # BACK BUTTON
        self.back_btn = QPushButton()
        self.back_btn.setStyleSheet("background:#7b2f2f; border-radius:25px; font-size:22px; color:white; padding:12px;")
        self.back_btn.clicked.connect(self.finish)
        self.layout.addWidget(self.back_btn)

        # TRAINING DATA
        self.words = []
        self.index = 0
        self.current = None


        self.refresh_ui()

    # ===============================
    def start(self, count=20):
        self.words = get_training_words(count)
        self.index = 0
        self.show_word()
        self.refresh_ui()  

    def show_word(self):
        if self.index >= len(self.words):
            self.finish()
            return

        self.current = self.words[self.index]
        self.word.setText(self.current[1])
        self.progress.setValue(int(100 * self.index / len(self.words)))

    def check(self):
        if not self.words or not self.current:
            return

        user_input = self.answer.text()
        if len(user_input) == 0:
            return

        ok = check_answer(self.current[0], user_input, self.current[2])

        if ok:
            self.word.setText(f"{self.current[1]} ✅ {t(get_settings()['language'], 'training', 'correct')}")
        else:
            self.word.setText(f"{self.current[1]} ❌ {t(get_settings()['language'], 'training', 'incorrect')} → {self.current[2]}")

        self.answer.clear()
        self.index += 1
        QTimer.singleShot(800, self.show_word)

    def finish(self):
        self.main.dictionary.refresh()
        self.main.show_menu()

    # ===============================
    def refresh_ui(self):
        lang = get_settings()["language"]
        self.answer.setPlaceholderText(t(lang, "training", "answer_placeholder"))
        self.submit_btn.setText(t(lang, "training", "submit"))
        self.back_btn.setText(t(lang, "training", "back"))
