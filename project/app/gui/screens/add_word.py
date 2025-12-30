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
        root = QVBoxLayout(self)
        root.setContentsMargins(15, 15, 15, 15)
        root.setSpacing(20)

        # ---------- TITLE ----------
        title = QLabel("Add Word")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px;
            background: #2b2b2b;
            color: white;
            padding: 15px;
            border-radius: 25px;
        """)
        root.addWidget(title)

        # ---------- INPUT FIELDS ----------
        self.eng = QLineEdit()
        self.eng.setPlaceholderText("English Word")
        self.eng.setStyleSheet("""
            QLineEdit {
                background: #1f1f1f;
                border-radius: 15px;
                padding: 10px;
                font-size: 18px;
                color: white;
            }
        """)

        self.tr = QLineEdit()
        self.tr.setPlaceholderText("Translation")
        self.tr.setStyleSheet("""
            QLineEdit {
                background: #1f1f1f;
                border-radius: 15px;
                padding: 10px;
                font-size: 18px;
                color: white;
            }
        """)

        self.ex = QTextEdit()
        self.ex.setPlaceholderText("Example (optional)")
        self.ex.setStyleSheet("""
            QTextEdit {
                background: #1f1f1f;
                border-radius: 15px;
                padding: 10px;
                font-size: 18px;
                color: white;
            }
        """)

        root.addWidget(self.eng)
        root.addWidget(self.tr)
        root.addWidget(self.ex)

        # ---------- BUTTONS ----------
        save = QPushButton("Save")
        save.setStyleSheet("""
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
        save.clicked.connect(self.save)

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
        back.clicked.connect(main.show_menu)

        root.addWidget(save)
        root.addWidget(back)

    # ================= SAVE WORD =================
    def save(self):
        add_word(
            self.eng.text(),
            self.tr.text(),
            example=self.ex.toPlainText()
        )
        self.eng.clear()
        self.tr.clear()
        self.ex.clear()
        self.main.show_menu()
