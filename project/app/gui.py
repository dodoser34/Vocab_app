from PyQt6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QTextEdit,
    QProgressBar, QApplication, QStackedLayout, QScrollArea
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from app.logic import add_word, get_words, update_progress, get_statistics
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vocab Trainer")
        self.resize(500, 650)
        self.base_width = 220
        self.base_height = 60

        self.setStyleSheet("""
            QWidget { background-color: #2e2e2e; color: #f0f0f0; }
            QPushButton { background-color: #4caf50; color: white; border-radius: 10px; font-size: 16px; padding: 10px; }
            QPushButton:hover { background-color: #45a049; }
            QLabel { font-size: 18px; font-weight: bold; }
        """)

        self.stack = QStackedLayout()
        self.setLayout(self.stack)

        self.create_menu()
        self.create_add_word_widget()
        self.create_training_widget()
        self.create_dictionary_widget()

    # ------------------ Главное меню ------------------
    def create_menu(self):
        self.menu_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.menu_widget.setLayout(main_layout)

        header = QLabel("Vocab Trainer")
        header.setFont(QFont("Arial", 26, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header)
        main_layout.addSpacing(20)

        # Последние 10 слов сверху
        self.last_words_layout = QVBoxLayout()
        self.last_words_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        main_layout.addLayout(self.last_words_layout)
        self.update_last_words()
        main_layout.addSpacing(20)

        # Кнопки меню
        self.buttons = []
        buttons_info = [
            ("➕ Добавить слово", self.show_add_word),
            ("📝 Тренировка", lambda: self.start_training(100)),
            ("⏱ Быстрая тренировка", lambda: self.start_training(15)),
            ("⏲ На время", lambda: self.start_training(2, timer=True)),
            ("⚠️ Повторить ошибки", lambda: self.start_training(10, errors_only=True)),
            ("📊 Статистика", self.show_stats),
            ("📖 Словарь", self.show_dictionary)
        ]
        for text, func in buttons_info:
            btn = QPushButton(text)
            btn.setFixedSize(self.base_width, self.base_height)
            btn.clicked.connect(func)
            main_layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignHCenter)
            main_layout.addSpacing(10)
            self.buttons.append(btn)

        main_layout.addStretch(1)
        self.stack.addWidget(self.menu_widget)

    def update_last_words(self):
        # очистка
        while self.last_words_layout.count():
            item = self.last_words_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        last_words = get_words(10)
        if not last_words:
            lbl = QLabel("Нет добавленных слов")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.last_words_layout.addWidget(lbl)
        else:
            for w in last_words:
                lbl = QLabel(f"{w[1]} → {w[2]}")
                lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.last_words_layout.addWidget(lbl)

    # ------------------ Добавление слова ------------------
    def create_add_word_widget(self):
        self.add_word_widget = QWidget()
        layout = QVBoxLayout()
        self.add_word_widget.setLayout(layout)
        self.eng_input = QLineEdit(); self.eng_input.setPlaceholderText("Английское слово")
        self.trans_input = QLineEdit(); self.trans_input.setPlaceholderText("Перевод")
        self.example_input = QTextEdit(); self.example_input.setPlaceholderText("Пример (необязательно)")
        self.save_btn = QPushButton("💾 Сохранить")
        self.save_btn.clicked.connect(self.save_word)
        self.back_btn1 = QPushButton("⬅ Назад")
        self.back_btn1.clicked.connect(lambda: self.show_menu())

        for w in [self.eng_input, self.trans_input, self.example_input, self.save_btn, self.back_btn1]:
            layout.addWidget(w)
        self.stack.addWidget(self.add_word_widget)

    def show_add_word(self):
        self.eng_input.clear()
        self.trans_input.clear()
        self.example_input.clear()
        self.stack.setCurrentWidget(self.add_word_widget)

    def save_word(self):
        add_word(self.eng_input.text(), self.trans_input.text(), example=self.example_input.toPlainText())
        self.eng_input.clear(); self.trans_input.clear(); self.example_input.clear()
        self.update_last_words()
        self.show_menu()

    def show_menu(self):
        self.update_last_words()
        self.stack.setCurrentWidget(self.menu_widget)

    # ------------------ Тренировка ------------------
    def create_training_widget(self):
        self.train_widget = QWidget()
        layout = QVBoxLayout()
        self.train_widget.setLayout(layout)
        self.word_label = QLabel()
        self.word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.answer_input = QLineEdit(); self.answer_input.setPlaceholderText("Введите перевод")
        self.submit_btn = QPushButton("✅ Ответить"); self.submit_btn.clicked.connect(self.check_answer)
        self.progress = QProgressBar()
        self.back_btn2 = QPushButton("⬅ Назад"); self.back_btn2.clicked.connect(self.show_menu)

        for w in [self.word_label, self.answer_input, self.submit_btn, self.progress, self.back_btn2]:
            layout.addWidget(w)
        self.stack.addWidget(self.train_widget)

    def start_training(self, count, errors_only=False, timer=False):
        self.words = get_words(count, errors_only=errors_only)
        self.index = 0
        self.timer_mode = timer
        self.time_left = 120
        if not self.words:
            self.word_label.setText("Нет слов для тренировки")
        else:
            self.show_word()
        self.stack.setCurrentWidget(self.train_widget)
        if self.timer_mode:
            self.qtimer = QTimer()
            self.qtimer.timeout.connect(self.update_timer)
            self.qtimer.start(1000)

    def show_word(self):
        if self.index < len(self.words):
            self.current_word = self.words[self.index]
            self.word_label.setText(self.current_word[1])
            self.answer_input.clear()
            self.progress.setValue(int(100*self.index/len(self.words)))
        else:
            self.show_menu()

    def check_answer(self):
        answer = self.answer_input.text().strip()
        if answer.lower() == self.current_word[2].lower():
            update_progress(self.current_word[0], correct=True)
        else:
            update_progress(self.current_word[0], correct=False)
        self.index += 1
        self.show_word()

    def update_timer(self):
        self.time_left -= 1
        self.progress.setValue(int(100*(120-self.time_left)/120))
        if self.time_left <= 0:
            self.qtimer.stop()
            self.show_menu()

    # ------------------ Статистика ------------------
    def show_stats(self):
        stats = get_statistics()
        msg = f"Всего слов: {stats['total_words']}\n" \
              f"✅ Правильно: {stats['total_correct']}\n" \
              f"❌ Неправильно: {stats['total_incorrect']}\n" \
              f"Точность: {stats['accuracy']}%\n\nСтатистика по дням:\n"
        for day in stats['daily']:
            msg += f"{day[0]}: ✅{day[1]} ❌{day[2]}\n"
        self.word_label.setText(msg)
        self.stack.setCurrentWidget(self.train_widget)

    # ------------------ Полный словарь ------------------
    def create_dictionary_widget(self):
        self.dict_widget = QWidget()
        layout = QVBoxLayout(); self.dict_widget.setLayout(layout)
        self.dict_scroll = QScrollArea(); self.dict_scroll.setWidgetResizable(True)
        container = QWidget(); self.dict_scroll_layout = QVBoxLayout(); container.setLayout(self.dict_scroll_layout)
        self.dict_scroll.setWidget(container)
        self.back_btn_dict = QPushButton("⬅ Назад"); self.back_btn_dict.clicked.connect(self.show_menu)
        layout.addWidget(self.dict_scroll)
        layout.addWidget(self.back_btn_dict)
        self.stack.addWidget(self.dict_widget)

    def show_dictionary(self):
        while self.dict_scroll_layout.count():
            item = self.dict_scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        all_words = get_words(1000)
        for w in all_words:
            lbl = QLabel(f"{w[1]} → {w[2]}")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.dict_scroll_layout.addWidget(lbl)
        self.stack.setCurrentWidget(self.dict_widget)

    # ------------------ Адаптивные кнопки ------------------
    def resizeEvent(self, event):
        scale = min(self.width() / 500, 1.3)
        for btn in self.buttons:
            btn.setFixedSize(int(self.base_width * scale), int(self.base_height * scale))
        super().resizeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
