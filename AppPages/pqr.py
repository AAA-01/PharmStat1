import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
from io import BytesIO

from SPC import ImRControlChart, Rule01, Rule02, Rule03, Rule04, Rule05, Rule06, Rule07, Rule08
from utils.translations import translations
from streamlit_quill import st_quill
from utils.pdf_export import build_pdf, PdfSection
from utils.signature_block import DEFAULT_ROLES
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode

# Column keys for signature editor (ASCII to avoid encoding issues)
SIG_ROLE = "role"
SIG_NAME = "full_name"
SIG_POSITION = "position"
SIG_SIGN = "sign"
PQR_HEADER = {
    "left_title": "\u0424\u043e\u0440\u043c\u0430",
    "left_subtitle": "\u041e\u0431\u0437\u043e\u0440 \u0432\u044b\u043f\u0443\u0441\u043a\u0430\u044e\u0449\u0435\u0433\u043e \u043a\u043e\u043d\u0442\u0440\u043e\u043b\u044f \u0433\u043e\u0442\u043e\u0432\u043e\u0439 \u043f\u0440\u043e\u0434\u0443\u043a\u0446\u0438\u0438",
    "right_lines": [
        "FORM008216/4",
        "\u042407-\u0421\u041e\u041f-\u0413-025",
        "SOP004546",
    ],
    "height": 80,
}
PQR_COVER_PAGE = {
    "center_lines": [
        "\u0410\u041e \u00ab\u0425\u0438\u043c\u0444\u0430\u0440\u043c\u00bb",
        "\u041e\u0431\u0437\u043e\u0440 \u043a\u0430\u0447\u0435\u0441\u0442\u0432\u0430 \u043f\u0440\u043e\u0434\u0443\u043a\u0442\u0430",
    ],
    "section_heading": "7. \u041e\u0411\u0417\u041e\u0420 \u0412\u042b\u041f\u0423\u0421\u041a\u0410\u042e\u0429\u0415\u0413\u041e \u041a\u041e\u041d\u0422\u0420\u041e\u041b\u042f \u0413\u041e\u0422\u041e\u0412\u041e\u0419 \u041f\u0420\u041e\u0414\u0423\u041a\u0426\u0418\u0418",
}


def _apply_imr_xticks(fig, series_labels):
    """Force x-axis tick step = 1 for both I and MR charts."""
    axes = fig.get_axes()
    if not axes:
        return

    top_n = len(series_labels)
    top_positions = list(range(1, top_n + 1))
    axes[0].set_xticks(top_positions)
    if series_labels:
        axes[0].set_xticklabels(series_labels, rotation=45, ha="right")

    if len(axes) > 1:
        bottom_n = max(top_n - 1, 0)
        if bottom_n:
            bottom_positions = list(range(1, bottom_n + 1))
            axes[1].set_xticks(bottom_positions)
            axes[1].set_xticklabels([str(i) for i in bottom_positions])


