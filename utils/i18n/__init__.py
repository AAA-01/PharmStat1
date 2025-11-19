# utils/i18n/__init__.py
from functools import lru_cache
from importlib import import_module
from typing import Dict, Any, List
from .common import deep_merge

DISPLAY_TO_CODE = {
    "Polski": "pl",
    "English": "en",
    "Русский": "ru",
}

# Секции, которые собираем пакетно (можно заменить через set_sections)
SECTIONS: List[str] = [
    "general",
    "statistical_analysis",
    # "descriptive_statistics",
    # "control_charts",
    # "process_capability",
    "stability_regression",
    # "histogram_analysis",
    # "boxplot_charts",
    # "temp_humidity_analysis",
    # "pqr_module",
]

def set_sections(sections: List[str]) -> None:
    """Позволяет переопределить набор секций, которые грузит load_all()."""
    global SECTIONS
    SECTIONS = list(sections)

def map_display_to_code(display: str) -> str:
    """Преобразует человекочитаемый язык из селектора в код ('pl'|'en'|'ru'), по умолчанию 'pl'."""
    return DISPLAY_TO_CODE.get(display, "pl")

def _normalize_as_mapping(section: str, obj: Any) -> Dict[str, Dict[str, Any]]:
    """
    Привести объект модуля к виду {section: {...}}.
    Допускаются варианты:
      - {section: {...}}         (уже готово)
      - {...}                    (считаем, что это тело нужной секции)
      - None / не dict           -> {}
    """
    if isinstance(obj, dict):
        if section in obj and isinstance(obj[section], dict):
            return {section: obj[section]}
        return {section: obj}
    return {section: {}}

def _import_section(section: str, code: str) -> Dict[str, Dict[str, Any]]:
    """
    Ожидается модуль: utils.i18n.<section>.<code>
    Поддерживаем следующие варианты содержимого модуля:
      - TRANSLATIONS = {section: {...}} ИЛИ {...}
      - translations = {section: {...}} ИЛИ {...}
      - <section> = {...}  (например, general = {...})
    Возвращает всегда словарь формата: {section: {...}}.
    """
    mod = import_module(f"utils.i18n.{section}.{code}")

    # Пытаемся найти подходящую переменную
    obj = (
        getattr(mod, "TRANSLATIONS", None) or
        getattr(mod, "translations", None) or
        getattr(mod, section, None)
    )

    return _normalize_as_mapping(section, obj)

@lru_cache(maxsize=16)
def load_all(language_code: str) -> Dict[str, Dict[str, Any]]:
    """
    Собирает ВСЕ секции для данного языка.
    Порядок фолбэков: <language_code> -> 'en' -> 'ru' -> {}.
    """
    code = language_code if language_code in {"pl", "en", "ru"} else "pl"
    bundle: Dict[str, Dict[str, Any]] = {}

    for section in SECTIONS:
        part: Dict[str, Dict[str, Any]] = {}
        # 1) основной язык
        try:
            part = _import_section(section, code)
        except ModuleNotFoundError:
            part = {}
        # 2) fallback en
        if not part or not part.get(section):
            try:
                fb = _import_section(section, "en")
                # только дополняем отсутствующие ключи
                part = deep_merge(fb, part)
            except ModuleNotFoundError:
                pass
        # 3) fallback ru
        if not part or not part.get(section):
            try:
                fb = _import_section(section, "ru")
                part = deep_merge(fb, part)
            except ModuleNotFoundError:
                pass

        bundle = deep_merge(bundle, part)

    return bundle

@lru_cache(maxsize=64)
def load_section(language_code: str, section: str) -> Dict[str, Any]:
    """
    Загружает одну секцию как обычный dict (тело секции).
    Порядок фолбэков: <language_code> -> 'en' -> 'ru' -> {}.
    """
    # основной язык
    try:
        obj = _import_section(section, language_code)[section]
        if obj:  # если не пустой — возвращаем
            return obj
    except ModuleNotFoundError:
        pass

    # en fallback
    try:
        obj_en = _import_section(section, "en")[section]
    except ModuleNotFoundError:
        obj_en = {}

    # ru fallback
    try:
        obj_ru = _import_section(section, "ru")[section]
    except ModuleNotFoundError:
        obj_ru = {}

    # объединяем (en базовый, language_code дополняет, затем ru дополняет пустоты)
    merged = {}
    merged = deep_merge(merged, obj_en)
    # если основной язык всё же был доступен, он уже бы вернулся выше — но на всякий случай:
    try:
        obj_lang = _import_section(section, language_code)[section]
        merged = deep_merge(merged, obj_lang)
    except ModuleNotFoundError:
        pass
    merged = deep_merge(merged, obj_ru)

    return merged
