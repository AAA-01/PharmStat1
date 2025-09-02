import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.translations import translations

def show(language):
    t = translations[language]["temp_humidity_analysis"]

    st.header(t["title"])

    st.write(f"""
    **{t["instructions"]["header"]}:**
    - {t["instructions"]["upload_file"]}
    - {t["instructions"]["set_limits"]}
    - {t["instructions"]["view_results"]}
    """)

    temp_lower = st.slider(t["settings"]["temp_lower"], min_value=0, max_value=100, value=23)
    temp_upper = st.slider(t["settings"]["temp_upper"], min_value=0, max_value=100, value=27)

    hum_lower = st.slider(t["settings"]["hum_lower"], min_value=0, max_value=100, value=55)
    hum_upper = st.slider(t["settings"]["hum_upper"], min_value=0, max_value=100, value=65)

    uploaded_file = st.file_uploader(t["file_handling"]["choose_file"], type=["xlsx", "xls"])

    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file, header=None, skiprows=1)
            df.columns = ['time', 'temperature', 'humidity']

            df['time'] = pd.to_datetime(df['time'], errors='coerce')
            df.dropna(subset=['time'], inplace=True)

            st.subheader(t["file_handling"]["data_preview"])
            st.dataframe(df.head(10))

            st.subheader(t["statistics"]["temp_stats"])
            mean_temp = df['temperature'].mean()
            min_temp = df['temperature'].min()
            max_temp = df['temperature'].max()
            std_temp = df['temperature'].std()
            rsd_temp = (std_temp / mean_temp * 100) if mean_temp != 0 else None

            st.write(f"- **{t['statistics']['mean']} (\u00b0C)**: {mean_temp:.2f}")
            st.write(f"- **{t['statistics']['min']} (\u00b0C)**: {min_temp:.2f}")
            st.write(f"- **{t['statistics']['max']} (\u00b0C)**: {max_temp:.2f}")
            st.write(f"- **{t['statistics']['rsd']} (%)**: {rsd_temp:.2f}")

            st.subheader(t["statistics"]["hum_stats"])
            mean_hum = df['humidity'].mean()
            min_hum = df['humidity'].min()
            max_hum = df['humidity'].max()
            std_hum = df['humidity'].std()
            rsd_hum = (std_hum / mean_hum * 100) if mean_hum != 0 else None

            st.write(f"- **{t['statistics']['mean']} (%)**: {mean_hum:.2f}")
            st.write(f"- **{t['statistics']['min']} (%)**: {min_hum:.2f}")
            st.write(f"- **{t['statistics']['max']} (%)**: {max_hum:.2f}")
            st.write(f"- **{t['statistics']['rsd']} (%)**: {rsd_hum:.2f}")

            threshold_crossings = []
            for i in range(1, len(df)):
                prev_temp = df['temperature'].iloc[i-1]
                curr_temp = df['temperature'].iloc[i]
                prev_hum  = df['humidity'].iloc[i-1]
                curr_hum  = df['humidity'].iloc[i]

                if ((prev_temp < temp_lower and curr_temp >= temp_lower) or
                    (prev_temp >= temp_lower and curr_temp < temp_lower) or
                    (prev_temp < temp_upper and curr_temp >= temp_upper) or
                    (prev_temp > temp_upper and curr_temp <= temp_upper) or
                    (prev_hum < hum_lower and curr_hum >= hum_lower) or
                    (prev_hum >= hum_lower and curr_hum < hum_lower) or
                    (prev_hum < hum_upper and curr_hum >= hum_upper) or
                    (prev_hum > hum_upper and curr_hum <= hum_upper)):
                    threshold_crossings.append({
                        'time': df['time'].iloc[i],
                        'temperature': curr_temp,
                        'humidity': curr_hum
                    })

            st.subheader(t["thresholds"]["crossings"])
            if threshold_crossings:
                crossings_df = pd.DataFrame(threshold_crossings)
                st.dataframe(crossings_df)
            else:
                st.write(t["thresholds"]["no_crossings"])

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(df['time'], df['temperature'], label=t['plot']['temp'], color='red')
            ax.plot(df['time'], df['humidity'], label=t['plot']['hum'], color='blue')

            ax.axhline(y=temp_lower, color='red', linestyle='--', label=t['plot']['temp_lower_limit'])
            ax.axhline(y=temp_upper, color='red', linestyle='--', label=t['plot']['temp_upper_limit'])
            ax.axhline(y=hum_lower, color='blue', linestyle='--', label=t['plot']['hum_lower_limit'])
            ax.axhline(y=hum_upper, color='blue', linestyle='--', label=t['plot']['hum_upper_limit'])

            ax.set_xlabel(t['plot']['x_label'])
            ax.set_ylabel(t['plot']['y_label'])
            ax.set_title(t['plot']['title'])
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)

        except Exception as e:
            st.error(f"{t['file_handling']['error_processing_file']}: {e}")
    else:
        st.info(t["file_handling"]["no_file_uploaded"])
