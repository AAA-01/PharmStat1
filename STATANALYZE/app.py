import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from analyzer import analyze_groups

st.set_page_config(page_title="Статистический анализ", layout="wide")

st.title("📊 Инструмент статистического анализа")

uploaded_file = st.file_uploader("Загрузите Excel-файл", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("### 📄 Просмотр данных")
    st.dataframe(df.head())

    # 🔹 Выбор типа выборок
    sample_type = st.selectbox(
        "Выберите тип выборок:",
        ["Независимые (по умолчанию)", "Зависимые (парные)"]
    )
    paired = True if sample_type == "Зависимые (парные)" else False

    # 🔹 Выбор уровня значимости
    alpha = st.selectbox(
        "Выберите уровень значимости (alpha):",
        [0.01, 0.025, 0.05, 0.1],
        index=2  # по умолчанию 0.05
    )

    # 🔹 Подсказки по выбору alpha
    st.markdown("**Рекомендации по выбору уровня значимости:**")
    if alpha == 0.05:
        st.info("🔹 Стандарт в большинстве наук. Общепринятое значение.\n"
                "См.: [ICH E9 Statistical Principles](https://www.ich.org/page/efficacy-guidelines)")
    elif alpha == 0.025:
        st.info("🔹 Часто используется в биоэквивалентности (двусторонние тесты, 90% ДИ).\n"
                "См.: [EMA Bioequivalence Guideline](https://www.ema.europa.eu/en/documents/scientific-guideline/guideline-investigation-bioequivalence_en.pdf)")
    elif alpha == 0.01:
        st.warning("🔹 Более строгий порог, типичный для фарм-контроля качества и валидации процессов.\n"
                   "См.: [FDA Process Validation Guidance 2011](https://www.fda.gov/media/71021/download)")
    elif alpha == 0.1:
        st.info("🔹 Используется в исследовательских целях. В фарме почти не применяется.")

    # Подготовка групп
    groups = [df[col].dropna().tolist() for col in df.columns]

    try:
        result = analyze_groups(groups, paired=paired, alpha=alpha)

        st.write("## 🔍 Результаты")
        st.write(f"**Выбранный тест:** {result['test_used']}")
        st.write(f"**Статистика:** {result['statistic']:.4f}")
        st.write(f"**p-value:** {result['p_value']:.4f}")
        st.write(f"**Alpha (уровень значимости):** {result['alpha']}")
        st.write(f"**p-значения Шапиро–Уилка:** {result['shapiro_p']}")
        if result['levene_p'] is not None:
            st.write(f"**p-значение Левена:** {result['levene_p']:.4f}")

        # 🔎 Итоговый вывод
        if result['p_value'] < alpha:
            st.success("✅ Обнаружены статистически значимые различия (p < alpha).")
        else:
            st.info("ℹ️ Статистически значимых различий не выявлено (p ≥ alpha).")

        # 📑 Дополнительная статистика по группам
        st.write("### 📑 Статистика по группам (для ручной проверки)")
        for i, summary in enumerate(result['group_summary'], start=1):
            st.write(f"**Группа {i}:** "
                     f"n={summary['n']}, "
                     f"среднее={summary['mean']:.4f}, "
                     f"std={summary['std']:.4f}, "
                     f"медиана={summary['median']:.4f}, "
                     f"IQR={summary['iqr']:.4f}, "
                     f"дисперсия={summary['var']:.4f}")

        # === Визуализация ===
        st.write("## 📊 Визуализация данных")

        # 📦 Boxplot
        st.subheader("Boxplot (ящик с усами)")
        fig, ax = plt.subplots()
        df.boxplot(ax=ax)
        st.pyplot(fig)


        # 📊 Density plot
        st.subheader("Плотность распределений (KDE)")
        fig, ax = plt.subplots()
        for col in df.columns:
            sns.kdeplot(df[col].dropna(), label=col, fill=True, ax=ax)
        ax.legend()
        st.pyplot(fig)


    except ValueError as e:
        st.error(str(e))
