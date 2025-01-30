import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def analyze_data(df):
    # Utworzenie logarytmu liczby recenzji
    df['Log_Liczba_recenzji'] = np.log1p(df['Liczba recenzji'])

    moving_averages(df)
    time_series_decomposition(df)
    cross_table(df)
    scatter_plot(df)

def moving_averages(df):
    # Liczba gier wydanych w poszczególnych latach
    games_per_year = df.groupby('Rok wydania').size()
    # Średnia cena gier w poszczególnych latach
    avg_price_per_year = df.groupby('Rok wydania')['Cena'].mean()

    # Wizualizacja trendów czasowych
    plt.figure(figsize=(14, 6))
    plt.subplot(1, 2, 1)
    games_per_year.plot(kind='bar', color='skyblue', alpha=0.8)
    plt.title("Liczba gier wydanych w poszczególnych latach")
    plt.xlabel("Rok")
    plt.ylabel("Liczba gier")

    plt.subplot(1, 2, 2)
    avg_price_per_year.plot(kind='line', marker='o', color='orange')
    plt.title("Średnia cena gier w poszczególnych latach")
    plt.xlabel("Rok")
    plt.ylabel("Średnia cena (zł)")
    plt.tight_layout()
    plt.show()

def time_series_decomposition(df):
    from statsmodels.tsa.seasonal import seasonal_decompose
    # Wykluczenie roku 2025
    df_filtered = df[df['Rok wydania'] < 2025]
    tag_columns = [col for col in df_filtered.columns if col.startswith('Tag_')]
    tag_trends = df_filtered.groupby('Rok wydania')[tag_columns].sum()
    tag_trends = tag_trends.reindex(range(tag_trends.index.min(), tag_trends.index.max() + 1), fill_value=0)

    selected_tags = ['Tag_RPG', 'Tag_Strategiczne', 'Tag_Symulatory', 'Tag_Akcja', 'Tag_Wieloosobowe']
    plt.figure(figsize=(12, 6))
    for tag in selected_tags:
        plt.plot(tag_trends.index, tag_trends[tag], label=tag.replace('Tag_', ''))
    plt.title('Trendy popularności wybranych tagów w czasie')
    plt.xlabel('Rok wydania')
    plt.ylabel('Liczba gier')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Wybór jednego tagu do analizy trendu
    tag_to_analyze = 'Tag_Strategiczne'
    tag_data = tag_trends[tag_to_analyze]

    # Dekompozycja szeregu czasowego (skupienie na trendzie)
    decomposition = seasonal_decompose(tag_data, model='additive', period=1)

    # Wizualizacja tylko trendu
    plt.figure(figsize=(10, 5))
    plt.plot(decomposition.trend, label='Trend', color='orange')
    plt.title(f'Trend popularności tagu: {tag_to_analyze.replace("Tag_", "")}')
    plt.xlabel('Rok wydania')
    plt.ylabel('Liczba gier')
    plt.legend()
    plt.grid(True)
    plt.show()

def cross_table(df):
    tag_counts = df['Tagi'].str.split(', ').explode().value_counts()
    top_tags = tag_counts.head(20).index
    tag_matrix = pd.DataFrame(0, index=top_tags, columns=top_tags)
    for tags in df['Tagi'].dropna().str.split(', '):
        for tag1 in tags:
            for tag2 in tags:
                if tag1 in top_tags and tag2 in top_tags:
                    tag_matrix.loc[tag1, tag2] += 1
    tag_corr = tag_matrix.corr()
    top_corr_tags = tag_corr.sum().sort_values(ascending=False).head(20).index
    filtered_corr = tag_corr.loc[top_corr_tags, top_corr_tags]

    plt.figure(figsize=(12, 8))
    sns.heatmap(filtered_corr, annot=True, cmap='coolwarm', xticklabels=top_corr_tags, yticklabels=top_corr_tags)
    plt.title('Heatmapa dla 20 najbardziej skorelowanych tagów')
    plt.show()

def scatter_plot(df):
    plt.figure(figsize=(12, 7))

    # Usunięcie rekordów z kategorią 'Brak informacji'
    df_filtered = df[df['Nacechowanie recenzji'] != 'Brak informacji']

    # Definiowanie pełnej i poprawnej kolejności dla legendy
    hue_order = ['Przytłaczająco pozytywne', 'Bardzo pozytywne', 'W większości pozytywne', 'Pozytywne', 'Mieszane', 'Negatywne', 'W większości negatywne', 'Przytłaczająco negatywne']

    # Rysowanie wykresu rozrzutu
    sns.scatterplot(data=df_filtered, x='Cena', y='Log_Liczba_recenzji', hue='Nacechowanie recenzji',
                    hue_order=hue_order, palette='coolwarm', alpha=0.7)
    plt.title('Wpływ ceny na sukces gier')
    plt.xlabel('Cena gry (zł)')
    plt.ylabel('Logarytm liczby recenzji')
    plt.legend(title="Nacechowanie recenzji")
    plt.grid(True)
    plt.show()

