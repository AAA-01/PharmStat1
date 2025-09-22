from STATANALYZE.analyzer import analyze_groups
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

__all__ = ["show"]

# Добавляем путь к корню проекта (если модуль запускается как часть пакета)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def show(language=None):
    st.title("Инструмент статистического анализа")

    uploaded_file = st.file_uploader("Загрузите Excel-файл", type=["xlsx", "xls"])
    if not uploaded_file:
        return

    df = pd.read_excel(uploaded_file)

    # Краткая сводка набора
    st.write("Обзор данных")
    c1, c2 = st.columns(2)
    with c1:
        st.write(f"Количество групп: {len(df.columns)}")
    with c2:
        st.write(f"Размер выборок (строк): {len(df)}")

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

    # Предпросмотр
    st.write("Предварительный просмотр")
    st.dataframe(df.head())

    # Подготовка групп
    groups = [df[col].dropna().tolist() for col in df.columns]

    try:
        result = analyze_groups(groups, paired=paired, alpha=alpha)

        # =========================
        # 1) Таблица показателей
        # =========================
        st.subheader("1) Таблица статистических показателей по группам")

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

        # Кнопка для выгрузки CSV
        csv = full_df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("Скачать таблицу показателей (CSV)", data=csv, file_name="group_stats.csv", mime="text/csv")

        # Доп. графики (опционально, но полезно для визуализации)
        with st.expander("Визуализация распределений"):
            st.markdown("**Boxplot**")
            fig1, ax1 = plt.subplots()
            df.boxplot(ax=ax1)
            st.pyplot(fig1)

            st.markdown("**Плотности (KDE)**")
            fig2, ax2 = plt.subplots()
            for col in df.columns:
                sns.kdeplot(df[col].dropna(), label=col, fill=True, ax=ax2)
            ax2.legend()
            st.pyplot(fig2)

        # =========================
        # 2) Проверка на нормальность
        # =========================
        st.subheader("2) Проверка на нормальность")

        # 2a. Шапиро–Уилка
        st.markdown("**a. Тест Шапиро–Уилка**")
        cols = st.columns(4)
        normal_groups, non_normal_groups = [], []

        for i, (p_value, col_name) in enumerate(zip(result["shapiro_p"], df.columns), start=1):
            with cols[(i-1) % 4]:
                if p_value > alpha:
                    normal_groups.append(str(i))
                    st.success(f"Группа {i} ({col_name}): нормальная (p = {p_value:.4f} > α={alpha})")
                else:
                    non_normal_groups.append(str(i))
                    st.error(f"Группа {i} ({col_name}): не-нормальная (p = {p_value:.4f} ≤ α={alpha})")

        if len(result.get("shapiro_p", [])) == 0:
            st.warning("Шапиро–Уилка не рассчитан (нет данных?).")

        # 2b. Левен
        levene_p = result.get("levene_p", None)
        st.markdown("**b. Тест Левена (однородность дисперсий)**")
        if levene_p is None:
            st.info("Тест Левена не применим или не рассчитан для данного набора.")
        else:
            if levene_p > alpha:
                st.success(f"Дисперсии однородны (p = {levene_p:.4f} > α={alpha}).")
            else:
                st.warning(f"Дисперсии неоднородны (p = {levene_p:.4f} ≤ α={alpha}).")

        # =========================
        # 3) Выбранный статистический метод + вывод
        # =========================
        st.subheader("3) Выбранный статистический метод и итог")

        c1, c2 = st.columns(2)
        with c1:
            st.info(f"**Использованный тест:** {result['test_used']}")
            st.info(f"**Уровень значимости:** α = {result['alpha']}")
        with c2:
            st.info(f"**Значение статистики:** {result['statistic']:.4f}")
            st.info(f"**p-value:** {result['p_value']:.4f}")

        # Краткий вывод
        st.markdown("**Краткий вывод о статистических различиях:**")
        if result["p_value"] < alpha:
            st.success(f"Обнаружены статистически значимые различия (p = {result['p_value']:.4f} < α={alpha}).")
        else:
            st.info(f"Статистически значимых различий не выявлено (p = {result['p_value']:.4f} ≥ α={alpha}).")

        # Пояснения
        with st.expander("Как интерпретировать результаты?"):
            st.write(
                "- **Шапиро–Уилка**: p > α → распределение близко к нормальному; p ≤ α → отклонение от нормальности.\n"
                "- **Левен**: p > α → дисперсии однородны; p ≤ α → дисперсии неоднородны.\n"
                "- Выбор параметрического/непараметрического теста и учёт однородности дисперсий зависят от этих проверок."
            )

    except ValueError as e:
        st.error(str(e))
