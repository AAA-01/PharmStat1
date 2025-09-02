import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
import io

# ---------------------------------------------------------
# Importy z biblioteki sixsigmaspc
# (zamiast SPC.*)
# ---------------------------------------------------------
#pip install sixsigmaspc
from SPC import Rule01, Rule02, Rule03, Rule04, Rule05, Rule06, Rule07, Rule08
from SPC import XbarRControlChart

# ---------------------------------------------------------
# Funkcje i limity dla temperatury i wilgotności
# ---------------------------------------------------------
temperature_limit = (23, 27)  # 23 - 27 °C
humidity_limit = (55, 65)     # 55% - 65%

def generate_report_streamlit(file_content):
    """
    Generuje raport z pliku Excel (pomiary temperatury i wilgotności),
    wyświetla wyniki w Streamlit.
    """
    try:
        df = pd.read_excel(io.BytesIO(file_content), header=None, skiprows=1)
        df.columns = ['time', 'temperature', 'humidity']

        df['time'] = pd.to_datetime(df['time'], format='%m/%d/%y %H:%M', errors='coerce')
        df = df.dropna(subset=['time'])

        threshold_crossings = []
        for i in range(1, len(df)):
            prev_temp = df['temperature'].iloc[i-1]
            curr_temp = df['temperature'].iloc[i]
            prev_hum  = df['humidity'].iloc[i-1]
            curr_hum  = df['humidity'].iloc[i]

            if ((prev_temp < 23 and curr_temp >= 23) or
                (prev_temp >= 23 and curr_temp < 23) or
                (prev_temp < 27 and curr_temp >= 27) or
                (prev_temp > 27 and curr_temp <= 27) or
                (prev_hum < 55 and curr_hum >= 55) or
                (prev_hum >= 55 and curr_hum < 55) or
                (prev_hum < 65 and curr_hum >= 65) or
                (prev_hum > 65 and curr_hum <= 65)):
                threshold_crossings.append({
                    'time': df['time'].iloc[i],
                    'temperature': curr_temp,
                    'humidity': curr_hum
                })

        crossings_df = pd.DataFrame(threshold_crossings)

        st.subheader("Przekroczenia progów temperatury / wilgotności")
        if not crossings_df.empty:
            st.dataframe(crossings_df)
        else:
            st.write("Brak przekroczeń granic.")

        st.write("---")
        st.subheader("Statystyki temperatury")
        avg_temp = df["temperature"].mean()
        min_temp = df["temperature"].min()
        max_temp = df["temperature"].max()
        rsd_temp = (df["temperature"].std() / avg_temp * 100) if avg_temp != 0 else None
        st.write(f"- **Średnia:** {avg_temp:.2f}")
        st.write(f"- **Minimum:** {min_temp:.2f}")
        st.write(f"- **Maksimum:** {max_temp:.2f}")
        st.write(f"- **RSD:** {rsd_temp:.2f}%")
        st.write(f"- **Liczba pomiarów:** {len(df['temperature'])}")

        st.subheader("Statystyki wilgotności")
        avg_hum = df["humidity"].mean()
        min_hum = df["humidity"].min()
        max_hum = df["humidity"].max()
        rsd_hum = (df["humidity"].std() / avg_hum * 100) if avg_hum != 0 else None
        st.write(f"- **Średnia:** {avg_hum:.2f}")
        st.write(f"- **Minimum:** {min_hum:.2f}")
        st.write(f"- **Maksimum:** {max_hum:.2f}")
        st.write(f"- **RSD:** {rsd_hum:.2f}%")
        st.write(f"- **Liczba pomiarów:** {len(df['humidity'])}")

        # Rysowanie wykresu
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(df['time'], df['temperature'], label='Temperature')
        ax.plot(df['time'], df['humidity'], label='Humidity')
        ax.axhline(y=temperature_limit[0], color='blue', linestyle='--', label='Temp Lower Limit')
        ax.axhline(y=temperature_limit[1], color='blue', linestyle='--', label='Temp Upper Limit')
        ax.axhline(y=humidity_limit[0], color='green', linestyle='--', label='Humidity Lower Limit')
        ax.axhline(y=humidity_limit[1], color='green', linestyle='--', label='Humidity Upper Limit')

        ax.set_xlabel('Datetime')
        ax.set_ylabel('Value')
        ax.set_title('Temperature and Humidity Monitoring')
        ax.grid(True)
        ax.legend()
        fig.tight_layout()

        st.pyplot(fig)

    except Exception as e:
        st.error(f"Wystąpił błąd podczas analizy pliku: {e}")


