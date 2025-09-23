# AppPages/descriptive_statistics.py
import streamlit as st
import pandas as pd
from scipy.stats import shapiro, skew, kurtosis

from utils.data_processing import calculate_descriptive_stats
from utils.i18n import map_display_to_code, load_section  # новый i18n

__all__ = ["show"]

def show(language_display: str) -> None:
    """
    Страница описательной статистики.
    language_display: "Polski" | "English" | "Русский" (из селектора в app.py)
    """
    lang = map_display_to_code(language_display)                 # "pl" | "en" | "ru"
    t = load_section(lang, "descriptive_statistics")            # переводы секции

    st.header(t["title"])

    st.write(f"""
**{t['instructions']['header']}:**
- {t['instructions']['upload_file']}
- {t['instructions']['select_columns']}
- {t['instructions']['stats_summary']}
- {t['instructions']['normality_skew_kurtosis']}
""")

    uploaded_file = st.file_uploader(t["file_handling"]["choose_file"], type=["xlsx", "xls"])

    if uploaded_file is None:
        st.info(t["file_handling"]["no_file_uploaded"])
        return

    try:
        df = pd.read_excel(uploaded_file)

        # Предпросмотр
        show_data = st.checkbox(t["file_handling"]["show_data_preview"], value=True)
        if show_data:
            st.write(f"**{t['file_handling']['data_preview']}**")
            st.dataframe(df.head())

        # Предлагаем только числовые столбцы по умолчанию, но даём выбрать любые
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        all_cols = df.columns.tolist()

        selected_columns = st.multiselect(
            t["file_handling"]["select_columns"],
            options=all_cols,
            default=numeric_cols if numeric_cols else all_cols
        )

        if not selected_columns:
            st.warning(t.get("warnings_no_columns", "No columns selected."))
            return

        # Отфильтруем нечисловое при расчётах (сохранив порядок)
        numeric_selected = [c for c in selected_columns if pd.api.types.is_numeric_dtype(df[c])]
        if not numeric_selected:
            st.error(t.get("error_no_numeric_in_selection", "Selected columns contain no numeric data."))
            return

        # Параметры расчётов
        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            round_digits = st.number_input(t.get("formatting_round", "Rounding digits"), min_value=0, max_value=8, value=2)
        with c2:
            alpha = st.selectbox(
                t.get("alpha_label", "Significance level (alpha):"),
                options=[0.01, 0.025, 0.05, 0.1],
                index=2
            )

        # Базовая описательная статистика
        st.subheader(t["title"])
        base_stats = calculate_descriptive_stats(df[numeric_selected])
        # Приводим к единому формату индекса (строки-метрики)
        base_stats = base_stats.copy()

        # Дополнительные метрики: Shapiro p-value, Skewness, Kurtosis
        add_rows = {
            t["statistics"]["skewness"]: [],
            t["statistics"]["kurtosis"]: [],
            t["statistics"].get("shapiro_pvalue", "Shapiro p-value"): []
        }

        for col in numeric_selected:
            series = df[col].dropna()
            # безопасные вычисления — пустые/константные выборки пропускаем
            if len(series) < 3 or series.nunique(dropna=True) < 2:
                # NaN/прочерк для невозможных расчётов
                add_rows[t["statistics"]["skewness"]].append(float("nan"))
                add_rows[t["statistics"]["kurtosis"]].append(float("nan"))
                add_rows[t["statistics"].get("shapiro_pvalue", "Shapiro p-value")].append(float("nan"))
                continue

            try:
                p_shapiro = shapiro(series).pvalue
            except Exception:
                p_shapiro = float("nan")

            try:
                s = skew(series)
            except Exception:
                s = float("nan")

            try:
                k = kurtosis(series)
            except Exception:
                k = float("nan")

            add_rows[t["statistics"]["skewness"]].append(round(s, round_digits) if pd.notna(s) else float("nan"))
            add_rows[t["statistics"]["kurtosis"]].append(round(k, round_digits) if pd.notna(k) else float("nan"))
            add_rows[t["statistics"].get("shapiro_pvalue", "Shapiro p-value")].append(
                round(p_shapiro, 4) if pd.notna(p_shapiro) else float("nan")
            )

        add_df = pd.DataFrame(add_rows, index=numeric_selected).T

        # Объединяем базовую и дополнительные строки
        full_stats = pd.concat([base_stats, add_df], axis=0)

        # Итоговая таблица
        st.dataframe(full_stats)

        # Краткая интерпретация по нормальности (по p-value)
        st.markdown("---")
        st.subheader(t["normality_summary"]["title"])
        notes = []
        for col, p in zip(numeric_selected, add_rows[t["statistics"].get("shapiro_pvalue", "Shapiro p-value")]):
            if pd.isna(p):
                notes.append(f"- **{col}** — {t['normality_summary'].get('not_applicable', 'not applicable')}")
            elif p > alpha:
                notes.append(f"- **{col}** — {t['normality_summary']['normal']}  \n  ({t['normality_summary']['p_line'].format(p=p, alpha=alpha, sign=t['sign_gt'])})")
            else:
                notes.append(f"- **{col}** — {t['normality_summary']['non_normal']}  \n  ({t['normality_summary']['p_line'].format(p=p, alpha=alpha, sign=t['sign_le'])})")

        st.markdown("\n".join(notes))

    except Exception as e:
        st.error(f"{t['file_handling']['error_processing_file']}: {e}")
