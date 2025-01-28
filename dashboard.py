from collections import Counter
import plotly.graph_objects as go
import pandas as pd

def create_dashboard(df):
    map_sentiment(df)

    # Obliczanie wyników
    top_positive_tags = avg_sentiment_and_price_per_tag(df, top_n=20, min_games=3)

    # Tworzenie i wyświetlanie wykresu tylko dla najlepiej ocenianych tagów
    fig_positive = create_dual_axis_chart(top_positive_tags, 'Tagi z najlepszymi ocenami (ważone liczbą recenzji)')
    fig_positive.show()

def map_sentiment(df):
    # Mapowanie tekstowego nacechowania recenzji na wartości numeryczne
    sentiment_map = {
        'Przytłaczająco pozytywne': 4,
        'Bardzo pozytywne': 3,
        'W większości pozytywne': 2,
        'Mieszane': 1,
        'Negatywne': 0
    }
    df['sentiment_score'] = df['Nacechowanie recenzji'].map(sentiment_map).fillna(0)

def avg_sentiment_and_price_per_tag(df, top_n=20, min_games=3):
    tags = df['Tagi'].apply(lambda x: x.split(', '))
    tag_scores = Counter()
    tag_weights = Counter()
    tag_prices = Counter()
    tag_counts = Counter()

    for idx, tag_list in enumerate(tags):
        for tag in tag_list:
            sentiment_score = df.iloc[idx]['sentiment_score']
            review_count = df.iloc[idx]['Liczba recenzji']
            price = df.iloc[idx]['Cena']
            
            # Ważenie ocen liczbą recenzji
            tag_scores[tag] += sentiment_score * review_count
            tag_weights[tag] += review_count
            
            # Suma cen i liczba wystąpień
            tag_prices[tag] += price
            tag_counts[tag] += 1

    # Obliczanie średnich ocen i cen (filtr minimalnej liczby gier)
    avg_data = {
        tag: {
            'Average Sentiment': tag_scores[tag] / tag_weights[tag],
            'Average Price': tag_prices[tag] / tag_counts[tag],
            'Game Count': tag_counts[tag]
        }
        for tag in tag_scores if tag_counts[tag] >= min_games
    }
    avg_df = pd.DataFrame.from_dict(avg_data, orient='index').reset_index()
    avg_df.rename(columns={'index': 'Tag'}, inplace=True)
    
    # Zwracanie DataFrame tylko z najlepszymi ocenami
    return avg_df.sort_values('Average Sentiment', ascending=False).head(top_n)


def create_dual_axis_chart(df, title):
    fig = go.Figure()

    # Słupki dla średniej oceny
    fig.add_trace(go.Bar(
        x=df['Tag'],
        y=df['Average Sentiment'],
        name='Średnia ocena',
        marker_color='#90CAF9',  # Łagodny pastelowy niebieski
        yaxis='y1'
    ))

    # Linie i punkty dla średniej ceny
    fig.add_trace(go.Scatter(
        x=df['Tag'],
        y=df['Average Price'],
        name='Średnia cena',
        mode='lines+markers',
        marker=dict(color='red', size=10),
        line=dict(width=2, dash='dot'),
        yaxis='y2'
    ))

    # Konfiguracja osi Y
    fig.update_layout(
        title=title,
        xaxis=dict(title='Tagi', tickangle=45),
        yaxis=dict(
            title='Średnia ocena',
            titlefont=dict(color='#90CAF9'),  # Dopasowany kolor tytułu osi
            tickfont=dict(color='#90CAF9'),
        ),
        yaxis2=dict(
            title='Średnia cena (zł)',
            titlefont=dict(color='red'),
            tickfont=dict(color='red'),
            overlaying='y',
            side='right'
        ),
        legend=dict(x=0.5, y=1.1, orientation='h')
    )

    return fig
