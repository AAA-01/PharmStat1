# AppPages/control_charts.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Импорт классов ImRControlChart и правил SPC
from SPC import ImRControlChart, Rule01, Rule02, Rule03, Rule04, Rule05, Rule06, Rule07, Rule08

# Новый i18n-лоадер
from utils.i18n import map_display_to_code, load_section

__all__ = ["show"]

def show(language_display: str) -> None:
    """
    Страница контрольных карт (I-MR).
    language_display: "Polski" | "English" | "Русский" (из селектора в app.py)
    """
    lang = map_display_to_code(language_display)       # "pl" | "en" | "ru"
    t = load_section(lang, "control_charts")           # словарь переводов для секции

    st.header(t["title"])

    st.write(f"""
**{t['instructions']['header']}:**
- {t['instructions']['upload_file']}
- {t['instructions']['data_format']}
- {t['instructions']['chart_info']}
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

        col_count = df.shape[1]
        if col_count < 2:
            st.error(t["file_handling"]["error_two_columns"])
            return

        # Переименуем первую колонку в "ось времени"/идентификатор наблюдений
        df.rename(columns={df.columns[0]: t["chart_labels"]["time_series"]}, inplace=True)

        # Если колонок > 2 — даём выбрать столбец с данными
        if col_count > 2:
            result_column = st.selectbox(
                t["file_handling"]["select_result_column"],
                df.columns[1:],
                help=t["file_handling"]["select_result_column_help"]
            )
        else:
            result_column = df.columns[1]

        # Копируем выбранную колонку в унифицированное имя
        df[t["chart_labels"]["values"]] = df[result_column]

        # Предпросмотр
        show_data = st.checkbox(t["file_handling"]["show_data_preview"], value=True)
        if show_data:
            st.subheader(t["file_handling"]["data_preview"])
            st.dataframe(df[[t["chart_labels"]["time_series"], t["chart_labels"]["values"]]].head(10))

        # Приведение типов
        df[t["chart_labels"]["time_series"]] = df[t["chart_labels"]["time_series"]].astype(str)
        df[t["chart_labels"]["values"]] = pd.to_numeric(df[t["chart_labels"]["values"]], errors="coerce")
        df.dropna(subset=[t["chart_labels"]["values"]], inplace=True)

        if df.empty:
            st.error(t["file_handling"]["error_no_numeric_data"])
            return

        # Данные для I-MR
        data_array = df[t["chart_labels"]["values"]].to_numpy().reshape(-1, 1)

        chart = ImRControlChart(
            data=data_array,
            xlabel=t["chart_labels"]["observation"],
            ylabel_top=t["chart_labels"]["individual_values"],
            ylabel_bottom=t["chart_labels"]["moving_range"]
        )

        # Линии пределов и правила Вестингауза
        chart.limits = True
        chart.append_rules([
            Rule01(), Rule02(), Rule03(), Rule04(),
            Rule05(), Rule06(), Rule07(), Rule08()
        ])

        # Проверка нормальности индивидуальных значений
        normally_distributed = chart.normally_distributed(
            data=chart.value_I, significance_level=0.05
        )
        st.write(f"{t['analysis_results']['normal_distribution_check']} **{normally_distributed}**")

        # Рендер графика
        chart.plot()
        fig = plt.gcf()
        st.pyplot(fig)

        # Таблички CL/UCL/LCL по желанию
        show_I_data = st.checkbox(t["analysis_results"]["show_I_chart"], value=True)
        show_MR_data = st.checkbox(t["analysis_results"]["show_MR_chart"], value=True)

        if show_I_data:
            df_I = chart.data(0)
            st.write(f"**{t['analysis_results']['I_chart_data']}** (CL, UCL, LCL):")
            st.dataframe(df_I[["CL", "UCL", "LCL"]].reset_index(drop=True))

        if show_MR_data:
            df_MR = chart.data(1)
            st.write(f"**{t['analysis_results']['MR_chart_data']}** (CL, UCL, LCL):")
            st.dataframe(df_MR[["CL", "UCL", "LCL"]].reset_index(drop=True))

        st.write("---")
        st.write(f"{t['analysis_results']['process_stable']} **{chart.stable()}**")

    except Exception as e:
        st.error(f"{t['file_handling']['error_processing_file']}: {e}")
