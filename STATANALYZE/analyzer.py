import numpy as np
from scipy.stats import (
    shapiro, levene, ttest_ind, mannwhitneyu,
    f_oneway, kruskal, ttest_rel, wilcoxon, friedmanchisquare
)


def clean_data(group):
    """Очистка данных: удаляем NaN, None и нечисловые значения"""
    cleaned = []
    for x in group:
        try:
            val = float(x)
            if not np.isnan(val):
                cleaned.append(val)
        except (TypeError, ValueError):
            continue
    return np.array(cleaned, dtype=np.float64)


def analyze_groups(groups, paired=False, alpha=0.05):
    """
    Анализ групп: выбор статистического теста в зависимости от нормальности,
    равенства дисперсий и зависимости выборок.
    """

    # Очистка данных
    groups = [clean_data(g) for g in groups if len(g) > 0]

    if len(groups) < 2:
        raise ValueError("Нужно минимум две группы данных для анализа")

    for g in groups:
        if len(g) < 2:
            raise ValueError("Слишком мало точек в одной из групп для статистического анализа")

    # Проверка нормальности (Шапиро–Уилк)
    shapiro_p = [shapiro(g)[1] if len(g) >= 3 else 0.0 for g in groups]
    normal = all(p > alpha for p in shapiro_p)

    # Проверка равенства дисперсий (только если нормальные данные и ≥2 группы)
    levene_p = None
    if normal and len(groups) > 1:
        levene_p = levene(*groups)[1]

    result = {
        "test_used": None,
        "statistic": None,
        "p_value": None,
        "shapiro_p": shapiro_p,
        "levene_p": levene_p,
        "alpha": alpha,
        "group_summary": []
    }

    # === Выбор теста ===
    if len(groups) == 2:
        g1, g2 = groups
        if paired:
            # Парные выборки
            if normal:
                stat, p = ttest_rel(g1, g2)
                test_name = "Paired t-test"
            else:
                stat, p = wilcoxon(g1, g2)
                test_name = "Wilcoxon signed-rank test"
        else:
            # Независимые выборки
            if normal:
                if levene_p is not None and levene_p > alpha:
                    stat, p = ttest_ind(g1, g2, equal_var=True)
                    test_name = "Independent t-test"
                else:
                    stat, p = ttest_ind(g1, g2, equal_var=False)
                    test_name = "Welch's t-test"
            else:
                stat, p = mannwhitneyu(g1, g2)
                test_name = "Mann–Whitney U test"

    else:
        # ≥ 3 группы
        if paired:
            if normal:
                stat, p = friedmanchisquare(*groups)
                test_name = "Friedman test (parametric)"
            else:
                stat, p = friedmanchisquare(*groups)
                test_name = "Friedman test (non-parametric)"
        else:
            if normal:
                stat, p = f_oneway(*groups)
                test_name = "One-way ANOVA"
            else:
                stat, p = kruskal(*groups)
                test_name = "Kruskal–Wallis test"

    # Записываем результаты
    result["test_used"] = test_name
    result["statistic"] = float(stat)
    result["p_value"] = float(p)

    # === Дополнительная статистика для каждой группы ===
    for g in groups:
        summary = {
            "n": len(g),
            "mean": float(np.mean(g)),
            "std": float(np.std(g, ddof=1)),
            "median": float(np.median(g)),
            "iqr": float(np.percentile(g, 75) - np.percentile(g, 25)),
            "var": float(np.var(g, ddof=1)),
        }
        result["group_summary"].append(summary)

    return result
