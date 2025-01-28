from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
import pandas as pd

def predict_tag(df, target_tag):
    # Upewnienie się, że kolumna celu jest traktowana jako zmienna kategoryczna
    df[target_tag] = df[target_tag].astype('int')  # Konwersja na typ całkowity
    
    # Przygotowanie danych
    X = df[[col for col in df.columns if col.startswith('Tag_') and col != target_tag]]
    y = df[target_tag]
    
    # Podział na zbiór treningowy i testowy
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Standaryzacja danych (opcjonalnie, w zależności od cech)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Trenowanie drzewa decyzyjnego
    clf = DecisionTreeClassifier(class_weight='balanced')
    clf.fit(X_train_scaled, y_train)
    
    # Predykcja na zbiorze testowym
    y_pred = clf.predict(X_test_scaled)
    
    # Ocena modelu
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    
    return accuracy, report