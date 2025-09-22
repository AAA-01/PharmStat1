from STATANALYZE.analyzer import analyze_groups
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

__all__ = ["show"]

# Добавляем путь к корневой директории проекта в sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def show(language=None):
    st.title("Инструмент статистического анализа")

    uploaded_file = st.file_uploader("Загрузите Excel-файл", type=["xlsx", "xls"])

    if not uploaded_file:
        return

    df = pd.read_excel(uploaded_file)

    # Краткая сводка данных
    st.write("Обзор данных")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"Количество групп: {len(df.columns)}")
        st.write(f"Размер выборок: {len(df)}")

    # 🔹 Выбор типа выборок
    sample_type = st.selectbox(
        "Выберите тип выборок:",
        ["Независимые (по умолчанию)", "Зависимые (парные)"],
    )
    paired = sample_type == "Зависимые (парные)"

    # 🔹 Выбор уровня значимости
    alpha = st.selectbox(
        "Выберите уровень значимости (alpha):",
        [0.01, 0.025, 0.05, 0.1],
        index=2,  # по умолчанию 0.05
    )

    # 🔹 Подсказки по выбору alpha
    st.markdown("**Рекомендации по выбору уровня значимости:**")
    if alpha == 0.05:
        st.info(
            "🔹 Стандарт в большинстве наук. Общепринятое значение.\n"
            "См.: [ICH E9 Statistical Principles](https://www.ich.org/page/efficacy-guidelines)"
        )
    elif alpha == 0.025:
        st.info(
            "🔹 Часто используется в биоэквивалентности (двусторонние тесты, 90% ДИ).\n"
            "См.: [EMA Bioequivalence Guideline](https://www.ema.europa.eu/en/documents/scientific-guideline/guideline-investigation-bioequivalence_en.pdf)"
        )
    elif alpha == 0.01:
        st.warning(
            "🔹 Более строгий порог, типичный для фарм-контроля качества и валидации процессов.\n"
            "См.: [FDA Process Validation Guidance 2011](https://www.fda.gov/media/71021/download)"
        )
    elif alpha == 0.1:
        st.info(
            "🔹 Используется в исследовательских целях. В фарме почти не применяется."
        )

    # Предварительный просмотр
    st.write("Предварительный просмотр")
    st.dataframe(df.head())

    # Подготовка групп
    groups = [df[col].dropna().tolist() for col in df.columns]

    try:
        result = analyze_groups(groups, paired=paired, alpha=alpha)

        st.write("Результаты анализа")

        # Основные результаты
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Использован тест:** {result['test_used']}")
            st.info(f"**Уровень значимости:** α = {result['alpha']}")
        with col2:
            st.info(f"**Значение статистики:** {result['statistic']:.4f}")
            st.info(f"**p-value:** {result['p_value']:.4f}")

        # Проверка нормальности
        st.write("Проверка нормальности распределения")
        st.write("Тест Шапиро-Уилка для каждой группы:")

        cols = st.columns(4)
        normal_groups, non_normal_groups = [], []

        for i, (p_value, _) in enumerate(zip(result["shapiro_p"], df.columns)):
            with cols[i % 4]:
                if p_value > result["alpha"]:
                    normal_groups.append(str(i + 1))
                    st.success(f"Группа {i+1}: ✓")
                else:
                    non_normal_groups.append(str(i + 1))
                    st.error(f"Группа {i+1}: ✗")
                st.caption(f"p = {p_value:.4f}")

        # Итог проверки нормальности
        st.write("Итог проверки нормальности:")
        st.info(
            f"**Нормальные распределения групп** (p > 0.05): {', '.join(normal_groups)}\n\n"
            f"**Ненормальные распределения групп** (p < 0.05): {', '.join(non_normal_groups)}\n\n"
            f"Для {len(normal_groups)} групп распределение близко к нормальному, "
            f"но для {len(non_normal_groups)} групп оно явно отличается от нормального."
        )

        with st.expander("Как интерпретировать результаты?"):
            st.write(
                "- **p-value > 0.05**: распределение нормальное ✓\n"
                "- **p-value ≤ 0.05**: распределение отличается от нормального ✗"
            )

        # Тест Левена
        if result["levene_p"] is not None:
            st.write("Проверка однородности дисперсий")
            if result["levene_p"] > result["alpha"]:
                st.success(f"Дисперсии однородны (тест Левена, p = {result['levene_p']:.4f})")
            else:
                st.warning(f"Дисперсии неоднородны (тест Левена, p = {result['levene_p']:.4f})")

        # Итоговый вывод
        if result["p_value"] < alpha:
            st.success("Обнаружены статистически значимые различия (p < alpha).")
        else:
            st.info("Статистически значимых различий не выявлено (p ≥ alpha).")

        # Полная таблица статистических показателей
        all_data = [
            {
                "Группа": f"{i}: {df.columns[i-1]}",
                "n": summary["n"],
                "Среднее": summary["mean"],
                "Медиана": summary["median"],
                "Стандартное отклонение": summary["std"],
                "Межквартильный размах (IQR)": summary["iqr"],
                "Дисперсия": summary["var"],
            }
            for i, summary in enumerate(result["group_summary"], start=1)
        ]
        full_df = pd.DataFrame(all_data)
        st.subheader("Полная таблица статистических показателей")
        st.dataframe(full_df, use_container_width=True)

        # Boxplot
        st.subheader("Boxplot")
        fig, ax = plt.subplots()
        df.boxplot(ax=ax)
        st.pyplot(fig)

        # Density plot
        st.subheader("Плотность распределений (KDE)")
        fig, ax = plt.subplots()
        for col in df.columns:
            sns.kdeplot(df[col].dropna(), label=col, fill=True, ax=ax)
        ax.legend()
        st.pyplot(fig)

    except ValueError as e:
        st.error(str(e))
