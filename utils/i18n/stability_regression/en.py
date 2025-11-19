# utils/i18n/stability_regression/en.py
TRANSLATIONS = {
    "stability_regression": {
        "menu_title": "Stability Regression",
        "stability_regression_label": "Stability Regression",
        "stability_regression_desc": (
            "Regression analysis for stability data. Stability regression enables predicting product shelf life "
            "based on long-term stability study results. This is crucial in the pharmaceutical and food industries, "
            "where product stability directly impacts safety and efficacy."
        ),
        "title": "Stability Data Analysis",
        "instructions": {
            "header": "Instructions",
            "upload_file": "Upload an Excel file containing stability data.",
            "display_series": "The selected series will be displayed on the chart along with regression lines.",
            "view_regression_results": "Below the chart, you will find a table with regression parameters for the selected series."
        },
        "file_handling": {
            "choose_file": "Choose an Excel file (xlsx or xls):",
            "show_data_preview": "Show data preview",
            "data_preview": "Data preview (first 12 rows):",
            "select_series": "Select series for analysis:",
            "error_processing_file": "An error occurred while processing the file",
            "no_file_uploaded": "No file selected - please upload an Excel file above."
        },
        "plot": {
            "data": "data",
            "regression": "regression",
            "spec_limit": "Specification Limit",
            "x_label": "Time (months)",
            "title": "Stability Analysis"
        },
        "regression_results": {
            "header": "Regression Analysis Results for Selected Series",
            "series": "Series",
            "slope": "Slope",
            "intercept": "Intercept",
            "r_value": "Correlation Coefficient (r)",
            "p_value": "p-value",
            "std_err": "Standard Error"
        }
    }
}
