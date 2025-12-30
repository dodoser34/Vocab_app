SETTINGS = {
    "theme": "dark",   # "dark" или "light"
    "language": "en"   # "en", "ru", "de"
}

def get_settings():
    return SETTINGS.copy()

def set_theme(theme: str):
    if theme in ("dark", "light"):
        SETTINGS["theme"] = theme

def set_language(lang: str):
    if lang in ("en", "ru", "de"):
        SETTINGS["language"] = lang
