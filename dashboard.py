import plotly.graph_objects as go
import dash
from dash import dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

def create_dashboard():
    data = pd.read_csv('game_data.csv')
    data['Rok wydania'] = pd.to_datetime(data['Data wydania']).dt.year

    tag_columns = [col.replace('Tag_', '') for col in data.columns if col.startswith('Tag_')]

    # Inicjalizacja aplikacji Dash
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    # Layout aplikacji
    app.layout = dbc.Container([
        dbc.Row(dbc.Col(html.H1("Dashboard gier"), className="mb-4")),
        
        dbc.Row([
            dbc.Col([
                html.Label('Filtruj gry po tagach:'),
                dcc.Dropdown(
                    id='tag-filter',
                    options=[{'label': tag, 'value': 'Tag_' + tag} for tag in tag_columns],
                    multi=True,
                    placeholder="Wybierz tagi do analizy"
                ),
                html.Label('Wybierz nacechowanie recenzji:', style={'margin-top': '20px'}),
                dcc.Checklist(
                    id='review-filter',
                    options=[{'label': v, 'value': v} for v in data['Nacechowanie recenzji'].unique()],
                    value=[v for v in data['Nacechowanie recenzji'].unique()],
                    inline=True
                ),
            ], width=4),
            dbc.Col([
                html.Label('Zakres cen:', style={'margin-top': '20px'}),
                dcc.RangeSlider(
                    id='price-range',
                    min=data['Cena'].min(),
                    max=data['Cena'].max(),
                    step=1,
                    value=[data['Cena'].min(), data['Cena'].max()],
                    marks=None
                ),
                html.Div(id='price-range-label', style={'margin-top': '10px'})
            ], width=8)
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                html.Label('Histogram cen gier'),
                dcc.Graph(id='price_histogram'),
            ], width=6),
            dbc.Col([
                html.Label('Nacechowanie recenzji - Wykres kołowy'),
                dcc.Graph(id='review_pie_chart'),
            ], width=6)
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                html.Label('Trendy w tagach gier w ciągu lat'),
                dcc.Graph(id='tags_over_years'),
            ], width=12)
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                html.Label('Popularność tagów (filtrowana przez nacechowanie)'),
                dcc.Graph(id='tag_popularity', style={'height': '500px'}),
            ], width=12)
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                html.Label('Interaktywna tabela gier'),
                dash_table.DataTable(
                    id='data-table',
                    columns=[{"name": i, "id": i} for i in data[['Tytuł', 'Cena', 'Data wydania', 'Nacechowanie recenzji']].columns],
                    style_table={'overflowX': 'auto', 'overflowY': 'auto', 'height': '300px'},
                    page_size=10,
                    style_cell={
                        'height': 'auto',
                        'minWidth': '80px', 'width': '150px', 'maxWidth': '180px',
                        'whiteSpace': 'normal'
                    },
                    sort_action='native'
                )
            ])
        ])
    ])

    # Callback do aktualizacji wszystkich elementów dashboardu
    @app.callback(
        [Output('price_histogram', 'figure'),
        Output('review_pie_chart', 'figure'),
        Output('data-table', 'data'),
        Output('tags_over_years', 'figure'),
        Output('tag_popularity', 'figure'),
        Output('price-range-label', 'children')],
        [Input('review-filter', 'value'),
        Input('tag-filter', 'value'),
        Input('price-range', 'value')])
    def update_content(selected_reviews, selected_tags, price_range):
        # Filtruj dane na podstawie wybranych recenzji i zakresu cen
        filtered_data = data[(data['Nacechowanie recenzji'].isin(selected_reviews)) & (data['Cena'] >= price_range[0]) & (data['Cena'] <= price_range[1])]
        
        # Filtruj dane na podstawie wybranych tagów
        if selected_tags:
            filtered_data = filtered_data[filtered_data[selected_tags].sum(axis=1) > 0]
        
        # Histogram cen
        price_fig = px.histogram(filtered_data, x='Cena', nbins=30, title='Rozkład cen gier')
        
        # Wykres kołowy nacechowania recenzji
        review_fig = px.pie(filtered_data, names='Nacechowanie recenzji', title='Nacechowanie recenzji')
        
        # Tabela danych
        table_data = filtered_data[['Tytuł', 'Cena', 'Data wydania', 'Nacechowanie recenzji']].to_dict('records')
        
        # Trendy w tagach w ciągu lat
        yearly_data = filtered_data.groupby('Rok wydania')[selected_tags].sum() if selected_tags else filtered_data.groupby('Rok wydania').size()
        tags_fig = px.line(yearly_data, x=yearly_data.index, y=yearly_data.columns if selected_tags else yearly_data.values, title='Liczba gier wydanych na rok')
        
        # Wykres popularności tagów
        tag_counts = filtered_data[selected_tags].sum() if selected_tags else filtered_data[data.columns[data.columns.str.startswith('Tag_')]].sum()
        tag_popularity_fig = px.bar(x=[tag.replace('Tag_', '') for tag in tag_counts.index], y=tag_counts.values, title='Popularność tagów', orientation='v')
        
        # Aktualizacja etykiety zakresu cen
        price_label = f"Aktualny zakres cen: {price_range[0]} - {price_range[1]}"

        return price_fig, review_fig, table_data, tags_fig, tag_popularity_fig, price_label

    # Uruchomienie aplikacji
    if __name__ == '__main__':
        app.run_server(debug=True, port=8050)

create_dashboard()