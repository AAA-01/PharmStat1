# AppPages/statistical_analysis.py
from STATANALYZE.analyzer import analyze_groups
from utils.statistical_analysis_translation import statistical_analysis_translations
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

__all__ = ["show"]

_PRINT_CSS = """
<style>
html, body, [class^="css"] { line-height: 1.35; }
h2, h3 { margin-top: 0.4rem; margin-bottom: 0.6rem; }
.stAlert { padding: 0.6rem 0.8rem; }
@media print {
  @page { size: A4 landscape; margin: 12mm; }
  header, footer, .stFileUploader, .stToolbar { display:none !important; }
  .block-container { padding-top: 0 !important; }
  [data-testid="stHorizontalBlock"] { display:block !important; }
  [data-testid="column"] { width:100% !important; display:block !important; }
  .report-block { break-inside: avoid !important; page-break-inside: avoid !important; }
  [data-testid="stTable"] table, [data-testid="stDataFrame"] table { break-inside: avoid !important; page-break-inside: avoid !important; }
  [data-testid="stTable"] tr,     [data-testid="stDataFrame"] tr     { break-inside: avoid !important; page-break-inside: avoid !important; }
  .stDataFrame, .stTable { overflow: visible !important; }
  .stDataFrame table, .stTable table { font-size: 11px !important; }
  .stPyplot, .stAltairChart, .stPlotlyChart { break-inside: avoid !important; page-break-inside: avoid !important; }
  h1, h2, h3 { page-break-after: avoid; }
}
</style>
"""
st.markdown(_PRINT_CSS, unsafe_allow_html=True)

