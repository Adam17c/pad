import pandas as pd
import matplotlib.pyplot as plt

def analyze_data(df):
    # Tworzenie listy wszystkich unikalnych tagów
    #all_tags = set(tag for tags in df['Tagi'].dropna() for tag in tags.split(', '))
    moving_averages(df)
    time_series_decomposition(df)
    cross_table(df)

def moving_averages(df):
    # Konwersja daty wydania na rok
    df['Year'] = df['Data wydania'].dt.year

    # Liczba gier wydanych w poszczególnych latach
    games_per_year = df.groupby('Year').size()

    # Średnia cena gier w poszczególnych latach
    avg_price_per_year = df.groupby('Year')['Cena'].mean()

    # Wizualizacja trendów czasowych
    plt.figure(figsize=(14, 6))

    # Liczba gier na osi 1
    plt.subplot(1, 2, 1)
    games_per_year.plot(kind='bar', color='skyblue', alpha=0.8)
    plt.title("Liczba gier wydanych w poszczególnych latach")
    plt.xlabel("Rok")
    plt.ylabel("Liczba gier")

    # Średnia cena na osi 2
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

    # Lista tagów do analizy (np. najpopularniejsze)
    tag_columns = [col for col in df_filtered.columns if col.startswith('Tag_')]

    # Zliczanie wystąpień każdego tagu w danym roku
    tag_trends = df_filtered.groupby('Rok wydania')[tag_columns].sum()

    # Filtracja lat i uzupełnienie braków w danych dla lat, które nie zawierają żadnej gry
    tag_trends = tag_trends.reindex(range(tag_trends.index.min(), tag_trends.index.max() + 1), fill_value=0)

    # Wizualizacja trendów dla wybranych tagów
    selected_tags = ['Tag_RPG', 'Tag_Strategiczne', 'Tag_Symulatory', 'Tag_Akcja', 'Tag_Wieloosobowe', 'Tag_Battle royale', 'Tag_Zespołowe']  # Przykładowe tagi

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
    import seaborn as sns
    import matplotlib.pyplot as plt

    # Zliczanie liczby wystąpień każdego tagu
    tag_counts = df['Tagi'].str.split(', ').explode().value_counts()

    # Wybór najpopularniejszych tagów
    top_tags = tag_counts.head(20).index

    # Tworzenie macierzy współwystępowania tagów
    tag_matrix = pd.DataFrame(0, index=top_tags, columns=top_tags)

    for tags in df['Tagi'].dropna().str.split(', '):
        for tag1 in tags:
            for tag2 in tags:
                if tag1 in top_tags and tag2 in top_tags:
                    tag_matrix.loc[tag1, tag2] += 1

    # Obliczenie korelacji między tagami
    tag_corr = tag_matrix.corr()
    # Wybranie top 20 tagów z najwyższą sumaryczną korelacją
    top_corr_tags = tag_corr.sum().sort_values(ascending=False).head(20).index
    filtered_corr = tag_corr.loc[top_corr_tags, top_corr_tags]

    # Heatmapa
    plt.figure(figsize=(12, 8))
    sns.heatmap(filtered_corr, annot=True, cmap='coolwarm', xticklabels=top_corr_tags, yticklabels=top_corr_tags)
    plt.title('Heatmapa dla 20 najbardziej skorelowanych tagów')
    plt.show()