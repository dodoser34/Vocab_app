from PyQt6.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QMessageBox, QHBoxLayout, QProgressBar)
from PyQt6.QtCore import QTimer, Qt
from app.logic import add_word, get_words, update_progress, get_statistics

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vocab Trainer ПК")
        self.resize(500, 600)
        self.setStyleSheet("font-family: Arial; font-size: 14px;")

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.header = QLabel("Vocab Trainer")
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header.setStyleSheet("font-size: 24px; font-weight: bold; margin: 10px;")
        layout.addWidget(self.header)

        # Кнопки тренировок
        self.btn_add_word = QPushButton("➕ Добавить слово")
        self.btn_training = QPushButton("📝 Тренировка 10 слов")
        self.btn_fast_5 = QPushButton("⏱ Быстрая тренировка 5 слов")
        self.btn_fast_2min = QPushButton("⏲ 2 минуты")
        self.btn_errors = QPushButton("⚠️ Повторить ошибки")
        self.btn_stats = QPushButton("📊 Статистика")
        for btn in [self.btn_add_word, self.btn_training, self.btn_fast_5, self.btn_fast_2min, self.btn_errors, self.btn_stats]:
            btn.setMinimumHeight(40)
            layout.addWidget(btn)

        # Фильтры
        self.filter_layout = QHBoxLayout()
        self.type_filter = QLineEdit(); self.type_filter.setPlaceholderText("Тип слова")
        self.tag_filter = QLineEdit(); self.tag_filter.setPlaceholderText("Тег")
        self.filter_layout.addWidget(self.type_filter)
        self.filter_layout.addWidget(self.tag_filter)
        layout.addLayout(self.filter_layout)

        # Подключаем кнопки
        self.btn_add_word.clicked.connect(self.show_add_word)
        self.btn_training.clicked.connect(lambda: self.start_training(10))
        self.btn_fast_5.clicked.connect(lambda: self.start_training(5))
        self.btn_fast_2min.clicked.connect(lambda: self.start_training(2, timer=True))
        self.btn_errors.clicked.connect(lambda: self.start_training(10, errors_only=True))
        self.btn_stats.clicked.connect(self.show_stats)

    def show_add_word(self):
        self.add_word_window = AddWordWindow()
        self.add_word_window.show()

    def start_training(self, count, errors_only=False, timer=False):
        self.training_window = TrainingWindow(count, errors_only, timer,
                                              self.type_filter.text(), self.tag_filter.text())
        self.training_window.show()

    def show_stats(self):
        stats = get_statistics()
        msg = f"Всего слов: {stats['total_words']}\n" \
              f"✅ Правильно: {stats['total_correct']}\n" \
              f"❌ Неправильно: {stats['total_incorrect']}\n" \
              f"Точность: {stats['accuracy']}%\n\nСтатистика по дням:\n"
        for day in stats['daily']:
            msg += f"{day[0]}: ✅{day[1]} ❌{day[2]}\n"
        QMessageBox.information(self, "Статистика", msg)


class AddWordWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить слово")
        self.resize(400, 450)
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.english = QLineEdit(); self.english.setPlaceholderText("Английское слово")
        self.translation = QLineEdit(); self.translation.setPlaceholderText("Перевод")
        self.type_ = QLineEdit(); self.type_.setPlaceholderText("Тип слова")
        self.example = QTextEdit(); self.example.setPlaceholderText("Пример предложения (необязательно)")
        self.tags = QLineEdit(); self.tags.setPlaceholderText("Теги через запятую")
        self.btn_save = QPushButton("💾 Сохранить")

        layout.addWidget(self.english)
        layout.addWidget(self.translation)
        layout.addWidget(self.type_)
        layout.addWidget(self.example)
        layout.addWidget(self.tags)
        layout.addWidget(self.btn_save)

        self.btn_save.clicked.connect(self.save_word)

    def save_word(self):
        add_word(self.english.text(), self.translation.text(),
                 self.type_.text(), example=self.example.toPlainText(),
                 tags=self.tags.text())
        QMessageBox.information(self, "Успех", "Слово добавлено!")
        self.close()


class TrainingWindow(QWidget):
    def __init__(self, limit=10, errors_only=False, timer=False, type_filter=None, tag_filter=None):
        super().__init__()
        self.setWindowTitle("Тренировка")
        self.resize(500, 450)
        self.setStyleSheet("font-size: 16px;")

        self.words = get_words(limit, tags=tag_filter, types=type_filter, errors_only=errors_only)
        self.index = 0
        self.timer_mode = timer

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.word_label = QLabel()
        self.word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.word_label.setStyleSheet("font-size: 20px; margin: 20px;")
        self.answer_input = QLineEdit()
        self.answer_input.setPlaceholderText("Введите перевод")
        self.btn_submit = QPushButton("✅ Ответить")
        self.progress = QProgressBar()
        self.progress.setMaximum(100)

        self.layout.addWidget(self.word_label)
        self.layout.addWidget(self.answer_input)
        self.layout.addWidget(self.btn_submit)
        self.layout.addWidget(self.progress)

        self.btn_submit.clicked.connect(self.check_answer)

        # Таймер для 2 минуты
        if self.timer_mode:
            self.time_left = 120
            self.qtimer = QTimer()
            self.qtimer.timeout.connect(self.update_timer)
            self.qtimer.start(1000)

        self.show_word()

    def update_timer(self):
        self.time_left -= 1
        self.progress.setValue(int(100*(120-self.time_left)/120))
        if self.time_left <= 0:
            self.qtimer.stop()
            QMessageBox.information(self, "Время вышло", "Сессия 2 минуты завершена!")
            self.close()

    def show_word(self):
        if self.index < len(self.words):
            self.current_word = self.words[self.index]
            self.word_label.setText(self.current_word[1])
            self.answer_input.clear()
            self.progress.setValue(int(100*self.index/len(self.words)))
        else:
            QMessageBox.information(self, "Готово", "Тренировка завершена!")
            self.close()

    def check_answer(self):
        answer = self.answer_input.text().strip()
        correct_translation = self.current_word[2]
        if answer.lower() == correct_translation.lower():
            update_progress(self.current_word[0], correct=True)
            QMessageBox.information(self, "✅", "Правильно!")
        else:
            update_progress(self.current_word[0], correct=False)
            QMessageBox.information(self, "❌", f"Неправильно. Правильный ответ: {correct_translation}")
        self.index += 1
        self.show_word()