def show(language: str):
    t = statistical_analysis_translations[language]["statistical_analysis"]

    st.title(t["title"])

    uploaded_file = st.file_uploader(t["upload_label"], type=["xlsx", "xls"])
    if not uploaded_file:
        return

    df = pd.read_excel(uploaded_file)

    # ===== Dane źródłowe / Source data / Исходные данные =====
    st.markdown('<div class="report-block">', unsafe_allow_html=True)
    st.subheader(t["source_data"])
    st.table(df.reset_index(drop=True).round(2))
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # Przygotowanie grup
    groups = [df[col].dropna().tolist() for col in df.columns]

    # Parametry
    sample_type = st.selectbox(
        t["sample_type_label"],
        [t["sample_ind"], t["sample_dep"]],
    )
    paired = (sample_type == t["sample_dep"])

    alpha = st.selectbox(
        t["alpha_label"],
        [0.01, 0.025, 0.05, 0.1],
        index=2,
    )

    try:
        result = analyze_groups(groups, paired=paired, alpha=alpha)

        # ===== 1) Przegląd danych / Data overview / Обзор данных =====
        st.markdown('<div class="report-block">', unsafe_allow_html=True)
        st.subheader(t["sec1"])

        c1, c2 = st.columns(2)
        with c1:
            st.write(t["groups_count"].format(n=len(df.columns)))
        with c2:
            st.write(t["rows_count"].format(n=len(df)))

        st.markdown("**" + t["group_stats_title"] + "**")
        rows = []
        for i, summary in enumerate(result["group_summary"], start=1):
            rows.append({
                statistical_analysis_translations[language]["statistical_analysis"]["group_col"] if "group_col" in statistical_analysis_translations[language]["statistical_analysis"] else "Group": f"{i}: {df.columns[i-1]}",
                statistical_analysis_translations[language]["statistical_analysis"]["n_col"]     if "n_col"     in statistical_analysis_translations[language]["statistical_analysis"] else "n": summary.get("n"),
                statistical_analysis_translations[language]["statistical_analysis"]["mean_col"]  if "mean_col"  in statistical_analysis_translations[language]["statistical_analysis"] else "Mean": summary.get("mean"),
                statistical_analysis_translations[language]["statistical_analysis"]["median_col"]if "median_col"in statistical_analysis_translations[language]["statistical_analysis"] else "Median": summary.get("median"),
                statistical_analysis_translations[language]["statistical_analysis"]["std_col"]   if "std_col"   in statistical_analysis_translations[language]["statistical_analysis"] else "Std. deviation": summary.get("std"),
                statistical_analysis_translations[language]["statistical_analysis"]["iqr_col"]   if "iqr_col"   in statistical_analysis_translations[language]["statistical_analysis"] else "IQR": summary.get("iqr"),
                statistical_analysis_translations[language]["statistical_analysis"]["var_col"]   if "var_col"   in statistical_analysis_translations[language]["statistical_analysis"] else "Variance": summary.get("var"),
            })
        full_df = pd.DataFrame(rows)
        styled_full_df = (
            full_df.style
            .hide(axis="index")
            .set_properties(**{"text-align": "center"})
            .set_table_styles([{"selector": "th", "props": [("text-align", "center")]}])
            .format(precision=2)
        )
        st.dataframe(styled_full_df, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # ===== Wizualizacja / Visualization / Визуализация =====
        st.markdown('<div class="report-block">', unsafe_allow_html=True)
        st.subheader(t["viz"])
        vcol1, vcol2 = st.columns(2)

        with vcol1:
            st.markdown("**" + t["boxplot"] + "**")
            fig1, ax1 = plt.subplots()
            df.boxplot(ax=ax1)
            ax1.set_xlabel(""); ax1.set_ylabel("")
            st.pyplot(fig1, use_container_width=True)

        with vcol2:
            st.markdown("**" + t["kde"] + "**")
            fig2, ax2 = plt.subplots()
            for col in df.columns:
                sns.kdeplot(df[col].dropna(), label=col, fill=True, ax=ax2)
            # Tytuł legendy / Legend title / Заголовок легенды
            legend_title = statistical_analysis_translations[language]["statistical_analysis"].get("group_col", "Group")
            ax2.legend(title=legend_title, loc="best")
            ax2.set_xlabel(""); ax2.set_ylabel("")
            st.pyplot(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")

        # ===== 2) Normalność / Normality / Нормальность =====
        t_sa = statistical_analysis_translations[language]["statistical_analysis"]
        st.markdown('<div class="report-block">', unsafe_allow_html=True)
        st.subheader(t_sa["sec2"])

        st.markdown("**" + t_sa["sw_title"] + "**")
        cols = st.columns(4)
        for i, (p_value, col_name) in enumerate(zip(result["shapiro_p"], df.columns), start=1):
            is_normal = p_value > alpha
            verdict = t_sa["group_verdict_normal"] if is_normal else t_sa["group_verdict_non_normal"]
            sign = t_sa["sign_gt"] if is_normal else t_sa["sign_le"]
            msg = verdict.format(i=i, name=col_name) + "  \n" + t_sa["p_line"].format(p=p_value, sign=sign, alpha=alpha)
            with cols[(i - 1) % 4]:
                st.success(msg) if is_normal else st.error(msg)

        if len(result.get("shapiro_p", [])) == 0:
            st.warning(t_sa["levene_na"])

        st.markdown("**" + t_sa["levene_title"] + "**")
        levene_p = result.get("levene_p", None)
        if levene_p is None:
            st.info(t_sa["levene_na"])
        else:
            is_homo = levene_p > alpha
            sign = t_sa["sign_gt"] if is_homo else t_sa["sign_le"]
            lev_text = (t_sa["dist_homo"] if is_homo else t_sa["dist_hetero"]) + "  \n" + t_sa["p_line"].format(p=levene_p, sign=sign, alpha=alpha)
            st.success(lev_text) if is_homo else st.warning(lev_text)

        with st.expander(t_sa["help_norm_title"]):
            st.write(t_sa["help_norm_text"])
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")

        # ===== 3) Metoda i wniosek / Method & conclusion / Метод и итог =====
        st.markdown('<div class="report-block">', unsafe_allow_html=True)
        st.subheader(t_sa["sec3"])

        c1, c2 = st.columns(2)
        with c1:
            st.info(t_sa["used_test"].format(test=result["test_used"]) + "  \n" + t_sa["alpha_used"].format(alpha=result["alpha"]))
        with c2:
            st.info(t_sa["stat_value"].format(stat=result["statistic"]) + "  \n" + t_sa["p_value"].format(p=result["p_value"]))

        st.markdown(t_sa["short_conclusion"])
        if result["p_value"] < alpha:
            st.success(t_sa["sig_yes"] + "  \n" + t_sa["p_line"].format(p=result["p_value"], sign=t_sa["sign_gt"], alpha=alpha))
        else:
            st.info(t_sa["sig_no"] + "  \n" + t_sa["p_line"].format(p=result["p_value"], sign=t_sa["sign_le"], alpha=alpha))

        with st.expander(t_sa["help_method_title"]):
            st.write(t_sa["help_method_text"])
        st.markdown("</div>", unsafe_allow_html=True)

    except ValueError as e:
        # Bezpiecznie: jeśli gdzieś brakuje klucza tłumaczeń — pokaż błąd oryginalnie.
        st.error(str(e))
