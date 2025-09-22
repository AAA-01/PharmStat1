from STATANALYZE.analyzer import analyze_groups
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

__all__ = ["show"]

# Широкий макет
st.set_page_config(layout="wide")

# Печать: альбомная ориентация + не рвать блоки + компактные таблицы при печати
_PRINT_CSS = """
<style>
/* экран — как было */
html, body, [class^="css"] { line-height: 1.35; }
h2, h3 { margin-top: 0.4rem; margin-bottom: 0.6rem; }
.stAlert { padding: 0.6rem 0.8rem; }

@media print {
  /* A4 ландшафт + поля */
  @page { size: A4 landscape; margin: 12mm; }

  /* скрыть хром UI */
  header, footer, .stFileUploader, .stToolbar { display:none !important; }
  .block-container { padding-top: 0 !important; }

  /* 1) Развернуть ВСЕ колонки в одну вертикаль */
  [data-testid="stHorizontalBlock"] { display:block !important; }
  [data-testid="column"] { width:100% !important; display:block !important; }

  /* 2) Не рвать основные контейнеры */
  .report-block { break-inside: avoid !important; page-break-inside: avoid !important; }

  /* 3) Не рвать таблицы и их строки */
  [data-testid="stTable"] table, 
  [data-testid="stDataFrame"] table { break-inside: avoid !important; page-break-inside: avoid !important; }
  [data-testid="stTable"] tr, 
  [data-testid="stDataFrame"] tr { break-inside: avoid !important; page-break-inside: avoid !important; }

  /* 4) Сделать таблицы компактнее, разрешить перенос в ячейках */
  .stDataFrame, .stTable { overflow: visible !important; }
  .stDataFrame table, .stTable table { font-size: 11px !important; }
  .stDataFrame th, .stDataFrame td, 
  .stTable th, .stTable td { white-space: normal !important; word-break: break-word !important; }

  /* 5) Графики и заголовки не рвать */
  .stPyplot, .stAltairChart, .stPlotlyChart { break-inside: avoid !important; page-break-inside: avoid !important; }
  h1, h2, h3 { page-break-after: avoid; }
}
</style>
"""
st.markdown(_PRINT_CSS, unsafe_allow_html=True)