# -------------------- STRONY ISTNIEJĄCE -------------------- #
def show_intro():
    st.header("Wprowadzenie")
    st.write("""
    **Witaj w przykładowej aplikacji Streamlit!**  
    W bocznym menu możesz przełączać się między kilkoma podstronami:
    
    1. **Wprowadzenie**  
    2. **Wykres punktowy i liniowy**  
    3. **Regresja liniowa (SciPy)**  
    4. **Wczytanie pliku Excel**  
    5. **Analiza temperatury i wilgotności**  
    6. **Karta kontrolna Shewharta (X-bar / R)**  

    ---
    **Jak korzystać z aplikacji?**  
    - Wybierz interesującą Cię podstronę w bocznym panelu.
    - Interakcja odbywa się przez widżety (suwaki, przyciski, pola do wczytania pliku, itp.).
    - Wyniki (wykresy, tabele, statystyki) pojawiają się w głównym obszarze strony.
    """)

def show_scatter_line():
    st.header("Wykres punktowy i liniowy")
    num_rows = st.slider("Ile punktów losowych wygenerować?", 5, 300, 50)
    X = np.linspace(0, 10, num_rows)
    noise = np.random.randn(num_rows) * 3
    Y = 2.5 * X + noise
    df = pd.DataFrame({"X": X, "Y": Y})
    st.write("**Podgląd danych (pierwsze 5 wierszy):**")
    st.dataframe(df.head())
    
    chart_type = st.selectbox("Wybierz rodzaj wykresu:", ["Punktowy (scatter)", "Liniowy (line)"])
    
    if st.button("Rysuj wykres"):
        fig, ax = plt.subplots()
        if chart_type == "Punktowy (scatter)":
            ax.scatter(df["X"], df["Y"], color="blue", alpha=0.7)
            ax.set_title("Wykres punktowy")
        else:
            ax.plot(df["X"], df["Y"], color="red")
            ax.set_title("Wykres liniowy")

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        st.pyplot(fig)

def show_linreg_scipy():
    st.header("Regresja Liniowa (SciPy)")
    st.write("""
    W tej sekcji losujemy punkty (X, Y) i dopasowujemy do nich linię 
    z wykorzystaniem `scipy.stats.linregress`. 
    """)
    num_points = st.slider("Liczba punktów danych:", 10, 300, 50)
    X = np.linspace(0, 10, num_points)
    true_a = 3.0
    true_b = 2.0
    noise = np.random.randn(num_points) * 3
    Y = true_a * X + true_b + noise
    df_reg = pd.DataFrame({"X": X, "Y": Y})
    st.write("**Podgląd danych (pierwsze 5 wierszy):**")
    st.dataframe(df_reg.head())

    if st.button("Dopasuj regresję i narysuj wykres"):
        slope, intercept, r_value, p_value, std_err = linregress(X, Y)
        Y_pred = slope * X + intercept

        fig, ax = plt.subplots()
        ax.scatter(X, Y, label="Dane (punkty)", alpha=0.7)
        ax.plot(X, Y_pred, color="red", label="Linia regresji")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.legend()
        ax.set_title("Regresja Liniowa: Y = aX + b")
        st.pyplot(fig)

        st.write(f"**Nachylenie (slope)** = {slope:.3f}")
        st.write(f"**Wyraz wolny (intercept)** = {intercept:.3f}")
        st.write(f"**Współczynnik korelacji (r)** = {r_value:.3f}")
        st.write(f"**Wartość p (p-value)** = {p_value:.3e}")
        st.write(f"**Odchylenie standardowe (std_err)** = {std_err:.3f}")

def show_excel_upload():
    st.header("Wczytywanie pliku Excel")
    st.write("""
    Ta część aplikacji pozwala wgrać własny plik Excel (format `.xlsx` lub `.xls`) 
    i wyświetlić jego zawartość w postaci tabeli, wraz z przykładowymi statystykami.
    """)
    uploaded_file = st.file_uploader(
        "Wybierz plik Excel (xlsx, xls):",
        type=["xlsx", "xls"]
    )
    if uploaded_file is not None:
        try:
            df_excel = pd.read_excel(uploaded_file)
            st.success("Plik wczytany poprawnie. Oto podgląd danych:")
            st.dataframe(df_excel.head(20))

            st.subheader("Podstawowe statystyki")
            st.write(df_excel.describe())
        except Exception as e:
            st.error(f"Błąd odczytu pliku: {e}")
    else:
        st.info("Najpierw wybierz plik w polu powyżej.")

def show_temp_hum_analysis():
    st.header("Analiza temperatury i wilgotności z pliku Excel")
    st.write("""
    Tu możesz przesłać plik z danymi (kolumny: `time`, `temperature`, `humidity`).  
    Zostaną obliczone statystyki, przekroczenia limitów (23-27°C, 55-65%) 
    oraz wygenerowany wykres.
    """)

    uploaded_file = st.file_uploader(
        "Wybierz plik Excel (xlsx, xls):",
        type=["xlsx", "xls"]
    )

    if uploaded_file is not None:
        st.write(f"Analiza pliku: **{uploaded_file.name}**")
        file_bytes = uploaded_file.read()
        generate_report_streamlit(file_bytes)
    else:
        st.info("Nie wybrano pliku - proszę wgrać plik Excel powyżej.")


