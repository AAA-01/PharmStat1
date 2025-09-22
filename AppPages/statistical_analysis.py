from STATANALYZE.analyzer import analyze_groups
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

__all__ = ["show"]

# Широкий макет для удобства и печати
st.set_page_config(layout="wide")

# Глобальные стили (аккуратные для печати)
_PRINT_CSS = """
<style>
/* Общая читаемость */
html, body, [class^="css"]  { line-height: 1.35; }

/* Подзаголовки и разделители */
h2, h3 { margin-top: 0.4rem; margin-bottom: 0.6rem; }

/* Карточки сообщений (success/info/warn) — чуть компактнее */
.stAlert { padding: 0.6rem 0.8rem; }

/* Таблицы компактнее и без горизонтальной прокрутки при печати */
@media print {
  header, footer, .stFileUploader, .stToolbar, .st-emotion-cache-6qob1r, .st-emotion-cache-1avcm0n { display: none !important; }
  .block-container { padding-top: 0 !important; }
  .stDataFrame { overflow: visible !important; }
  .stPlotlyChart, .stPyplot, .stAltairChart { page-break-inside: avoid; }
  h1, h2, h3 { page-break-after: avoid; }
  .page-break { page-break-before: always; }
}
</style>
"""
st.markdown(_PRINT_CSS, unsafe_allow_html=True)

# Добавляем путь к корню проекта (если модуль запускается как часть пакета)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def show(language=None):
    st.title("Инструмент статистического анализа")

    uploaded_file = st.file_uploader("Загрузите Excel-файл", type=["xlsx", "xls"])
    if not uploaded_file:
        return

    df = pd.read_excel(uploaded_file)

    # ===== Исходные данные (вся таблица без скролла) =====
    st.subheader("Исходные данные")
    # Подбираем высоту под все строки (примерная высота строки ~28 px + заголовок ~42 px)
    row_h = 28
    header_h = 42
    df_height = header_h + max(1, len(df)) * row_h
    st.dataframe(df, use_container_width=True, height=df_height)

    st.markdown("---")

    # Подготовка групп для анализа
    groups = [df[col].dropna().tolist() for col in df.columns]

    # Тип выборок
    sample_type = st.selectbox(
        "Выберите тип выборок:",
        ["Независимые (по умолчанию)", "Зависимые (парные)"],
    )
    paired = (sample_type == "Зависимые (парные)")

    # Уровень значимости
    alpha = st.selectbox(
        "Выберите уровень значимости (alpha):",
        [0.01, 0.025, 0.05, 0.1],
        index=2,  # по умолчанию 0.05
    )

    try:
        result = analyze_groups(groups, paired=paired, alpha=alpha)

        # =========================
        # 1) Обзор данных
        # =========================
        st.subheader("1) Обзор данных")

        c1, c2 = st.columns(2)
        with c1:
            st.write(f"Количество групп: {len(df.columns)}")
        with c2:
            st.write(f"Размер выборок (строк): {len(df)}")

        # Таблица показателей (входит в Обзор данных)
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
        st.dataframe(full_df, use_container_width=True)

        # ===== Визуализация (всегда, в одну строку 2 графика) =====
        st.subheader("Визуализация")
        vcol1, vcol2 = st.columns(2)

        with vcol1:
            st.markdown("**Boxplot**")
            fig1, ax1 = plt.subplots()
            df.boxplot(ax=ax1)
            ax1.set_xlabel("")  # чище при печати
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

        st.markdown("---")

        # =========================
        # 2) Проверка на нормальность
        # =========================
        st.subheader("2) Проверка на нормальность")

        # 2a. Шапиро–Уилка
        st.markdown("**a. Тест Шапиро–Уилка**")
        cols = st.columns(4)

        for i, (p_value, col_name) in enumerate(zip(result["shapiro_p"], df.columns), start=1):
            # Первая строка — вердикт; вторая строка — p и сравнение (новая строка для читаемости)
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

        st.markdown(
                "Помощь в интерпретации результатов"
                "- **Шапиро–Уилка**: p > α → распределение близко к нормальному; p ≤ α → отклонение от нормальности.\n"
                "- **Левен**: p > α → дисперсии однородны; p ≤ α → дисперсии неоднородны.\n"
                "- Выбор параметрического/непараметрического теста и учёт однородности дисперсий зависят от этих проверок."
            )
        # =========================
        # 3) Выбранный статистический метод и итог
        # =========================
        st.subheader("3) Выбранный статистический метод и итог")

        c1, c2 = st.columns(2)
        with c1:
            st.info(f"**Использованный тест:** {result['test_used']}  \n**Уровень значимости:** α = {result['alpha']}")
        with c2:
            st.info(f"**Значение статистики:** {result['statistic']:.4f}  \n**p-value:** {result['p_value']:.4f}")

        # Краткий вывод (перенос p для печати)
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

       

    except ValueError as e:
        st.error(str(e))
