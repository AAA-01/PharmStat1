# utils/i18n/__init__.py
from functools import lru_cache
from importlib import import_module
from .common import deep_merge

DISPLAY_TO_CODE = {
    "Polski": "pl",
    "English": "en",
    "Русский": "ru",
}

# Какие секции собираем (добавляй по мере роста проекта)
SECTIONS = [
    "general",
    "statistical_analysis",
    # "descriptive_statistics", "control_charts", ...
]

def map_display_to_code(display: str) -> str:
    return DISPLAY_TO_CODE.get(display, "pl")

def _import_section(section: str, code: str) -> dict:
    """
    Ожидается модуль: utils.i18n.<section>.<code>
    И в нём переменная TRANSLATIONS = { <section>: {...} } ИЛИ просто {...}
    """
    mod = import_module(f"utils.i18n.{section}.{code}")
    obj = getattr(mod, "TRANSLATIONS", {})
    # Разрешаем два варианта: {section:{...}} или просто {...}
    return obj if section in obj else {section: obj}

@lru_cache(maxsize=16)
def load_all(language_code: str) -> dict:
    """
    Собирает все секции для данного языка, с фолбэком на en при отсутствии.
    """
    code = language_code if language_code in {"pl", "en", "ru"} else "pl"
    bundle = {}
    for section in SECTIONS:
        try:
            part = _import_section(section, code)
        except ModuleNotFoundError:
            # fallback: English → Russian → пусто
            for fb in ("en", "ru"):
                try:
                    part = _import_section(section, fb)
                    break
                except ModuleNotFoundError:
                    part = {}
        bundle = deep_merge(bundle, part)
    return bundle

@lru_cache(maxsize=64)
def load_section(language_code: str, section: str) -> dict:
    """Загрузить только один раздел (с фолбэком на en/ru)."""
    try:
        return _import_section(section, language_code)[section]
    except Exception:
        for fb in ("en", "ru"):
            try:
                return _import_section(section, fb)[section]
            except Exception:
                continue
    return {}
