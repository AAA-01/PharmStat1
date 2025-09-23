# utils/translations.py  (показываю только НОВЫЙ раздел)
statistical_analysis_translations = {
    "Polski": {
        # ... twoje istniejące sekcje ...
        "statistical_analysis": {
            "title": "Analiza statystyczna",

            "upload_label": "Prześlij plik Excel",
            "source_data": "Dane źródłowe",

            "sample_type_label": "Wybierz typ prób:",
            "sample_ind": "Niezależne (domyślnie)",
            "sample_dep": "Zależne (sparowane)",
            "alpha_label": "Wybierz poziom istotności (alpha):",

            "sec1": "1) Przegląd danych",
            "groups_count": "Liczba grup: {n}",
            "rows_count": "Wielkość próby (wiersze): {n}",
            "group_stats_title": "Tabela miar statystycznych dla grup",

            "viz": "Wizualizacja",
            "boxplot": "Boxplot",
            "kde": "Gęstości (KDE)",

            "sec2": "2) Testy normalności",
            "sw_title": "a. Test Shapiro–Wilka",
            "levene_title": "b. Test Levene’a (jednorodność wariancji)",
            "levene_na": "Test Levene’a nie ma zastosowania lub nie został obliczony dla tego zestawu.",
            "dist_homo": "Wariancje jednorodne",
            "dist_hetero": "Wariancje niejednorodne",

            "group_verdict_normal": "Grupa {i} ({name}): normalna",
            "group_verdict_non_normal": "Grupa {i} ({name}): nienormalna",
            "p_line": "(p = {p:.4f} {sign} α={alpha})",
            "sign_gt": ">",
            "sign_le": "≤",

            "sec3": "3) Wybrana metoda statystyczna i wniosek",
            "used_test": "**Zastosowany test:** {test}",
            "alpha_used": "**Poziom istotności:** α = {alpha}",
            "stat_value": "**Statystyka testowa:** {stat:.4f}",
            "p_value": "**p-value:** {p:.4f}",
            "short_conclusion": "**Krótki wniosek o różnicach statystycznych:**",
            "sig_yes": "Stwierdzono istotne statystycznie różnice",
            "sig_no": "Nie stwierdzono istotnych statystycznie różnic",

            "help_norm_title": "Pomoc w interpretacji wyników",
            "help_norm_text": (
                "- **Shapiro–Wilk**: p > α → rozkład zbliżony do normalnego; p ≤ α → odchylenie od normalności.\n"
                "- **Levene**: p > α → wariancje jednorodne; p ≤ α → wariancje niejednorodne.\n"
                "- Wybór testu parametrycznego/nieparametrycznego i uwzględnienie jednorodności wariancji zależą od tych testów."
            ),

            "help_method_title": "Pomoc w interpretacji wybranej metody",
            "help_method_text": (
                "- **Jeśli p-value < α** → różnice **istotne statystycznie** (odrzucamy H₀).\n"
                "- **Jeśli p-value ≥ α** → **brak** istotnych statystycznie różnic (brak podstaw do odrzucenia H₀).\n"
                "- **Znaczenie testów:** test t (parametryczny), Manna–Whitneya/Wilcoxona (nieparametryczne), ANOVA, Kruskal–Wallis."
            ),
        },
    },

    "English": {
        # ... your existing sections ...
        "statistical_analysis": {
            "title": "Statistical analysis",

            "upload_label": "Upload an Excel file",
            "source_data": "Source data",

            "sample_type_label": "Select sample type:",
            "sample_ind": "Independent (default)",
            "sample_dep": "Dependent (paired)",
            "alpha_label": "Select significance level (alpha):",

            "sec1": "1) Data overview",
            "groups_count": "Number of groups: {n}",
            "rows_count": "Sample size (rows): {n}",
            "group_stats_title": "Table of statistical metrics by groups",

            "viz": "Visualization",
            "boxplot": "Boxplot",
            "kde": "Densities (KDE)",

            "sec2": "2) Normality check",
            "sw_title": "a. Shapiro–Wilk test",
            "levene_title": "b. Levene's test (variance homogeneity)",
            "levene_na": "Levene's test is not applicable or wasn't computed for this dataset.",
            "dist_homo": "Variances are homogeneous",
            "dist_hetero": "Variances are heterogeneous",

            "group_verdict_normal": "Group {i} ({name}): normal",
            "group_verdict_non_normal": "Group {i} ({name}): non-normal",
            "p_line": "(p = {p:.4f} {sign} α={alpha})",
            "sign_gt": ">",
            "sign_le": "≤",

            "sec3": "3) Chosen statistical method and conclusion",
            "used_test": "**Test used:** {test}",
            "alpha_used": "**Significance level:** α = {alpha}",
            "stat_value": "**Test statistic:** {stat:.4f}",
            "p_value": "**p-value:** {p:.4f}",
            "short_conclusion": "**Brief conclusion on statistical differences:**",
            "sig_yes": "Statistically significant differences detected",
            "sig_no": "No statistically significant differences found",

            "help_norm_title": "Help for interpreting results",
            "help_norm_text": (
                "- **Shapiro–Wilk**: p > α → distribution close to normal; p ≤ α → deviation from normality.\n"
                "- **Levene**: p > α → variances are homogeneous; p ≤ α → variances are heterogeneous.\n"
                "- Choosing parametric/nonparametric tests and accounting for variance homogeneity depend on these checks."
            ),

            "help_method_title": "Help for interpreting the chosen method",
            "help_method_text": (
                "- **If p-value < α** → differences are **statistically significant** (reject H₀).\n"
                "- **If p-value ≥ α** → **no** statistically significant differences (fail to reject H₀).\n"
                "- **What the tests mean:** t-test (parametric), Mann–Whitney/Wilcoxon (nonparametric), ANOVA, Kruskal–Wallis."
            ),
        },
    },

    "Русский": {
        # ... твои существующие секции ...
        "statistical_analysis": {
            "title": "Статистический анализ",

            "upload_label": "Загрузите Excel-файл",
            "source_data": "Исходные данные",

            "sample_type_label": "Выберите тип выборок:",
            "sample_ind": "Независимые (по умолчанию)",
            "sample_dep": "Зависимые (парные)",
            "alpha_label": "Выберите уровень значимости (alpha):",

            "sec1": "1) Обзор данных",
            "groups_count": "Количество групп: {n}",
            "rows_count": "Размер выборок (строк): {n}",
            "group_stats_title": "Таблица статистических показателей по группам",

            "viz": "Визуализация",
            "boxplot": "Boxplot",
            "kde": "Плотности (KDE)",

            "sec2": "2) Проверка на нормальность",
            "sw_title": "a. Тест Шапиро–Уилка",
            "levene_title": "b. Тест Левена (однородность дисперсий)",
            "levene_na": "Тест Левена не применим или не рассчитан для данного набора.",
            "dist_homo": "Дисперсии однородны",
            "dist_hetero": "Дисперсии неоднородны",

            "group_verdict_normal": "Группа {i} ({name}): нормальная",
            "group_verdict_non_normal": "Группа {i} ({name}): не-нормальная",
            "p_line": "(p = {p:.4f} {sign} α={alpha})",
            "sign_gt": ">",
            "sign_le": "≤",

            "sec3": "3) Выбранный статистический метод и итог",
            "used_test": "**Использованный тест:** {test}",
            "alpha_used": "**Уровень значимости:** α = {alpha}",
            "stat_value": "**Значение статистики:** {stat:.4f}",
            "p_value": "**p-value:** {p:.4f}",
            "short_conclusion": "**Краткий вывод о статистических различиях:**",
            "sig_yes": "Обнаружены статистически значимые различия",
            "sig_no": "Статистически значимых различий не выявлено",

            "help_norm_title": "Помощь в интерпретации результатов",
            "help_norm_text": (
                "- **Шапиро–Уилка**: p > α → распределение близко к нормальному; p ≤ α → отклонение от нормальности.\n"
                "- **Левен**: p > α → дисперсии однородны; p ≤ α → дисперсии неоднородны.\n"
                "- Выбор параметрического/непараметрического теста и учёт однородности дисперсий зависят от этих проверок."
            ),

            "help_method_title": "Помощь в интерпретации выбранного метода",
            "help_method_text": (
                "- **Если p-value < α** → различия **статистически значимы** (H₀ отвергается).\n"
                "- **Если p-value ≥ α** → статистически значимых различий **не выявлено** (оснований отвергать H₀ нет).\n"
                "- **Что означает тест:** t-тест (параметрический), Манна–Уитни/Уилкоксона (непараметрический), ANOVA, Краскела–Уоллиса."
            ),
        },
    },
}
