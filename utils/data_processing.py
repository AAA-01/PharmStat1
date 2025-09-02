import pandas as pd
import numpy as np

def calculate_descriptive_stats(df):
    # Najpierw bierzemy tylko kolumny numeryczne (jeśli występują inne typy)
    numeric_df = df.select_dtypes(include=[np.number])
    
    # Uzyskujemy standardowe statystyki i kwantyle
    stats = numeric_df.describe(percentiles=[0.25, 0.5, 0.75])
    
    # Dodajemy wiersz RSD (%) na końcu
    # Uwaga: aby dodać nowy wiersz do describe, sięgamy po loc
    stats.loc['RSD (%)'] = (stats.loc['std'] / stats.loc['mean']) * 100
    
    return stats.round(2)
