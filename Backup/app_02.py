import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#from sklearn.linear_model import LinearRegression
import sklearn

st.title("Regresja Liniowa w Streamlit")

"""
Aplikacja generuje losowe punkty (X, Y) i dopasowuje do nich 
model regresji liniowej przy pomocy biblioteki **scikit-learn**.
"""

# Krok 1: Wybór liczby punktów do wygenerowania
num_points = st.slider("Ile punktów danych generujemy?", 10, 300, 50)

# Krok 2: Generowanie losowych danych
# Generujemy wartości X w równych odstępach z zakresu [0, 10]
X = np.linspace(0, 10, num_points)

# Generujemy Y = a*X + b + szum losowy
# Na przykład: Y = 3*X + 2, z losowym szumem ~N(0,4)
true_a = 3.0
true_b = 2.0
noise = np.random.randn(num_points) * 4

Y = true_a * X + true_b + noise

# Przechowaj dane w DataFrame (opcjonalnie do podglądu)
df = pd.DataFrame({"X": X, "Y": Y})

# Wyświetlamy surowe dane w tabeli
st.write("Podgląd wygenerowanych danych (pierwsze kilka wierszy):")
st.dataframe(df.head())

# Krok 3: Dopasowanie modelu regresji liniowej
# (Po kliknięciu przycisku)
if st.button("Pokaż wykres i dopasuj regresję"):
    # Tworzymy i trenujemy model
    model = LinearRegression()
    
    # X.reshape(-1,1) zmienia kształt z (num_points,) na (num_points, 1)
    model.fit(X.reshape(-1, 1), Y)

    # Obliczamy przewidywane wartości
    Y_pred = model.predict(X.reshape(-1, 1))

    # Krok 4: Rysowanie wykresu
    fig, ax = plt.subplots()
    ax.scatter(X, Y, label="Dane (punkty)", alpha=0.7)
    ax.plot(X, Y_pred, color="red", label="Linia regresji")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.legend()
    ax.set_title("Regresja liniowa: Y = aX + b")
    
    # Wyświetlenie wykresu w Streamlit
    st.pyplot(fig)
    
    # Wypisanie współczynników modelu
    a_estimated = model.coef_[0]
    b_estimated = model.intercept_
    st.write(f"**Oszacowane parametry modelu:**  \n"
             f"a = {a_estimated:.3f},  b = {b_estimated:.3f}")
    
    st.write("""
    Możesz zwiększać/zmniejszać liczbę punktów i ponownie klikać 
    "Pokaż wykres i dopasuj regresję", aby zobaczyć różne realizacje danych.
    """)

