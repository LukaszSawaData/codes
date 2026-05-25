"""
Zadanie 5: Klasyfikacja grup dyskusyjnych — 20 Newsgroups + MultinomialNB
=========================================================================

Cel: Nauczyć się klasyfikować wieloklasowe teksty przy użyciu TF-IDF
i MultinomialNB, oraz interpretować macierz pomyłek dla >2 klas.

Kluczowe zagadnienie:
    Macierz pomyłek pozwala zobaczyć, KTÓRE pary klas są mylone najczęściej.
    Np. "sci.space" i "comp.graphics" mogą być mylone rzadziej niż dwie
    klasy o nakładającej się leksyce (polityka vs religia).

Uwaga o danych:
    Dataset 20 Newsgroups jest pobierany z internetu.
    Pierwsze uruchomienie może chwilę potrwać (ok. 14 MB).
"""

import numpy as np

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report


# Wybrane 4 kategorie — tematycznie zróżnicowane
CATEGORIES = [
    "sci.space",
    "comp.graphics",
    "rec.sport.baseball",
    "talk.politics.mideast",
]

# Skrócone nazwy do wyświetlania w macierzy
SHORT_NAMES = ["sci.space", "comp.graph", "rec.baseball", "talk.politics"]


def fetch_data():
    """Pobiera dane treningowe i testowe dla wybranych kategorii."""
    print("Pobieranie danych treningowych...")
    train = fetch_20newsgroups(
        subset="train",
        categories=CATEGORIES,
        remove=("headers", "footers", "quotes"),  
        random_state=42,
    )
    print("Pobieranie danych testowych...")
    test = fetch_20newsgroups(
        subset="test",
        categories=CATEGORIES,
        remove=("headers", "footers", "quotes"),
        random_state=42,
    )
    return train, test


def print_confusion_matrix(cm, labels):
    """Wypisuje macierz pomyłek w czytelnej formie tekstowej."""
    col_w = 14
    header = " " * col_w + "".join(f"{l:>{col_w}}" for l in labels)
    print(header)
    print(" " * col_w + "-" * (col_w * len(labels)))
    for i, row in enumerate(cm):
        row_str = "".join(f"{v:>{col_w}}" for v in row)
        print(f"{labels[i]:>{col_w - 1}} |{row_str}")


def find_worst_confusions(cm, labels, top_n=3):
    """Zwraca top_n par klas o największej liczbie pomyłek (poza przekątną)."""
    pairs = []
    n = len(labels)
    for i in range(n):
        for j in range(n):
            if i != j and cm[i, j] > 0:
                pairs.append((cm[i, j], labels[i], labels[j]))
    pairs.sort(reverse=True)
    return pairs[:top_n]


