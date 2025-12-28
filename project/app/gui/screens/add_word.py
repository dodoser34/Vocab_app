from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QTextEdit,
    QPushButton, QLabel
)
from PyQt6.QtCore import Qt
from ...logic import add_word


class AddWordScreen(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.setStyleSheet("background:#232323; color:white;")

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("добавить слово")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size:26px;")
        layout.addWidget(title)

        self.eng = QLineEdit()
        self.eng.setPlaceholderText("английское слово")

        self.tr = QLineEdit()
        self.tr.setPlaceholderText("перевод")

        self.ex = QTextEdit()
        self.ex.setPlaceholderText("пример (необязательно)")

        save = QPushButton("сохранить")
        save.clicked.connect(self.save)

        back = QPushButton("назад")
        back.clicked.connect(main.show_menu)

        for w in (self.eng, self.tr, self.ex, save, back):
            layout.addWidget(w)

    def save(self):
        add_word(
            self.eng.text(),
            self.tr.text(),
            self.ex.toPlainText()
        )
        self.eng.clear()
        self.tr.clear()
        self.ex.clear()
        self.main.show_menu()