# -------------------- NOWA STRONA: X-BAR / R-CHART -------------------- #
def show_shewart_xbar_r():
    """
    Strona prezentująca przykład użycia XbarRControlChart z biblioteki sixsigmaspc
    (X-bar i R-chart) na przykładowych danych.
    """
    st.header("Karta kontrolna Shewharta (X-bar / R-chart)")
    st.write("""
    The x-bar and R-chart are control charts used to monitor the mean and variation 
    of a process based on samples taken in a given time.

    - **X-Bar chart**: Śledzi średnią procesu (z poszczególnych podgrup).  
    - **R-chart**: Śledzi rozstęp (range) procesu w tych podgrupach.

    (Źródło inspiracji: [sixsigmastudyguide.com/x-bar-r-control-charts](https://sixsigmastudyguide.com/x-bar-r-control-charts/))
    """)

    # Przykładowe dane i daty
    data = np.array([
        [23, 25, 24, 26],
        [22, 26, 24, 25],
        [28, 28, 22, 23],
        [25, 25, 26, 36],
        [22, 22, 25, 26],
        [26, 24, 23, 22],
        [29, 24, 24, 24],
        [26, 25, 25, 22],
        [22, 25, 24, 24],
        [25, 22, 26, 24],
        [24, 24, 24, 23],
        [24, 25, 26, 23],
        [22, 28, 22, 26],
        [23, 24, 25, 26],
        [24, 25, 29, 24],
        [24, 22, 28, 26],
        [24, 25, 25, 25],
        [22, 24, 25, 26],
        [26, 25, 22, 24],
        [26, 22, 24, 25]
    ])
    dates = [
        '21-12-21', '22-12-21', '23-12-21', '24-12-21', '25-12-21',
        '26-12-21', '27-12-21', '28-12-21', '29-12-21', '30-12-21',
        '31-12-21', '01-01-22', '02-01-22', '03-01-22', '05-01-22',
        '06-01-22', '07-01-22', '08-01-22', '09-01-22', '10-01-22'
    ]

    # Tworzymy wykres X-Bar / R
    chart = XbarRControlChart(
        data=data,
        xlabel="x-label",
        ylabel_top="Średnia (X-bar)",
        ylabel_bottom="Rozstęp (R)"
    )

    # Sprawdzamy normalność
    normally_distributed = chart.normally_distributed(data=chart.value_X, significance_level=0.05)
    st.write(f"Czy rozkład wartości X jest normalny (test na poziomie 0.05)? **{normally_distributed}**")

    # Ustawiamy daty
    chart.dates = dates
    chart.dateformat = "%d-%m-%y"

    # Dodajemy limity i reguły
    chart.limits = True
    chart.append_rules([Rule01(), Rule02(), Rule03(), Rule04(), Rule05(), Rule06(), Rule07(), Rule08()])

    # Rysujemy wykres (przechwytujemy aktualną figurę)
    chart.plot()
    fig = plt.gcf()
    st.pyplot(fig)

    # Dane wykresu X-bar
    df_xbar = chart.data(0)
    st.write("**Dane wykresu X-bar** (CL, UCL, LCL):")
    st.dataframe(df_xbar[["CL", "UCL", "LCL"]].reset_index(drop=True))

    # Dane wykresu R
    df_range = chart.data(1)
    st.write("**Dane wykresu R** (CL, UCL, LCL):")
    st.dataframe(df_range[["CL", "UCL", "LCL"]].reset_index(drop=True))

    st.write("---")
    st.write(f"Czy wykres jest stabilny wg reguł? **{chart.stable()}**")

# ---------------------------------------------------------
# GŁÓWNA CZĘŚĆ APLIKACJI – MENU
# ---------------------------------------------------------
st.title("Santo Pharmstat")

page = st.sidebar.radio(
    "Wybierz podstronę:",
    [
        "Wprowadzenie",
        "Wykres punktowy i liniowy",
        "Regresja liniowa (SciPy)",
        "Wczytanie pliku Excel",
        "Analiza temperatury i wilgotności",
        "Karta kontrolna Shewharta (X-bar / R)"
    ]
)

if page == "Wprowadzenie":
    show_intro()

elif page == "Wykres punktowy i liniowy":
    show_scatter_line()

elif page == "Regresja liniowa (SciPy)":
    show_linreg_scipy()

elif page == "Wczytanie pliku Excel":
    show_excel_upload()

elif page == "Analiza temperatury i wilgotności":
    show_temp_hum_analysis()

elif page == "Karta kontrolna Shewharta (X-bar / R)":
    show_shewart_xbar_r()
