# app.py
import streamlit as st
from utils.i18n import map_display_to_code, load_all, load_section

st.set_page_config(page_title="Santo Pharmstat", layout="wide")

# Выбор языка (человекочитаемый)
language_display = st.sidebar.selectbox(
    "Wybierz język / Select Language / Выберите язык",
    options=["Polski", "English", "Русский"],
    index=0
)
lang_code = map_display_to_code(language_display)  # "pl" | "en" | "ru"

# Загружаем ВСЕ переводы или только нужные секции
t = load_all(lang_code)
t_general = t["general"]
t_sa = t["statistical_analysis"]  # можно было бы load_section(lang_code, "statistical_analysis")

# Меню
st.sidebar.title(t_general["menu_title"])
page = st.sidebar.radio(
    t_general["choose_page"],
    [
        t_general["intro"],
        t_general["descriptive_stats"],
        t_general["control_charts"],
        t_general["process_capability"],
        t_general["stability_regression"],
        t_sa["title"],  # локализованный пункт статистического анализа
    ]
)

# Routing
if page == t_general["intro"]:
    from AppPages import Wprowadzenie
    Wprowadzenie.show(language_display)

elif page == t_general["statistical_analysis"]:
    from AppPages import statistical_analysis
    statistical_analysis.show(language_display)

elif page == t_general["histogram_analysis"]:
    from AppPages import histogram_analysis
    histogram_analysis.show(language_display)

elif page == t_general["boxplot_charts"]:
    from AppPages import BoxPlot
    BoxPlot.show(language_display)

elif page == t_general["descriptive_statistics"]:
    from AppPages import descriptive_statistics
    descriptive_statistics.show(language_display)

elif page == t_general["control_charts"]:
    from AppPages import control_charts
    control_charts.show(language_display)

elif page == t_general["process_capability"]:
    from AppPages import process_capability
    process_capability.show(language_display)

elif page == t_general["stability_regression"]:
    from AppPages import stability_analysis
    stability_analysis.show(language_display)

elif page == t_general["pqr_module"]:  
    from AppPages import pqr
    pqr.show(language_display)

elif page == t_general["temp_humidity_analysis"]:
    from AppPages import Analiza_temperatury_wilgotnosci
    Analiza_temperatury_wilgotnosci.show(language_display)

elif page == t_sa["title"]:
    from AppPages import statistical_analysis
    statistical_analysis.show(language_display)

