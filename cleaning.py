import pandas as pd
import numpy as np

def clean_data(df):
    # Konwersja ceny
    def clean_price(price):
        try:
            if "Free to Play" in price:
                return 0.0
            return float(price.replace(' zł', '').replace(',', '.'))
        except:
            return np.nan

    df['Cena'] = df['Cena'].apply(clean_price)

    # Konwersja liczby recenzji
    def clean_reviews(reviews):
        try:
            return int(reviews.replace('Recenzje użytkowników: ', '').replace(' ', ''))
        except:
            return np.nan

    df['Liczba recenzji'] = df['Liczba recenzji'].apply(clean_reviews)

    # Konwersja daty wydania
    polish_months = {
        'STY': 'Jan', 'LUT': 'Feb', 'MAR': 'Mar', 'KWI': 'Apr', 'MAJ': 'May', 'CZE': 'Jun',
        'LIP': 'Jul', 'SIE': 'Aug', 'WRZ': 'Sep', 'PAŹ': 'Oct', 'LIS': 'Nov', 'GRU': 'Dec'
    }

    def clean_date(date):
        if pd.isna(date):
            return np.nan
        for pl, en in polish_months.items():
            date = date.replace(pl, en)
        try:
            return pd.to_datetime(date, format='%d %b %Y')
        except:
            return np.nan

    df['Data wydania'] = df['Data wydania'].apply(clean_date)

    # Rozbicie tagów na kolumny (one-hot encoding)
    def split_tags(tags):
        return tags.split(', ') if isinstance(tags, str) else []

    # Przygotowanie unikalnych tagów
    all_tags = sorted(set(tag for tags in df['Tagi'].apply(split_tags) for tag in tags))
    
    # Tworzenie macierzy tagów (one-hot encoding)
    tags_matrix = pd.DataFrame(
        {
            f'Tag_{tag}': df['Tagi'].apply(lambda tags: 1 if tag in split_tags(tags) else 0)
            for tag in all_tags
        }
    )
    
    # Łączenie oryginalnego DataFrame z macierzą tagów
    df = pd.concat([df.reset_index(drop=True), tags_matrix.reset_index(drop=True)], axis=1)

    # Usuwanie potencjalnych braków danych
    df.dropna(subset=['Cena', 'Liczba recenzji', 'Data wydania'], inplace=True)

    # Dodanie kolumny z rokiem wydania
    df['Data wydania'] = pd.to_datetime(df['Data wydania'])
    df['Rok wydania'] = df['Data wydania'].dt.year

    return df
