# utils/i18n/general/en.py
TRANSLATIONS = {
     "control_charts": {
                "control_charts": "ImR Control Charts",
                "control_charts_desc": "Monitoring process stability using ImR control charts. Control charts allow tracking of changes in production or research processes, detecting any deviations from the norm. They are an essential tool in quality management and continuous process improvement.",
                "title": "ImR Control Charts",
                "instructions": {
                    "header": "Instructions",
                    "upload_file": "Upload an Excel file containing measurement data.",
                    "data_format": "The file should contain two columns: sample dates or IDs and numerical data.",
                    "extra_columns": "If the file contains more than 2 columns, additional columns will be ignored.",
                    "chart_info": "ImR charts will be generated, including the Individual Values (I) chart and the Moving Range (MR) chart."
                },
                "file_handling": {
                    "choose_file": "Choose an Excel file (xlsx or xls):",
                    "show_data_preview": "Show data preview",
                    "data_preview": "Data preview (first 10 rows):",
                    "error_processing_file": "An error occurred while processing the file",
                    "no_file_uploaded": "No file selected - please upload an Excel file above.",
                    "error_two_columns": "The file must contain at least 2 columns (Time/ID, Value).",
                    "warning_extra_columns": "The file contains extra columns:",
                    "select_result_column": "Select the result column for analysis:",
                    "select_result_column_help": "Choose the column containing the data you want to analyze in the control chart.",
                    "using_first_two": "Only the first two columns will be used."
                },
                "chart_labels": {
                    "time_series": "Time/ID",
                    "values": "Value",
                    "individual_values": "I (Individual Values)",
                    "moving_range": "MR (Moving Range)",
                    "observation": "Observation"
                },
                "analysis_results": {
                    "normal_distribution_check": "Is the distribution of I values normal (α=0.05 test)?",
                    "process_stable": "Is the process stable according to the rules?",
                    "show_I_chart": "Show I Chart Data (Individual Values)",
                    "show_MR_chart": "Show MR Chart Data (Moving Range)",
                    "I_chart_data": "I Chart Data (Individual Values)",
                    "MR_chart_data": "MR Chart Data (Moving Range)"
                }
            },
           
           
}
