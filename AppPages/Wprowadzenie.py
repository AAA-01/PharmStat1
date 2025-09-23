# AppPages/Wprowadzenie.py
import streamlit as st
from utils.i18n import map_display_to_code, load_section

__all__ = ["show"]

def show(language_display: str) -> None:
    """
    Страница-введение. Берёт тексты из секции 'general' для выбранного языка.
    language_display: "Polski" | "English" | "Русский"
    """
    lang = map_display_to_code(language_display)   # "pl" | "en" | "ru"
    t = load_section(lang, "general")              # словарь переводов general

    # Заголовок и описание
    st.header(t["intro"])
    st.write(t["intro_text"])
    st.write(t["intro_desc"])

    st.markdown("---")

    # Как пользоваться (подзаголовок + пункты)
    st.subheader(t["how_to_use"])
    st.markdown(f"- {t['upload_data']}")
    st.markdown(f"- {t['view_results']}")
    st.markdown(f"- {t['customize_view']}")

    # Подсказка по модулям
    st.markdown("---")
    st.write(
        f"• {t['descriptive_statistics']}  \n"
        f"• {t['control_charts']}  \n"
        f"• {t['process_capability']}  \n"
        f"• {t['stability_regression']}  \n"
        f"• {t['histogram_analysis']}  \n"
        f"• {t['boxplot_charts']}  \n"
        f"• {t['pqr_module']}  \n"
        f"• {t['temp_humidity_analysis']}"
    )
