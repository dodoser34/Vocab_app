from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton
from PyQt6.QtCore import Qt
from ...logic.add_word_logic import add_word
from project.app.logic.translations import t
from project.app.logic.settings_logic import get_settings

class AddWordScreen(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.setStyleSheet("background:#232323; color:white;")
        self.root = QVBoxLayout(self)
        self.root.setContentsMargins(15, 15, 15, 15)
        self.root.setSpacing(20)

        # --- TITLE ---
        self.title = QLabel()
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("""
            font-size: 28px;
            background: #2b2b2b;
            color: white;
            padding: 15px;
            border-radius: 25px;
        """)
        self.root.addWidget(self.title)

        # --- INPUT FIELDS ---
        self.eng = QLineEdit()
        self.eng.setStyleSheet("background: #1f1f1f; border-radius: 15px; padding: 10px; font-size: 18px; color: white;")
        self.tr = QLineEdit()
        self.tr.setStyleSheet("background: #1f1f1f; border-radius: 15px; padding: 10px; font-size: 18px; color: white;")
        self.ex = QTextEdit()
        self.ex.setStyleSheet("background: #1f1f1f; border-radius: 15px; padding: 10px; font-size: 18px; color: white;")

        self.root.addWidget(self.eng)
        self.root.addWidget(self.tr)
        self.root.addWidget(self.ex)

        # --- BUTTONS ---
        self.save_btn = QPushButton()
        self.save_btn.setStyleSheet("background: #6f865f; border-radius: 25px; font-size: 22px; color: white; padding: 12px;")
        self.save_btn.clicked.connect(self.save)

        self.back_btn = QPushButton()
        self.back_btn.setStyleSheet("background: #7b2f2f; border-radius: 25px; font-size: 22px; color: white; padding: 12px;")
        self.back_btn.clicked.connect(main.show_menu)

        self.root.addWidget(self.save_btn)
        self.root.addWidget(self.back_btn)

        # Устанавливаем начальные тексты
        self.refresh_ui()

    def save(self):
        english = self.eng.text().strip()
        translation = self.tr.text().strip()
        example = self.ex.toPlainText().strip()

        if not english or not translation:
            print("Error: You must fill in the English word and its translation")
            return

        add_word(english, translation, example=example)

        self.eng.clear()
        self.tr.clear()
        self.ex.clear()
        self.main.show_menu()

    # --- Обновление текстов по языку ---
    def refresh_ui(self):
        lang = get_settings()["language"]
        self.title.setText(t(lang, "add_word", "title"))
        self.eng.setPlaceholderText(t(lang, "add_word", "english_placeholder"))
        self.tr.setPlaceholderText(t(lang, "add_word", "translation_placeholder"))
        self.ex.setPlaceholderText(t(lang, "add_word", "example_placeholder"))
        self.save_btn.setText(t(lang, "add_word", "save"))
        self.back_btn.setText(t(lang, "add_word", "back"))
