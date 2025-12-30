from PyQt6.QtWidgets import QWidget, QStackedLayout
from PyQt6.QtCore import Qt
from .screens.menu import MenuScreen
from .screens.add_word import AddWordScreen
from .screens.training import TrainingScreen
from .screens.dictionary import DictionaryScreen
from .screens.settings import SettingsScreen


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vocab App")
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setFixedSize(1000, 800)

        self.stack = QStackedLayout(self)

        self.menu = MenuScreen(self)
        self.add_word = AddWordScreen(self)
        self.training = TrainingScreen(self)
        self.dictionary = DictionaryScreen(self)
        self.settings = SettingsScreen(self)

        for w in (
            self.menu,
            self.add_word,
            self.training,
            self.dictionary,
            self.settings
        ):
            self.stack.addWidget(w)

        self.show_menu()

    def show_menu(self):
        self.menu.update_words()
        self.stack.setCurrentWidget(self.menu)

    def show_add_word(self):
        self.stack.setCurrentWidget(self.add_word)

    def show_training(self):
        self.stack.setCurrentWidget(self.training)
        self.training.start()

    def show_dictionary(self):
        self.stack.setCurrentWidget(self.dictionary)
        self.dictionary.refresh()

    def show_settings(self):
        self.stack.setCurrentWidget(self.settings)