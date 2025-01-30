## Opis struktury projektu

Projekt skład się z następujących plików:
- analyzing.py - rysowanie wykresów pomagających przenalizować dane,
- cleaning.py - czyści dane, czyli wykonuje operacje takie jak np. rozbicie listy tagów na kolumny albo konwersja daty,
- dashboard.py - generuje interaktywny daschboard wizualizujący dane,
- modeling.py - tworzy klasyfikator, okreslający czy gra zawiera dany tag, czy też nie,
- projekt.ipynb - Jupyter Notebook, główny plik projektu, wykonuje operacje zawarte w plikach .py z wyjątkiem rysowania dashboardu,
- README.md,
- requirenments.txt - zawiera listę bibliotek do zainstalowania przed odpaleniem programów,
- web_scraping.py - pozwala ściągnąć dane ze strony https://store.steampowered.com.

## Instrukcja uruchomienia

Aby uruchomić projekt, należy utworzyć wirtualne środowiko pythonowe i zainstalowac biblioteki z pliku requirenments.txt.
Przykładowe komendy w konsoli (dla systemu Windows):
- python -m venv myvenv (użyj python co najmniej 3.10)
- myvenv\Scripts\activate
- cd <ścieżka_do_folderu_z_projektem>
- pip install -r requirements.txt

Nastepnie można otworzyć plik projekt.ipynb w Visual Studio Code i użyć nowo utworzonego środowiska.
Aby uruchomić venv w VS Code:
- kliknij Ctrl + , i wyszukaj venv,
- dodaj ścieżkę do swojego środowiska.

## Uwagi dotyczące dashboardu

Przed użyciem dashboardu, w Jupyter Notebook należy wykonać krok zapisujący dane do pliku games_data.csv. 
Aby zobaczyć dashboard, należy uruchomić plik dashboard.py w konsoli (używając swtorzonego wcześniej środowiska wirtualnego). Dashboard korzysta z narzędzia Streamlit.