def show(language):
    t = translations[language]["pqr_module"]

    # =========================
    # Upload step
    # =========================
    if not st.session_state.get("pqr_file_bytes"):
        with st.expander("Загрузка файла", expanded=True):
            st.header(t["title"])

            st.write(f"""
            **{t["instructions"]["header"]}:**
            - {t["instructions"]["upload_file"]}
            - {t["instructions"]["select_series"]}
            - {t["instructions"]["input_spec_limits"]}
            - {t["instructions"]["view_charts"]}
            """)

            uploaded_file = st.file_uploader(
                t["file_handling"]["choose_file"],
                type=["xlsx", "xls"],
                key="pqr_uploader"
            )

            if uploaded_file is not None:
                st.session_state["pqr_file_bytes"] = uploaded_file.getvalue()
                st.session_state["pqr_file_name"] = uploaded_file.name
                st.rerun()

        st.info(t["file_handling"]["no_file_uploaded"])
        return

    # =========================
    # Main body
    # =========================
    try:
        file_like = BytesIO(st.session_state["pqr_file_bytes"])

        with st.expander("Отчёт PQR", expanded=True):
            df = pd.read_excel(file_like)

            if df.shape[1] < 2:
                st.error(t["file_handling"]["error_two_columns"])
                return

            df.rename(columns={df.columns[0]: t["chart_labels"]["time_series"]}, inplace=True)

            if df.shape[1] > 2:
                result_column = st.selectbox(
                    t["file_handling"]["select_result_column"],
                    df.columns[1:],
                    help=t["file_handling"]["select_result_column_help"]
                )
            else:
                result_column = df.columns[1]

            df[t["chart_labels"]["values"]] = df[result_column]

            st.header("Описание и вводные")
            content = st_quill(
                placeholder="Добавьте описание, вводные данные, комментарии...",
                html=True,
                key="editor",
            )

        if content:
            st.markdown(content, unsafe_allow_html=True)

        # Data preview
        show_data = st.checkbox(t["file_handling"]["show_data_preview"], value=True)
        if show_data:
            st.subheader(t["file_handling"]["data_preview"])
            subset = df[[t["chart_labels"]["time_series"], t["chart_labels"]["values"]]].reset_index(drop=True)
            st.dataframe(subset, use_container_width=True)

        # Prepare data
        df[t["chart_labels"]["time_series"]] = df[t["chart_labels"]["time_series"]].astype(str)
        df[t["chart_labels"]["values"]] = pd.to_numeric(df[t["chart_labels"]["values"]], errors='coerce')
        df.dropna(subset=[t["chart_labels"]["values"]], inplace=True)
        if df.empty:
            st.error(t["file_handling"]["error_no_numeric_data"])
            return

        data_array = df[t["chart_labels"]["values"]].to_numpy().reshape(-1, 1)
        series_ids = df[t["chart_labels"]["time_series"]].to_list()

        # ====== ImR chart ======
        st.subheader(t["subheaders"]["imr_chart"])
        chart = ImRControlChart(
            data=data_array,
            xlabel=t["chart_labels"]["observation"],
            ylabel_top=t["chart_labels"]["individual_values"],
            ylabel_bottom=t["chart_labels"]["moving_range"]
        )
        chart.limits = True
        chart.append_rules([Rule01(), Rule02(), Rule03(), Rule04(), Rule05(), Rule06(), Rule07(), Rule08()])
        chart.plot()
        fig_imr = plt.gcf()
        _apply_imr_xticks(fig_imr, series_ids)
        st.pyplot(fig_imr)

        # ====== Cpk + histogram ======
        st.subheader(t["subheaders"]["cpk_analysis"])
        usl = st.number_input(t["spec_limits"]["usl"], value=0.0)
        lsl = st.number_input(t["spec_limits"]["lsl"], value=0.0)

        fig_hist = None
        cpk_content = None
        if usl == lsl:
            st.warning(t["warnings"]["spec_limits_equal"])
        else:
            mean = float(np.mean(data_array))
            std_dev = float(np.std(data_array, ddof=1))
            cpk = min((usl - mean) / (3 * std_dev), (mean - lsl) / (3 * std_dev))

            fig_hist, ax = plt.subplots(figsize=(10, 6))
            ax.hist(data_array, bins=20, density=True, alpha=0.6, edgecolor='black')

            bins = np.linspace(min(data_array)[0], max(data_array)[0], 200)
            y = norm.pdf(bins, mean, std_dev)
            ax.plot(bins, y, '--', color='black')

            ax.axvline(usl, linestyle='dashed', linewidth=2, label=t["spec_limits"]["usl"])
            ax.axvline(lsl, linestyle='dashed', linewidth=2, label=t["spec_limits"]["lsl"])

            ax.set_xlabel(t["chart_labels"]["values"])
            ax.set_ylabel(t["chart_labels"]["frequency"])
            ax.set_title(t["chart_labels"]["histogram_with_spec_limits"])
            ax.legend()

            st.pyplot(fig_hist)

            st.write(f"{t['cpk_results']['mean']}: **{mean:.2f}**")
            st.write(f"{t['cpk_results']['std_dev']}: **{std_dev:.2f}**")
            st.write(f"{t['cpk_results']['cpk']}: **{cpk:.2f}**")
            cpk_content = [
                f"{t['cpk_results']['mean']}: {mean:.2f}",
                f"{t['cpk_results']['std_dev']}: {std_dev:.2f}",
                f"{t['cpk_results']['cpk']}: {cpk:.2f}",
                f"USL: {usl}",
                f"LSL: {lsl}",
            ]

        # ====== Comparison chart ======
        st.subheader(t["subheaders"]["spec_limits_comparison"])
        fig_comp, ax = plt.subplots(figsize=(12, 6))
        ax.plot(series_ids, data_array, marker='o', linestyle='-', label=t["chart_labels"]["values"])
        ax.axhline(usl, linestyle='dashed', linewidth=2, label=t["spec_limits"]["usl"])
        ax.axhline(lsl, linestyle='dashed', linewidth=2, label=t["spec_limits"]["lsl"])
        ax.set_xlabel(t["chart_labels"]["time_series"])
        ax.set_ylabel(t["chart_labels"]["values"])
        ax.set_title(t["chart_labels"]["control_chart_with_spec_limits"])
        plt.xticks(rotation=45)
        plt.grid(True)
        ax.legend()
        st.pyplot(fig_comp)

                        # ====== Signatures editor ======
        if "pqr_signatures" not in st.session_state:
            st.session_state["pqr_signatures"] = [
                {SIG_ROLE: role, SIG_NAME: "", SIG_POSITION: "", SIG_SIGN: ""}
                for role in DEFAULT_ROLES
            ]
        st.text_area(
            label="Выводы:",
            placeholder="Наберите выводы, замечания или ключевые наблюдения...",
            height=None,
            key="pqr_conclusions"
        )

        st.subheader("Подписи / согласование")
        sig_df = pd.DataFrame(st.session_state["pqr_signatures"])

        gb = GridOptionsBuilder.from_dataframe(sig_df)
        gb.configure_column(SIG_ROLE, header_name="Роль", editable=False, width=160)
        gb.configure_column(SIG_NAME, header_name="Ф.И.О.", editable=True, width=200)
        gb.configure_column(SIG_POSITION, header_name="Должность", editable=True, width=220)
        gb.configure_column(SIG_SIGN, header_name="Подпись, дата / ЭЦП", editable=True, width=220)
        gb.configure_grid_options(stopEditingWhenCellsLoseFocus=False)
        grid_options = gb.build()

        grid_resp = AgGrid(
            sig_df,
            gridOptions=grid_options,
            update_mode=GridUpdateMode.MODEL_CHANGED,
            data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
            height=260,
            fit_columns_on_grid_load=False,
            allow_unsafe_jscode=False,
            theme="streamlit",
            key="pqr_signatures_grid",
        )

        updated = grid_resp["data"]
        if isinstance(updated, pd.DataFrame):
            st.session_state["pqr_signatures"] = updated.to_dict("records")

        if st.button("Сохранить подписи"):
            st.success("Подписи сохранены", icon="✅")

