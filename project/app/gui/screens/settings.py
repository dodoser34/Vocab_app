from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QFrame
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint
from ...logic.settings_logic import get_settings, set_language, set_theme
from project.app.logic.translations.translations import t


LANGUAGES = [("English", "en"), ("Русский", "ru"), ("Deutsch", "de")]
THEMES = [("Dark", "dark"), ("Light", "light")]

class SettingsScreen(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.setStyleSheet("background:#232323; color:white;")
        root = QVBoxLayout(self)
        root.setContentsMargins(15, 15, 15, 15)
        root.setSpacing(20)

        # --- TITLE ---
        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("""
            font-size: 28px;
            background: #2b2b2b;
            color: white;
            padding: 15px;
            border-radius: 25px;
        """)
        root.addWidget(self.title_label)

        # --- BUTTONS ---
        self.lang_btn = QPushButton()
        self.lang_btn.setStyleSheet("background:#3b3b3b; border-radius:20px; font-size:20px; padding:12px; color:white;")
        self.lang_btn.clicked.connect(self.show_language_options)
        root.addWidget(self.lang_btn)

        self.theme_btn = QPushButton()
        self.theme_btn.setStyleSheet("background:#3b3b3b; border-radius:20px; font-size:20px; padding:12px; color:white;")
        self.theme_btn.clicked.connect(self.show_theme_options)
        root.addWidget(self.theme_btn)

        self.back_btn = QPushButton()
        self.back_btn.setStyleSheet("background:#7b2f2f; border-radius:25px; font-size:22px; color:white; padding:12px;")
        self.back_btn.clicked.connect(main.show_menu)
        root.addWidget(self.back_btn)

        # --- POPUP ---
        self.popup = QFrame(self)
        self.popup.setStyleSheet("background:#1f1f1f; border-radius:25px;")
        self.popup.setLayout(QVBoxLayout())
        self.popup.layout().setContentsMargins(20, 20, 20, 20)
        self.popup.layout().setSpacing(10)
        self.popup.hide()
        self.anim = None

        self.refresh_ui()

    # --- REFRESH UI ---
    def refresh_ui(self):
        lang = get_settings()["language"]
        self.title_label.setText(t(lang, "settings", "title"))
        self.lang_btn.setText(t(lang, "settings", "language"))
        self.theme_btn.setText(t(lang, "settings", "theme"))
        self.back_btn.setText(t(lang, "settings", "back"))

    # --- SHOW OPTIONS ---
    def show_language_options(self):
        self.show_popup([name for name, _ in LANGUAGES], self.select_language)

    def show_theme_options(self):
        self.show_popup([name for name, _ in THEMES], self.select_theme)

    # --- POPUP HANDLER ---
    def show_popup(self, options, callback):
        for i in reversed(range(self.popup.layout().count())):
            w = self.popup.layout().itemAt(i).widget()
            if w:
                w.deleteLater()

        for opt in options:
            btn = QPushButton(opt)
            btn.setStyleSheet("background:#2b2b2b; border-radius:15px; font-size:18px; color:white; padding:8px;")
            btn.clicked.connect(lambda _, o=opt: self.popup_option_selected(o, callback))
            self.popup.layout().addWidget(btn)

        self.popup.setFixedHeight(60 * len(options))
        self.popup.setFixedWidth(self.width() - 100)
        self.popup.move(50, self.height())
        self.popup.show()

        start_pos = self.popup.pos()
        end_pos = start_pos - QPoint(0, self.popup.height() + 280)
        self.anim = QPropertyAnimation(self.popup, b"pos")
        self.anim.setDuration(1050)
        self.anim.setStartValue(start_pos)
        self.anim.setEndValue(end_pos)
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.anim.start()

    def popup_option_selected(self, option, callback):
        callback(option)
        self.close_popup()

    def close_popup(self):
        if self.popup.isVisible():
            start_pos = self.popup.pos()
            end_pos = start_pos + QPoint(0, self.popup.height() + 280)
            self.anim = QPropertyAnimation(self.popup, b"pos")
            self.anim.setDuration(1000)
            self.anim.setStartValue(start_pos)
            self.anim.setEndValue(end_pos)
            self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
            self.anim.finished.connect(self.popup.hide)
            self.anim.start()

    # --- CALLBACKS ---
    def select_language(self, lang_name):
        code = next((code for name, code in LANGUAGES if name == lang_name), "en")
        set_language(code)
        self.refresh_ui()
        self.main.apply_language()
        self.main.apply_theme()

    def select_theme(self, theme_name):
        code = next((code for name, code in THEMES if name == theme_name), "dark")
        set_theme(code)
        self.refresh_ui()
        self.main.apply_theme()
