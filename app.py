import streamlit as st

from utils.i18n import map_display_to_code, load_all, load_section

st.set_page_config(page_title="Santo Pharmstat", layout="wide")

language_display = st.sidebar.selectbox(
    "Wybierz język / Select Language / Выберите язык",
    options=["Polski", "English", "Русский"],
    index=0
)
lang = map_display_to_code(language_display)

# t_general — общий раздел меню; t_sa — раздел страницы "Статистический анализ"
t = load_all(lang)
t_general = t["general"]
t_sa = load_section(lang, "statistical_analysis")   # только для названия пункта
t_stab = t["stability_regression"]


# --- Импорт страниц (функции show) один раз ---
from AppPages import Wprowadzenie
from AppPages import descriptive_statistics
from AppPages import control_charts
from AppPages import process_capability
from AppPages import stability_analysis
from AppPages import histogram_analysis
from AppPages import BoxPlot
#from AppPages import statistical_analysis
from AppPages import pqr
# при наличии:
# from AppPages import pqr
# from AppPages import Analiza_temperatury_wilgotnosci

# --- Карта пунктов меню -> функция показа страницы ---
routes = {
    t_general["intro"]:                             lambda: Wprowadzenie.show(language_display),
    t_general["descriptive_statistics"]:            lambda: descriptive_statistics.show(language_display),
    t_general["control_charts"]:                    lambda: control_charts.show(language_display),
    t_general["process_capability"]:                lambda: process_capability.show(language_display),
    t_general["stability_regression"]:              lambda: stability_analysis.show(language_display),
    t_general["histogram_analysis"]:                lambda: histogram_analysis.show(language_display),
    t_general["boxplot_charts"]:                    lambda: BoxPlot.show(language_display),
    t_general["pqr_module"]:                        lambda: pqr.show(language_display),
    # опциональные:
    # t_general["temp_humidity_analysis"]:    lambda: Analiza_temperatury_wilgotnosci.show(language_display),

    # пункт «Статистический анализ» берём ИСКЛЮЧИТЕЛЬНО из t_sa["title"]
    #t_sa["title"]:                          lambda: statistical_analysis.show(language_display),
}

# --- Рендер меню и роутинг ---
st.sidebar.title(t_general["menu_title"])
page = st.sidebar.radio(t_general["choose_page"], list(routes.keys()))
routes[page]()   # вызываем соответствующую функцию
