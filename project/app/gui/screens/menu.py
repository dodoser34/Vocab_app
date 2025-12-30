from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame, QGraphicsOpacityEffect
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QParallelAnimationGroup
from ...logic.menu_logic import get_latest_words
from project.app.logic.translations.translations import t
from project.app.logic.settings_logic import get_settings

class MenuScreen(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.setStyleSheet("background:#232323; color:white;")
        root = QVBoxLayout(self)
        root.setContentsMargins(10, 10, 10, 10)

        # TITLE
        self.title = QLabel()
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("""
            font-size: 28px;
            background: #2b2b2b;
            color: white;
            padding: 15px;
            border-radius: 25px;
        """)
        root.addWidget(self.title)

        # CARD
        card = QWidget()
        card.setStyleSheet("background:#2b2b2b; border-radius:30px;")
        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(10, 10, 10, 10)
        card_layout.setSpacing(0)
        root.addWidget(card)

        # LEFT (WORDS)
        left = QWidget()
        left.setStyleSheet("background:#1f1f1f; border-radius:25px;")
        left.setFixedWidth(460)
        self.left_layout = QVBoxLayout(left)
        self.left_layout.setContentsMargins(15, 15, 15, 15)
        self.left_layout.setSpacing(6)
        card_layout.addWidget(left)

        # RIGHT (BUTTONS)
        right = QVBoxLayout()
        right.setSpacing(10)
        card_layout.addLayout(right, 1)
        right.addSpacing(25)

        self.btn_add_word_wrapper = self.create_button("Add Word", "#6f865f", main.show_add_word)
        self.btn_training_wrapper = self.create_button("Training", "#7b2f2f", main.show_training)
        self.btn_dictionary_wrapper = self.create_button("Dictionary", "#3b3a74", main.show_dictionary)
        self.btn_settings_wrapper = self.create_button("Settings", "#b3b3b3", main.show_settings)

        right.addWidget(self.btn_add_word_wrapper)
        right.addWidget(self.btn_training_wrapper)
        right.addWidget(self.btn_dictionary_wrapper)
        right.addWidget(self.btn_settings_wrapper)
        right.addStretch()

        self.refresh_words()
        self.refresh_ui()

    # ------------------------------

    def create_button(self, text, color, action):
        wrapper = QWidget()
        wrapper.setFixedHeight(85)
        layout = QVBoxLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)

        b = QPushButton(text)
        b.setFixedSize(480, 85)
        b.setStyleSheet(f"""
            QPushButton {{
                background: {color};
                border-top-left-radius: 0px;
                border-bottom-left-radius: 0px;
                border-top-right-radius: 42px;
                border-bottom-right-radius: 42px;
                font-size: 25px;
                color: white;
            }}
        """)
        b.clicked.connect(action)
        layout.addWidget(b)

        # hover анимация
        anim = QPropertyAnimation(b, b"pos")
        anim.setDuration(220)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        def enterEvent(e):
            anim.stop()
            anim.setStartValue(b.pos())
            anim.setEndValue(QPoint(18, 0))
            anim.start()
            return QPushButton.enterEvent(b, e)

        def leaveEvent(e):
            anim.stop()
            anim.setStartValue(b.pos())
            anim.setEndValue(QPoint(0, 0))
            anim.start()
            return QPushButton.leaveEvent(b, e)

        b.enterEvent = enterEvent
        b.leaveEvent = leaveEvent


        wrapper.button = b

        return wrapper

    # ------------------------------

    def refresh_words(self):
        while self.left_layout.count():
            item = self.left_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        words = get_latest_words(10)

        if not words:
            placeholder = QLabel(t(get_settings()["language"], "menu", "title"))
            placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            placeholder.setStyleSheet("color:#aaaaaa; font-size:18px;")
            self.left_layout.addWidget(placeholder)
            return

        for w in reversed(words):
            card = QWidget()
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(0, 0, 0, 0)
            card_layout.setSpacing(0)

            row = QWidget()
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(10, 10, 10, 10)
            row_layout.setSpacing(10)
            row.setStyleSheet("background:#1a1a1a; border-radius:15px;")

            lbl_word = QLabel(w[1])
            lbl_word.setStyleSheet("font-size:20px; font-weight:bold;")
            arrow = QLabel("→")
            arrow.setStyleSheet("font-size:18px; color:#cccccc;")
            lbl_translation = QLabel(w[2])
            lbl_translation.setStyleSheet("font-size:18px; color:#cccccc;")

            row_layout.addStretch()
            row_layout.addWidget(lbl_word)
            row_layout.addSpacing(20)
            row_layout.addWidget(arrow)
            row_layout.addSpacing(20)
            row_layout.addWidget(lbl_translation)
            row_layout.addStretch()

            card_layout.addWidget(row)

            line = QFrame()
            line.setFrameShape(QFrame.Shape.HLine)
            line.setStyleSheet("color:#333333; margin:2px 0;")
            card_layout.addWidget(line)

            self.left_layout.addWidget(card)

            # APPEAR ANIMATION
            opacity = QGraphicsOpacityEffect(row)
            row.setGraphicsEffect(opacity)
            opacity.setOpacity(0)

            fade = QPropertyAnimation(opacity, b"opacity", row)
            fade.setDuration(300)
            fade.setStartValue(0)
            fade.setEndValue(1)
            fade.setEasingCurve(QEasingCurve.Type.OutCubic)

            row.move(row.x(), row.y() + 12)
            slide = QPropertyAnimation(row, b"pos", row)
            slide.setDuration(300)
            slide.setStartValue(row.pos())
            slide.setEndValue(row.pos() - QPoint(0, 12))
            slide.setEasingCurve(QEasingCurve.Type.OutCubic)

            group = QParallelAnimationGroup(row)
            group.addAnimation(fade)
            group.addAnimation(slide)
            group.start()

    # ------------------------------

    def refresh_ui(self):
        lang = get_settings()["language"]
        self.title.setText(t(lang, "menu", "title"))
        self.btn_add_word_wrapper.button.setText(t(lang, "menu", "add_word"))
        self.btn_training_wrapper.button.setText(t(lang, "menu", "training"))
        self.btn_dictionary_wrapper.button.setText(t(lang, "menu", "dictionary"))
        self.btn_settings_wrapper.button.setText(t(lang, "menu", "settings"))
