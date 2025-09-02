import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import shapiro, skew, kurtosis
from utils.translations import translations

def show(language):
    t = translations[language]["histogram_analysis"]

    st.header(t["title"])

    st.write(f"""
    **{t["instructions"]["header"]}:**
    - {t["instructions"]["upload_file"]}
    - {t["instructions"]["select_column"]}
    - {t["instructions"]["normality_test"]}
    """)

    uploaded_file = st.file_uploader(t["file_handling"]["choose_file"], type=["xlsx", "xls"])

    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            columns = df.columns.tolist()

            selected_column = st.selectbox(t["file_handling"]["select_column"], columns)

            data = df[selected_column].dropna()

            show_data = st.checkbox(t["file_handling"]["show_data_preview"], value=True)
            if show_data:
                st.subheader(t["file_handling"]["data_preview"])
                st.dataframe(data.head(10))

            plt.figure(figsize=(15, 10))
            plt.hist(data, color="lightgrey", edgecolor="black", bins=20, density=True, label="Histogram")
            sns.kdeplot(data, color="blue", label="Gęstość danych")
            plt.title(t["plot"]["histogram_title"])
            plt.xlabel(t["plot"]["x_label"])
            plt.ylabel(t["plot"]["y_label"])
            plt.legend()
            st.pyplot(plt.gcf())

            st.subheader(t["statistics"]["sample_size"])
            st.write(f"**{t['statistics']['sample_size']}:** {len(data)}")
            st.write(f"**{t['statistics']['mean']}:** {round(data.mean(), 2)}")
            st.write(f"**{t['statistics']['std_dev']}:** {round(data.std(), 2)}")
            st.write(f"**{t['statistics']['max']}:** {data.max()}")
            st.write(f"**{t['statistics']['min']}:** {data.min()}")
            st.write(f"**{t['statistics']['median']}:** {np.median(data)}")
            st.write(f"**{t['statistics']['rsd']}:** {round((data.std() / data.mean()) * 100, 2)}%")

            st.subheader(t["statistics"]["shapiro_test"])
            stat, p_value = shapiro(data)
            st.write(f"**{t['statistics']['shapiro_test']}:** statystyka = {round(stat, 4)}, p-wartość = {round(p_value, 4)}")
            if p_value > 0.05:
                st.success(t["normality_results"]["normal_distribution"])
            else:
                st.error(t["normality_results"]["non_normal_distribution"])

            st.subheader(f"{t['statistics']['skewness']} i {t['statistics']['kurtosis']}")
            st.write(f"**{t['statistics']['skewness']}:** {round(skew(data), 2)}")
            st.write(f"**{t['statistics']['kurtosis']}:** {round(kurtosis(data), 2)}")

        except Exception as e:
            st.error(f"{t['file_handling']['error_processing_file']}: {e}")
    else:
        st.info(t["file_handling"]["no_file_uploaded"])