def main():

    train_data, test_data = fetch_data()


    snippet = train_data.data[0][:400].replace("\n", " ")

    # ------------------------------------------------------------------ #
    # 2. Wektoryzacja TF-IDF                                               #
    # TF-IDF (Term Frequency–Inverse Document Frequency):                  #
    #   - TF  = jak często słowo pojawia się w dokumencie                  #
    #   - IDF = jak rzadkie jest słowo w całym korpusie                    #
    # Słowa pospolite (the, is, a) dostają niski IDF → mniejszą wagę.     #
    # ------------------------------------------------------------------ #
    vectorizer = TfidfVectorizer(
        max_features=20_000,   # ogranicz słownik do 20k najczęstszych tokenów
        sublinear_tf=True,     # zamień TF na 1 + log(TF) — spłaszcza rozkład
        min_df=2,              # ignoruj słowa występujące tylko 1 raz
    )

    X_train = vectorizer.fit_transform(train_data.data)
    X_test  = vectorizer.transform(test_data.data)

    print(f"Rozmiar słownika (po ograniczeniu):  {len(vectorizer.vocabulary_):,} tokenów")
    print(f"Kształt macierzy treningowej:        {X_train.shape}")
    print(f"Kształt macierzy testowej:           {X_test.shape}")
    print()

    # ------------------------------------------------------------------ #
    # 3. Trening MultinomialNB                                             #
    # alpha=0.1 — słabe wygładzanie Laplace'a (mniej niż domyślne 1.0)   #
    # Dla TF-IDF wartości nie są całkowitymi zliczeniami, ale MultinomialNB#
    # radzi sobie z wartościami float >= 0 po TF-IDF.                     #
    # ------------------------------------------------------------------ #
    model = MultinomialNB(alpha=0.1)
    model.fit(X_train, train_data.target)

    # ------------------------------------------------------------------ #
    # 4. Ewaluacja                                                         #
    # ------------------------------------------------------------------ #
    y_pred = model.predict(X_test)
    y_true = test_data.target

    acc = accuracy_score(y_true, y_pred)
    print(f"Dokładność (accuracy): {acc:.4f}  ({acc * 100:.1f}%)")
    print()

    # Raport klasyfikacji — precyzja, recall, F1 dla każdej klasy
    print("Raport klasyfikacji:")
    print(classification_report(y_true, y_pred, target_names=CATEGORIES))

    # ------------------------------------------------------------------ #
    # 5. Macierz pomyłek + analiza błędów                                  #
    # ------------------------------------------------------------------ #
    cm = confusion_matrix(y_true, y_pred)

    print("Macierz pomyłek (wiersze=prawdziwa klasa, kolumny=predykcja):")
    print_confusion_matrix(cm, SHORT_NAMES)
    print()

    # Suma błędów per klasa (poza przekątną)
    errors_per_class = cm.sum(axis=1) - np.diag(cm)
    print("Liczba błędów per klasa:")
    for i, cat in enumerate(CATEGORIES):
        total = cm[i].sum()
        print(f"  {cat:30s}  {errors_per_class[i]:3d} błędów / {total} próbek"
              f"  ({errors_per_class[i]/total*100:.1f}% błędów)")
    print()

    # Najczęstsze pary pomyłek
    worst = find_worst_confusions(cm, CATEGORIES)
    print("Najczęstsze pomyłki (para klas):")
    for count, true_cls, pred_cls in worst:
        print(f"  Prawdziwa: {true_cls:30s} → Predykowana: {pred_cls:30s}  ({count}x)")
    print()

    # ------------------------------------------------------------------ #
    # 6. Predykcja na nowym tekście + predict_proba                        #
    # ------------------------------------------------------------------ #
    new_texts = [
        "NASA launched a new rocket to the International Space Station.",
        "The pitcher threw a fastball in the ninth inning.",
        "OpenGL shaders and GPU rendering pipelines for 3D graphics.",
        "The president signed a new peace agreement in the Middle East.",
    ]

    print("=" * 65)
    print("Predykcja dla nowych tekstów:")
    print("=" * 65)
    X_new = vectorizer.transform(new_texts)
    preds = model.predict(X_new)
    probas = model.predict_proba(X_new)

    for text, pred_idx, proba in zip(new_texts, preds, probas):
        print(f"\nTekst:      \"{text[:70]}\"")
        print(f"Predykcja:  {CATEGORIES[pred_idx]}")
        print("Prawdopodobieństwa:")
        for cat, p in sorted(zip(CATEGORIES, proba), key=lambda x: -x[1]):
            bar = "#" * int(p * 35)
            print(f"  {cat:30s}: {p:.4f}  |{bar}")

    # ------------------------------------------------------------------ #
    # 7. Podsumowanie                                                       #
    # ------------------------------------------------------------------ #
    print()
    print("=" * 65)
    print("KLUCZOWE ZAGADNIENIA")
    print("=" * 65)
    print("""
Macierz pomyłek dla wielu klas:
  - Przekątna = poprawne klasyfikacje dla danej klasy.
  - cm[i, j] (i ≠ j) = dokumenty z klasy i sklasyfikowane jako j.
  - Duże wartości poza przekątną → klasy są leksycznie podobne
    lub mają nakładający się słownik (np. polityka vs religia).

TF-IDF vs CountVectorizer:
  - CountVectorizer: surowe zliczenia słów (BoW).
  - TfidfVectorizer: ważone zliczenia — częste słowa w całym korpusie
    (stop words) dostają mniejszą wagę, rzadkie lecz charakterystyczne
    słowa dostają większą wagę → lepsza dyskryminacja klas.

remove=("headers", "footers", "quotes"):
  - Usuwamy metadane nagłówków (From:, Subject:) i cytaty.
  - Bez tego model mógłby uczyć się na podstawie adresów e-mail
    zamiast treści — overfitting na artefaktach datasetu.
""")


if __name__ == "__main__":
    main()
