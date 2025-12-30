from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QPushButton, QFrame
from PyQt6.QtCore import Qt
from ...logic.dictionary_logic import get_full_dictionary
from project.app.logic.translations.translations import t
from project.app.logic.settings_logic import get_settings

class DictionaryScreen(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.setStyleSheet("background:#232323; color:white;")
        self.layout = QVBoxLayout(self)

        # --- TITLE ---
        self.title = QLabel()
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-size:28px; background:#2b2b2b; color:white; padding:15px; border-radius:25px;")
        self.layout.addWidget(self.title)

        # --- SCROLL AREA ---
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background:#1f1f1f; border-radius:25px;")
        self.layout.addWidget(scroll)

        self.container = QWidget()
        self.words_layout = QVBoxLayout(self.container)
        self.words_layout.setSpacing(10)
        scroll.setWidget(self.container)

        # --- BACK BUTTON ---
        self.back_btn = QPushButton()
        self.back_btn.setStyleSheet("background:#6f865f; border-radius:25px; font-size:22px; color:white; padding:12px;")
        self.back_btn.clicked.connect(main.show_menu)
        self.layout.addWidget(self.back_btn)

        # Инициализация текстов
        self.refresh_ui()

    def refresh(self):
        """Обновление списка слов"""
        # Очистка старых виджетов
        for i in reversed(range(self.words_layout.count())):
            item = self.words_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()

        # Получаем слова через логику
        words = get_full_dictionary()

        for w in words:
            row = QWidget()
            row_layout = QVBoxLayout(row)
            row.setStyleSheet("background:#1a1a1a; border-radius:15px; padding:8px;")
            
            lbl_word = QLabel(f"{w[1]} → {w[2]}")  # english → translation
            lbl_word.setStyleSheet("font-size:18px; color:white;")
            row_layout.addWidget(lbl_word)

            line = QFrame()
            line.setFrameShape(QFrame.Shape.HLine)
            line.setStyleSheet("color:#333333; margin:2px 0;")
            row_layout.addWidget(line)

            self.words_layout.addWidget(row)

    # --- Обновление текста по языку ---
    def refresh_ui(self):
        lang = get_settings()["language"]
        self.title.setText(t(lang, "dictionary", "title"))
        self.back_btn.setText(t(lang, "dictionary", "back"))
