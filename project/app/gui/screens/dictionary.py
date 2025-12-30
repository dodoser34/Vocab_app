from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QScrollArea, QPushButton, QFrame
)
from PyQt6.QtCore import Qt
from ...logic import get_words


class DictionaryScreen(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.setStyleSheet("background:#232323; color:white;")
        root = QVBoxLayout(self)
        root.setContentsMargins(15, 15, 15, 15)
        root.setSpacing(20)

        # ---------- TITLE ----------
        title = QLabel("Dictionary")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px;
            background: #2b2b2b;
            color: white;
            padding: 15px;
            border-radius: 25px;
        """)
        root.addWidget(title)

        # ---------- SCROLL AREA ----------
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background:#1f1f1f; border-radius:25px;")
        root.addWidget(scroll)

        self.container = QWidget()
        self.words_layout = QVBoxLayout(self.container)
        self.words_layout.setContentsMargins(15, 15, 15, 15)
        self.words_layout.setSpacing(10)
        self.words_layout.addStretch()
        scroll.setWidget(self.container)

        # ---------- BACK BUTTON ----------
        back = QPushButton("Back")
        back.setStyleSheet("""
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
        back.clicked.connect(main.show_menu)
        root.addWidget(back)

    # ================= REFRESH WORDS =================
    def refresh(self):
        # clear previous items
        for i in reversed(range(self.words_layout.count() - 1)):
            item = self.words_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()

        # add words
        for w in get_words(1000):
            row = QWidget()
            row_layout = QVBoxLayout(row)
            row_layout.setContentsMargins(10, 10, 10, 10)
            row_layout.setSpacing(0)
            row.setStyleSheet("background:#1a1a1a; border-radius:15px; padding:8px;")

            lbl_word = QLabel(f"{w[1]} → {w[2]}")
            lbl_word.setStyleSheet("font-size:18px; color:white;")
            row_layout.addWidget(lbl_word)

            # optional separator
            line = QFrame()
            line.setFrameShape(QFrame.Shape.HLine)
            line.setStyleSheet("color:#333333; margin:2px 0;")
            row_layout.addWidget(line)

            self.words_layout.insertWidget(0, row)
