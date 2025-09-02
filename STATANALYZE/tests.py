import unittest
import numpy as np
from analyzer import analyze_groups


class TestAnalyzer(unittest.TestCase):

    def test_two_normal_groups(self):
        """Две нормальные выборки → t-тест или Манн–Уитни"""
        data1 = [2.1, 2.2, 2.3, 2.4, 2.5]
        data2 = [2.2, 2.3, 2.4, 2.5, 2.6]
        result = analyze_groups([data1, data2])
        self.assertIn(
            result["test_used"],
            ["Independent t-test", "Welch's t-test", "Mann–Whitney U test"]
        )
        self.assertGreaterEqual(result["p_value"], 0.0)
        self.assertLessEqual(result["p_value"], 1.0)

    def test_three_groups(self):
        """Три группы → ANOVA или Краскела–Уоллиса"""
        data1 = [2.1, 2.2, 2.3, 2.4, 2.5]
        data2 = [2.2, 2.3, 2.4, 2.5, 2.6]
        data3 = [3.1, 3.2, 3.3, 3.4, 3.5]
        result = analyze_groups([data1, data2, data3])
        self.assertIn(
            result["test_used"],
            ["One-way ANOVA", "Kruskal–Wallis test"]
        )
        self.assertGreaterEqual(result["p_value"], 0.0)
        self.assertLessEqual(result["p_value"], 1.0)

    def test_empty_group(self):
        """Пустая группа → ValueError"""
        with self.assertRaises(ValueError):
            analyze_groups([[], [1, 2, 3]])

    def test_too_few_points(self):
        """Слишком мало точек → ValueError"""
        with self.assertRaises(ValueError):
            analyze_groups([[1], [2, 3, 4]])

    def test_non_numeric_values(self):
        """Смешанные данные (NaN, строки) → очистка и работа"""
        data1 = [2.1, "bad", 2.3, None, np.nan, 2.4]
        data2 = [2.2, 2.3, 2.5, 2.6]
        result = analyze_groups([data1, data2])
        self.assertIn(
            result["test_used"],
            ["Independent t-test", "Welch's t-test", "Mann–Whitney U test"]
        )
        self.assertGreaterEqual(result["p_value"], 0.0)
        self.assertLessEqual(result["p_value"], 1.0)

    def test_all_nan(self):
        """Если вся группа состоит из NaN → ValueError"""
        with self.assertRaises(ValueError):
            analyze_groups([[np.nan, None], [1, 2, 3]])

    def test_paired_data(self):
        """Парные данные → Paired t-test или Wilcoxon"""
        data1 = [2.1, 2.2, 2.3, 2.4, 2.5]
        data2 = [2.0, 2.1, 2.2, 2.3, 2.4]
        result = analyze_groups([data1, data2], paired=True)
        self.assertIn(
            result["test_used"],
            ["Paired t-test", "Wilcoxon signed-rank test"]
        )
        self.assertGreaterEqual(result["p_value"], 0.0)
        self.assertLessEqual(result["p_value"], 1.0)

    def test_group_summary(self):
        """Проверка, что возвращается статистика по каждой группе"""
        data1 = [1, 2, 3, 4, 5]
        data2 = [2, 3, 4, 5, 6]
        result = analyze_groups([data1, data2])
        self.assertIn("group_summary", result)
        self.assertEqual(len(result["group_summary"]), 2)
        for summary in result["group_summary"]:
            self.assertIn("mean", summary)
            self.assertIn("std", summary)
            self.assertIn("median", summary)
            self.assertIn("iqr", summary)
            self.assertIn("var", summary)


if __name__ == "__main__":
    unittest.main()
