from PyQt6.QtWidgets import QWidget, QStackedLayout
from PyQt6.QtCore import Qt
from .screens.menu import MenuScreen
from .screens.add_word import AddWordScreen
from .screens.training import TrainingScreen
from .screens.dictionary import DictionaryScreen
from .screens.settings import SettingsScreen
from project.app.logic.settings_logic import get_settings

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vocab App")
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setFixedSize(1000, 800)

        self.stack = QStackedLayout(self)
        self.stack.setContentsMargins(0, 0, 0, 0)
        self.stack.setSpacing(0)


        self.menu = MenuScreen(self)
        self.add_word = AddWordScreen(self)
        self.training = TrainingScreen(self)
        self.dictionary = DictionaryScreen(self)
        self.settings = SettingsScreen(self)

        for w in (self.menu, self.add_word, self.training, self.dictionary, self.settings):
            self.stack.addWidget(w)

        self.show_menu()

    # -----------------

    def show_menu(self):
        self.stack.setCurrentWidget(self.menu)
        self.menu.refresh_words()
        self.apply_theme()
        self.apply_language()

    def show_add_word(self):
        self.stack.setCurrentWidget(self.add_word)
        self.apply_theme()
        self.apply_language()

    def show_training(self):
        self.stack.setCurrentWidget(self.training)
        self.training.start()
        self.apply_theme()
        self.apply_language()

    def show_dictionary(self):
        self.stack.setCurrentWidget(self.dictionary)
        self.dictionary.refresh()
        self.apply_theme()
        self.apply_language()

    def show_settings(self):
        self.stack.setCurrentWidget(self.settings)
        self.apply_theme()
        self.apply_language()

    # -----------------

    def apply_theme(self):
        theme = get_settings()["theme"]
        style = "background:#232323; color:white;" if theme == "dark" else "background:#f0f0f0; color:black;"
        self.setStyleSheet(style)
        for screen in (self.menu, self.add_word, self.training, self.dictionary, self.settings):
            if hasattr(screen, "refresh_ui"):
                screen.refresh_ui()

    # -----------------

    def apply_language(self):
        for screen in (self.menu, self.add_word, self.training, self.dictionary, self.settings):
            if hasattr(screen, "refresh_ui"):
                screen.refresh_ui()
