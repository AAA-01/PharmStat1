# AppPages/BoxPlot.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from utils.data_processing import calculate_descriptive_stats
from utils.i18n import map_display_to_code, load_section  # <-- новый i18n

__all__ = ["show"]

def show(language_display: str) -> None:
    """
    Страница: BoxPlot Charts.
    language_display: "Polski" | "English" | "Русский" (из селектора в app.py)
    """
    lang = map_display_to_code(language_display)       # "pl" | "en" | "ru"
    t = load_section(lang, "boxplot_charts")           # словарь переводов секции

    st.header(t["title"])
    st.write(f"""
**{t['instructions']['header']}:**
- {t['instructions']['upload_file']}
- {t['instructions']['select_columns']}
- {t['instructions']['view_stats']}
""")

    uploaded_file = st.file_uploader(
        t["file_handling"]["choose_file"],
        type=["xlsx", "xls"]
    )

    if uploaded_file is None:
        st.info(t["file_handling"]["no_file_uploaded"])
        return

    try:
        df = pd.read_excel(uploaded_file)

        st.write(f"**{t['file_handling']['data_preview']}**")
        st.dataframe(df.head())

        # Предлагаем выбрать столбцы
        columns = df.columns.tolist()
        selected_columns = st.multiselect(
            t["file_handling"]["select_columns"],
            options=columns,
            default=columns
        )

        if not selected_columns:
            st.warning(t.get("warnings_no_columns", "No columns selected."))
            return

        # --- Построение BoxPlot ---
        st.subheader(t["title"])
        fig, ax = plt.subplots(figsize=(10, 6))
        df[selected_columns].boxplot(ax=ax)
        ax.set_title(t["plot"]["title"])
        ax.set_ylabel(t["plot"]["y_label"])
        ax.grid(True)
        st.pyplot(fig)

        # --- Статистика описательная ---
        st.subheader(t["statistics"]["title"])
        stats = calculate_descriptive_stats(df[selected_columns])
        st.dataframe(stats)

    except Exception as e:
        st.error(f"{t['file_handling']['error_processing_file']}: {e}")