# Путь к корню проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def show(language=None):
    st.title("Инструмент статистического анализа")

    uploaded_file = st.file_uploader("Загрузите Excel-файл", type=["xlsx", "xls"])
    if not uploaded_file:
        return

    df = pd.read_excel(uploaded_file)

    # ===== Исходные данные (вся таблица, без скролла) =====
    st.markdown('<div class="report-block">', unsafe_allow_html=True)
    st.subheader("Исходные данные")

    # показываем полностью, без скролла
    st.table(df.reset_index(drop=True).round(2))  

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")

    # Группы для анализа
    groups = [df[col].dropna().tolist() for col in df.columns]

    # Параметры анализа
    sample_type = st.selectbox(
        "Выберите тип выборок:",
        ["Независимые (по умолчанию)", "Зависимые (парные)"],
    )
    paired = (sample_type == "Зависимые (парные)")

    alpha = st.selectbox(
        "Выберите уровень значимости (alpha):",
        [0.01, 0.025, 0.05, 0.1],
        index=2,
    )

    try:
        result = analyze_groups(groups, paired=paired, alpha=alpha)

        # =========================
        # 1) Обзор данных
        # =========================
        st.markdown('<div class="report-block">', unsafe_allow_html=True)
        st.subheader("1) Обзор данных")

        c1, c2 = st.columns(2)
        with c1:
            st.write(f"Количество групп: {len(df.columns)}")
        with c2:
            st.write(f"Размер выборок (строк): {len(df)}")

        # Таблица показателей (центр, без индекса, 2 знака)
        st.markdown("**Таблица статистических показателей по группам**")
        rows = []
        for i, summary in enumerate(result["group_summary"], start=1):
            rows.append({
                "Группа": f"{i}: {df.columns[i-1]}",
                "n": summary.get("n"),
                "Среднее": summary.get("mean"),
                "Медиана": summary.get("median"),
                "Стандартное отклонение": summary.get("std"),
                "Межквартильный размах (IQR)": summary.get("iqr"),
                "Дисперсия": summary.get("var"),
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

        # ===== Визуализация =====
        st.markdown('<div class="report-block">', unsafe_allow_html=True)
        st.subheader("Визуализация")
        vcol1, vcol2 = st.columns(2)

        with vcol1:
            st.markdown("**Boxplot**")
            fig1, ax1 = plt.subplots()
            df.boxplot(ax=ax1)
            ax1.set_xlabel("")
            ax1.set_ylabel("")
            st.pyplot(fig1, use_container_width=True)

        with vcol2:
            st.markdown("**Плотности (KDE)**")
            fig2, ax2 = plt.subplots()
            for col in df.columns:
                sns.kdeplot(df[col].dropna(), label=col, fill=True, ax=ax2)
            ax2.legend(title="Группы", loc="best")
            ax2.set_xlabel("")
            ax2.set_ylabel("")
            st.pyplot(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")

        # =========================
        # 2) Проверка на нормальность
        # =========================
        st.markdown('<div class="report-block">', unsafe_allow_html=True)
        st.subheader("2) Проверка на нормальность")

        # 2a. Шапиро–Уилка
        st.markdown("**a. Тест Шапиро–Уилка**")
        cols = st.columns(4)

        for i, (p_value, col_name) in enumerate(zip(result["shapiro_p"], df.columns), start=1):
            verdict = "нормальная" if p_value > alpha else "не-нормальная"
            box_text = (
                f"Группа {i} ({col_name}): {verdict}  \n"
                f"(p = {p_value:.4f} {'>' if p_value > alpha else '≤'} α={alpha})"
            )
            with cols[(i-1) % 4]:
                if p_value > alpha:
                    st.success(box_text)
                else:
                    st.error(box_text)

        if len(result.get("shapiro_p", [])) == 0:
            st.warning("Тест Шапиро–Уилка не рассчитан (нет данных?).")

        # 2b. Левен
        st.markdown("**b. Тест Левена (однородность дисперсий)**")
        levene_p = result.get("levene_p", None)
        if levene_p is None:
            st.info("Тест Левена не применим или не рассчитан для данного набора.")
        else:
            lev_text_ok = f"Дисперсии однородны  \n(p = {levene_p:.4f} > α={alpha})"
            lev_text_bad = f"Дисперсии неоднородны  \n(p = {levene_p:.4f} ≤ α={alpha})"
            if levene_p > alpha:
                st.success(lev_text_ok)
            else:
                st.warning(lev_text_bad)

        with st.expander("Помощь в интерпретации результатов"):
            st.write(
                "- **Шапиро–Уилка**: p > α → распределение близко к нормальному; p ≤ α → отклонение от нормальности.\n"
                "- **Левен**: p > α → дисперсии однородны; p ≤ α → дисперсии неоднородны.\n"
                "- Выбор параметрического/непараметрического теста и учёт однородности дисперсий зависят от этих проверок."
            )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")

        # =========================
        # 3) Выбранный статистический метод и итог
        # =========================
        st.markdown('<div class="report-block">', unsafe_allow_html=True)
        st.subheader("3) Выбранный статистический метод и итог")

        c1, c2 = st.columns(2)
        with c1:
            st.info(f"**Использованный тест:** {result['test_used']}  \n**Уровень значимости:** α = {result['alpha']}")
        with c2:
            st.info(f"**Значение статистики:** {result['statistic']:.4f}  \n**p-value:** {result['p_value']:.4f}")

        st.markdown("**Краткий вывод о статистических различиях:**")
        if result["p_value"] < alpha:
            st.success(
                "Обнаружены статистически значимые различия  \n"
                f"(p = {result['p_value']:.4f} < α={alpha})."
            )
        else:
            st.info(
                "Статистически значимых различий не выявлено  \n"
                f"(p = {result['p_value']:.4f} ≥ α={alpha})."
            )

        with st.expander("Помощь в интерпретации выбранного метода"):
            st.write(
                "- **Если p-value < α** → различия **статистически значимы** (H₀ отвергается).\n"
                "- **Если p-value ≥ α** → статистически значимых различий **не выявлено** (оснований отвергать H₀ нет).\n"
                "- **Что означает тест:**\n"
                "  - **t-тест (параметрический)**: сравнивает средние при нормальности и равенстве дисперсий.\n"
                "  - **Манна–Уитни / Уилкоксона (непараметрический)**: сравнивает распределения/медианы при нарушении нормальности.\n"
                "  - **ANOVA**: проверяет различия между более чем двумя средними.\n"
                "  - **Краскела–Уоллиса**: непараметрический аналог ANOVA для ненормальных выборок.\n"
            )
        st.markdown("</div>", unsafe_allow_html=True)

    except ValueError as e:
        st.error(str(e))
