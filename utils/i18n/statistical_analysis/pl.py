TRANSLATIONS = {
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
   
}