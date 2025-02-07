from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import pandas as pd

def predict_tag(df, target_tag):
    df[target_tag] = df[target_tag].astype(int)

    # Przygotowanie danych
    cols_to_exclude = ['Tytuł', 'Tagi', 'Data wydania', 'Nacechowanie recenzji']

    X = df.drop(columns=cols_to_exclude + [target_tag])
    y = df[target_tag]

    # Podział na zbiór treningowy i testowy
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standaryzacja danych
    scaler = StandardScaler()
    X_train[['Cena', 'Liczba recenzji']] = scaler.fit_transform(X_train[['Cena', 'Liczba recenzji']])
    X_test[['Cena', 'Liczba recenzji']] = scaler.transform(X_test[['Cena', 'Liczba recenzji']])

    # Trenowanie lasu losowego
    clf = RandomForestClassifier(class_weight='balanced', n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    # Predykcja na zbiorze testowym
    y_pred = clf.predict(X_test)

    # Ocena modelu
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    
    # Obliczenie macierzy pomyłek i formatowanie jej jako DataFrame
    cm = confusion_matrix(y_test, y_pred)
    cm_df = pd.DataFrame(cm, index=[f'Prawdziwe {cls}' for cls in clf.classes_], 
                         columns=[f'Przewidziane {cls}' for cls in clf.classes_])
    
    print("Tag: ", target_tag)
    print("\nDokładność:", accuracy)
    print("\nRaport klasyfikacji:\n", report)
    print("\nMacierz pomyłek:\n ", cm_df)

