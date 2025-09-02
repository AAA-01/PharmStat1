import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.translations import translations

# Import klasy ImRControlChart i reguł z biblioteki SPC
from SPC import ImRControlChart, Rule01, Rule02, Rule03, Rule04, Rule05, Rule06, Rule07, Rule08

def show(language):
    t = translations[language]["control_charts"]

    st.header(t["title"])

    st.write(f"""
    **{t["instructions"]["header"]}:**
    - {t["instructions"]["upload_file"]}
    - {t["instructions"]["data_format"]}
    - {t["instructions"]["chart_info"]}
    """)

    uploaded_file = st.file_uploader(
        t["file_handling"]["choose_file"],
        type=["xlsx", "xls"]
    )

    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)

            col_count = df.shape[1]
            if col_count < 2:
                st.error(t["file_handling"]["error_two_columns"])
                return

            # Nazwij pierwszą kolumnę jako identyfikatory serii
            df.rename(columns={df.columns[0]: t["chart_labels"]["time_series"]}, inplace=True)

            # Jeśli jest więcej niż 2 kolumny, pozwól użytkownikowi wybrać kolumnę z wynikami
            if col_count > 2:
                result_column = st.selectbox(
                    t["file_handling"]["select_result_column"],
                    df.columns[1:],
                    help=t["file_handling"]["select_result_column_help"]
                )
            else:
                result_column = df.columns[1]

            # Przypisz wybraną kolumnę do zmiennej 'values'
            df[t["chart_labels"]["values"]] = df[result_column]

            show_data = st.checkbox(t["file_handling"]["show_data_preview"], value=True)
            if show_data:
                st.subheader(t["file_handling"]["data_preview"])
                st.dataframe(df[[t["chart_labels"]["time_series"], t["chart_labels"]["values"]]].head(10))

            df[t["chart_labels"]["time_series"]] = df[t["chart_labels"]["time_series"]].astype(str)
            df[t["chart_labels"]["values"]] = pd.to_numeric(df[t["chart_labels"]["values"]], errors='coerce')
            df.dropna(subset=[t["chart_labels"]["values"]], inplace=True)

            if df.empty:
                st.error(t["file_handling"]["error_no_numeric_data"])
                return

            data_array = df[t["chart_labels"]["values"]].to_numpy().reshape(-1, 1)

            chart = ImRControlChart(
                data=data_array,
                xlabel=t["chart_labels"]["observation"],
                ylabel_top=t["chart_labels"]["individual_values"],
                ylabel_bottom=t["chart_labels"]["moving_range"]
            )

            chart.limits = True
            chart.append_rules([
                Rule01(), Rule02(), Rule03(), Rule04(),
                Rule05(), Rule06(), Rule07(), Rule08()
            ])

            normally_distributed = chart.normally_distributed(
                data=chart.value_I, significance_level=0.05
            )
            st.write(f"{t['analysis_results']['normal_distribution_check']} **{normally_distributed}**")

            chart.plot()
            fig = plt.gcf()
            st.pyplot(fig)

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
    else:
        st.info(t["file_handling"]["no_file_uploaded"])