# PDF prep
        subset_for_pdf = df[[t["chart_labels"]["time_series"], t["chart_labels"]["values"]]].reset_index(drop=True)
        cpk_desc_html = "<br/>".join([f"• {item}" for item in cpk_content]) if cpk_content else None

        figures_for_pdf = [(t["subheaders"]["imr_chart"], fig_imr)]
        if fig_hist is not None:
            figures_for_pdf.append((t["subheaders"]["cpk_analysis"], fig_hist, cpk_desc_html))
        figures_for_pdf.append((t["subheaders"]["spec_limits_comparison"], fig_comp))

        sections = [
            PdfSection(
                heading="",
                body_html=content,
                show_heading=False
            ),
            PdfSection(
                heading="Исходные данные",
                table_df=subset_for_pdf,
                show_heading=True
            ),
        ]

        sig_rows = st.session_state.get("pqr_signatures", [])
        cleaned_rows = []
        for row in sig_rows:
            role = str(row.get(SIG_ROLE, "") or "")
            name = str(row.get(SIG_NAME, "") or "")
            pos = str(row.get(SIG_POSITION, "") or "")
            sign = str(row.get(SIG_SIGN, "") or "")
            if not any([role.strip(), name.strip(), pos.strip(), sign.strip()]):
                continue
            cleaned_rows.append({SIG_ROLE: role, SIG_NAME: name, SIG_POSITION: pos, SIG_SIGN: sign})

        sig_roles = [r[SIG_ROLE] for r in cleaned_rows]
        sig_payload = [
            {
                "name": r[SIG_NAME],
                "position": r[SIG_POSITION],
                "signature": r[SIG_SIGN],
            }
            for r in cleaned_rows
        ]

        pdf_buf = build_pdf(
            title=st.session_state.get("pqr_file_name", "PQR Report"),
            sections=sections,
            figures=figures_for_pdf,
            conclusions=st.session_state.get("pqr_conclusions", ""),
            show_title=False,
            signatures=sig_payload,
            signature_roles=sig_roles,
            cover_page=PQR_COVER_PAGE,
            header=PQR_HEADER,
        )

        st.download_button(
            "Скачать PDF отчёт",
            data=pdf_buf,
            file_name="PQR_report.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"{t['file_handling']['error_processing_file']}: {e}")
