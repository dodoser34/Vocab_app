from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt
from ...logic import get_words


class MenuScreen(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main

        self.setStyleSheet("background:#232323; color:white;")
        root = QVBoxLayout(self)
        root.setContentsMargins(10, 10, 10, 10)

        title = QLabel("Vocab App")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px;
            background: #2b2b2b;
            color: white;
            padding: 15px;
            border-radius: 25px;
        """)
        root.addWidget(title)

        card = QWidget()
        card.setStyleSheet("background:#2b2b2b; border-radius:30px;")
        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(10, 10, 10, 10)
        card_layout.setSpacing(0)
        root.addWidget(card)

        left = QWidget()
        left.setStyleSheet("background:#1f1f1f; border-radius:25px;")
        self.left_layout = QVBoxLayout(left)
        self.left_layout.setContentsMargins(15, 15, 15, 15)
        card_layout.addWidget(left, 1)

        right = QVBoxLayout()
        right.setSpacing(10)
        card_layout.addLayout(right, 1)

        top_space_for_buttons = 25  
        right.addSpacing(top_space_for_buttons)

        def btn(text, color, action):
            b = QPushButton(text)
            b.setFixedHeight(85)
            b.setStyleSheet(f"""
                background: {color};
                border-top-left-radius: 0px;
                border-bottom-left-radius: 0px;
                border-top-right-radius: 42px;
                border-bottom-right-radius: 42px;
                font-size: 25px;
                color: white;
            """)
            b.clicked.connect(action)
            return b

        right.addWidget(btn("добавить слова", "#6f865f", main.show_add_word))
        right.addWidget(btn("начать тренировку", "#7b2f2f", main.show_training))
        right.addWidget(btn("словарь", "#3b3a74", main.show_dictionary))
        right.addWidget(btn("настройки", "#b3b3b3", main.show_settings))
        right.addStretch()


        self.update_words()  

    def update_words(self):
        while self.left_layout.count():
            item = self.left_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        words = get_words(10)
        if not words:
            placeholder = QLabel(
                "Здесь будут\nпоследние\nдобавленные\nслова"
            )
            placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            placeholder.setStyleSheet("color: #aaaaaa; font-size: 18px;")
            self.left_layout.addWidget(placeholder)
        else:
            for w in reversed(words):
                card = QWidget()
                card_layout = QVBoxLayout(card)
                card_layout.setContentsMargins(0, 0, 0, 0)
                card_layout.setSpacing(0)

                row = QWidget()
                row_layout = QHBoxLayout(row)
                row_layout.setContentsMargins(10, 10, 10, 10)
                row_layout.setSpacing(10)
                row.setStyleSheet("background: #1a1a1a; border-radius: 15px;")
                lbl_word = QLabel(f"{w[1]}")
                lbl_word.setStyleSheet("font-size: 20px; font-weight: bold; color: #ffffff;")
                lbl_word.setAlignment(Qt.AlignmentFlag.AlignTop)

                arrow = QLabel("→")
                arrow.setStyleSheet("font-size: 18px; color: #cccccc;")
                arrow.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

                lbl_translation = QLabel(f"{w[2]}")
                lbl_translation.setStyleSheet("font-size: 18px; color: #cccccc;")
                lbl_translation.setAlignment(Qt.AlignmentFlag.AlignTop)

                for i in reversed(range(row_layout.count())):
                    row_layout.itemAt(i).widget().setParent(None)

                row_layout.addStretch(1)
                row_layout.addWidget(lbl_word)
                row_layout.addSpacing(20)
                row_layout.addWidget(arrow)
                row_layout.addSpacing(20)
                row_layout.addWidget(lbl_translation)
                row_layout.addStretch(1)

                card_layout.addWidget(row)

                line = QFrame()
                line.setFrameShape(QFrame.Shape.HLine)
                line.setStyleSheet("color: #333333; margin-top:2px; margin-bottom:2px;")
                card_layout.addWidget(line)

                self.left_layout.addWidget(card)
