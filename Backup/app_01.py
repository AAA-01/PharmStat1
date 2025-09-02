import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Tytuł aplikacji
st.title("Aplikacja z wyborem typu wykresu (matplotlib + Streamlit)")

# Ustawienie liczby losowych wierszy
num_rows = st.slider("Liczba wierszy danych:", 5, 100, 20)

a = st.sidebar.radio("Select one:", [1, 2])

# Generowanie przykładowych danych (trzy kolumny: X, Y, Z)
random_data = np.random.randn(num_rows, 3)
df = pd.DataFrame(random_data, columns=["X", "Y", "Z"])

# Wyświetlamy tabelę, żeby zobaczyć, co się w niej znajduje
st.write("Oto wygenerowane dane:")
st.dataframe(df)

# Lista rozwijalna (selectbox) do wyboru rodzaju wykresu
chart_type = st.selectbox(
    "Wybierz rodzaj wykresu:",
    ["Linia", "Punktowy (scatter)", "Słupkowy"]
)

# Po kliknięciu przycisku rysujemy wykres
if st.button("Rysuj wykres"):
    # Tworzymy obiekt figury i osi w matplotlib
    fig, ax = plt.subplots()

    if chart_type == "Linia":
        # Wykres liniowy dla każdej kolumny
        for col in df.columns:
            ax.plot(df.index, df[col], label=col)
        ax.set_title("Wykres liniowy (X, Y, Z)")
        ax.legend()

    elif chart_type == "Punktowy (scatter)":
        # Wykres punktowy (scatter) dla każdej kolumny
        for col in df.columns:
            ax.scatter(df.index, df[col], label=col)
        ax.set_title("Wykres punktowy (X, Y, Z)")
        ax.legend()

    else:  # "Słupkowy"
        # Przykład: narysujmy wykres słupkowy (bar) średnich wartości
        mean_values = df.mean()
        ax.bar(mean_values.index, mean_values.values)
        ax.set_title("Wykres słupkowy - średnie wartości (X, Y, Z)")
        # W tym przypadku wystarczy nam legenda w postaci etykiet na osi X

    # Wyświetlenie wykresu w aplikacji
    st.pyplot(fig)

st.write("""
**Wskazówki do rozbudowy:**
- Jeśli chcesz narysować bardziej złożony wykres słupkowy (np. grupowane słupki dla każdej kolumny w każdym wierszu), możesz iterować po indeksach DataFrame i odpowiednio je przesuwać.  
- Jeśli wolisz rysować wykres dla jednej konkretnej kolumny, dodaj kolejne opcje w selectboxie lub osobny selectbox do wyboru kolumny.
- Możesz również dodać pola wejściowe do filtrowania danych przed rysowaniem wykresu.
""")

