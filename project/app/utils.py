def clean_text(text: str) -> str:
    return text.strip().lower()

def format_tags(tags: str) -> list:
    return [t.strip() for t in tags.split(',') if t.strip()]
