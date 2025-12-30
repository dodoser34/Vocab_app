# project/app/logic/translations.py

TRANSLATIONS = {
    "en": {
        "menu": {
            "title": "Vocab App",
            "add_word": "Add Word",
            "training": "Training",
            "dictionary": "Dictionary",
            "settings": "Settings",
        },
        "add_word": {
            "title": "Add Word",
            "english_placeholder": "English Word",
            "translation_placeholder": "Translation",
            "example_placeholder": "Example (optional)",
            "save": "Save",
            "back": "Back",
        },
        "training": {
            "title": "Training",
            "answer_placeholder": "Enter translation",
            "submit": "Submit",
            "back": "Back",
            "correct": "Correct",
            "incorrect": "Incorrect",
        },
        "dictionary": {
            "title": "Dictionary",
            "search_placeholder": "Search word",
            "back": "Back",
        },
        "settings": {
            "title": "Settings",
            "language": "Language",
            "theme": "Theme",
            "back": "Back",
        },
    },
    "ru": {
        "menu": {
            "title": "Словарь",
            "add_word": "Добавить слово",
            "training": "Тренировка",
            "dictionary": "Словарь",
            "settings": "Настройки",
        },
        "add_word": {
            "title": "Добавить слово",
            "english_placeholder": "Английское слово",
            "translation_placeholder": "Перевод",
            "example_placeholder": "Пример (необязательно)",
            "save": "Сохранить",
            "back": "Назад",
        },
        "training": {
            "title": "Тренировка",
            "answer_placeholder": "Введите перевод",
            "submit": "Отправить",
            "back": "Назад",
            "correct": "Верно",
            "incorrect": "Неверно",
        },
        "dictionary": {
            "title": "Словарь",
            "search_placeholder": "Поиск слова",
            "back": "Назад",
        },
        "settings": {
            "title": "Настройки",
            "language": "Язык",
            "theme": "Тема",
            "back": "Назад",
        },
    },
    "de": {
        "menu": {
            "title": "Vokabel App",
            "add_word": "Wort hinzufügen",
            "training": "Training",
            "dictionary": "Wörterbuch",
            "settings": "Einstellungen",
        },
        "add_word": {
            "title": "Wort hinzufügen",
            "english_placeholder": "Englisches Wort",
            "translation_placeholder": "Übersetzung",
            "example_placeholder": "Beispiel (optional)",
            "save": "Speichern",
            "back": "Zurück",
        },
        "training": {
            "title": "Training",
            "answer_placeholder": "Übersetzung eingeben",
            "submit": "Senden",
            "back": "Zurück",
            "correct": "Richtig",
            "incorrect": "Falsch",
        },
        "dictionary": {
            "title": "Wörterbuch",
            "search_placeholder": "Wort suchen",
            "back": "Zurück",
        },
        "settings": {
            "title": "Einstellungen",
            "language": "Sprache",
            "theme": "Thema",
            "back": "Zurück",
        },
    },
}

def t(lang: str, section: str, key: str) -> str:
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(section, {}).get(key, key)