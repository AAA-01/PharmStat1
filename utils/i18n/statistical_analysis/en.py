# utils/i18n/general/en.py
TRANSLATIONS = {
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
         
           
}
