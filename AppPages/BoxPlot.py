import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.data_processing import calculate_descriptive_stats
from utils.translations import translations

def show(language):
    t = translations[language]["boxplot_charts"]

    st.header(t["title"])
    st.write(f"""
    **{t["instructions"]["header"]}:**
    - {t["instructions"]["upload_file"]}
    - {t["instructions"]["select_columns"]}
    - {t["instructions"]["view_stats"]}
    """)

    uploaded_file = st.file_uploader(
        t["file_handling"]["choose_file"],
        type=["xlsx", "xls"]
    )

    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            st.write(f"**{t["file_handling"]["data_preview"]}**")
            st.dataframe(df.head())

            columns = df.columns.tolist()
            selected_columns = st.multiselect(
                t["file_handling"]["select_columns"],
                columns,
                default=columns
            )

            if selected_columns:
                # Generuj wykres BoxPlot
                st.subheader(t["title"])
                fig, ax = plt.subplots(figsize=(10, 6))
                df[selected_columns].boxplot(ax=ax)
                ax.set_title(t["plot"]["title"])
                ax.set_ylabel(t["plot"]["y_label"])
                ax.grid(True)
                st.pyplot(fig)

                # Statystyki opisowe
                st.subheader(t["statistics"]["title"])
                stats = calculate_descriptive_stats(df[selected_columns])
                st.dataframe(stats)

        except Exception as e:
            st.error(f"{t["file_handling"]["error_processing_file"]}: {e}")
    else:
        st.info(t["file_handling"]["no_file_uploaded"])
