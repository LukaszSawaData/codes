"""
Zadanie 2: Klasyfikacja kwiatów Iris — GaussianNB
=================================================

Cel: Nauczyć się używać GaussianNB do cech ciągłych (float),
w przeciwieństwie do MultinomialNB, który działa na zliczeniach (int >= 0).

Kluczowe zagadnienie:
    - GaussianNB zakłada, że każda cecha w danej klasie pochodzi z rozkładu
      normalnego (Gaussa). Model estymuje średnią (μ) i wariancję (σ²)
      dla każdej cechy osobno w każdej klasie.
    - MultinomialNB jest przeznaczony do danych zliczeniowych (np. liczba
      wystąpień słów w tekście) — NIE nadaje się do ciągłych wartości float.
"""

import numpy as np

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report


def main():
    # ------------------------------------------------------------------ #
    # 1. Wczytanie danych                                                  #
    # ------------------------------------------------------------------ #
    iris = load_iris()
    X = iris.data        # 4 cechy: długość/szerokość działki i płatka [cm]
    y = iris.target      # etykiety: 0=setosa, 1=versicolor, 2=virginica
    class_names = iris.target_names  # ["setosa", "versicolor", "virginica"]

    print(f"Liczba próbek:  {X.shape[0]}")
    print(f"Liczba cech:    {X.shape[1]}  ({', '.join(iris.feature_names)})")
    print(f"Klasy:          {list(class_names)}")


    # ------------------------------------------------------------------ #
    # 2. Podział na zbiór treningowy (80%) i testowy (20%)                 #
    # stratify=y gwarantuje, że proporcje klas są zachowane w obu zbiorach #
    # ------------------------------------------------------------------ #
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y          # 10 próbek każdej klasy w teście (50/50/50 → 10/10/10)
    )

    print(f"Rozmiar zbioru treningowego: {X_train.shape[0]} próbek")
    print(f"Rozmiar zbioru testowego:    {X_test.shape[0]} próbek")

    model = GaussianNB()
    model.fit(X_train, y_train)

    print("Parametry nauczone przez GaussianNB (θ na klasę):")
    for i, cls in enumerate(class_names):
        print(f"  Klasa '{cls}':")
        for j, feat in enumerate(iris.feature_names):
            print(f"    {feat:35s}  μ={model.theta_[i, j]:.3f}  σ²={model.var_[i, j]:.4f}")
    print()

    # ------------------------------------------------------------------ #
    # 4. Predykcja i ewaluacja                                             #
    # ------------------------------------------------------------------ #
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    print(f"Dokładność (accuracy): {acc:.4f}  ({acc*100:.1f}%)")
    print()

    # ------------------------------------------------------------------ #
    # 5. Predykcja dla przykładowej próbki + predict_proba                 #
    # ------------------------------------------------------------------ #
    sample = np.array([[5.1, 3.5, 1.4, 0.2]])  # typowy kwiat setosa
    pred_class = model.predict(sample)[0]
    pred_proba = model.predict_proba(sample)[0]

    print("Przykładowa predykcja:")
    print(f"  Wejście (sepal_len, sepal_wid, petal_len, petal_wid): {sample[0].tolist()}")
    print(f"  Predykowana klasa: {class_names[pred_class]}")
    print("  Prawdopodobieństwa (predict_proba):")
    for cls, prob in zip(class_names, pred_proba):
        bar = "#" * int(prob * 40)
        print(f"    {cls:12s}: {prob:.6f}  |{bar}")
    print()

    # ------------------------------------------------------------------ #
    # 6. Podsumowanie kluczowych zagadnień                                 #
    # ------------------------------------------------------------------ #
    print("=" * 60)
    print("KLUCZOWE ZAGADNIENIA")
    print("=" * 60)
    print("""
GaussianNB vs MultinomialNB — kiedy co używać?

  GaussianNB:
    - cechy CIĄGŁE (float), np. wymiary w cm, temperatura, waga
    - zakłada rozkład normalny P(x_i | klasa) ~ N(μ, σ²)
    - przykłady: Iris, dane medyczne, czujniki

  MultinomialNB:
    - cechy ZLICZENIOWE (int >= 0), np. liczba wystąpień słowa
    - zakłada rozkład wielomianowy
    - przykłady: klasyfikacja tekstu, spam

  BernoulliNB:
    - cechy BINARNE (0/1), np. czy słowo wystąpiło (tak/nie)
    - przykłady: klasyfikacja dokumentów z flagami obecności słów

Macierz pomyłek — jak czytać?
  Przekątna = poprawne predykcje.
  Wartości poza przekątną = błędne klasyfikacje.
  Np. cm[1,2]=2 oznacza: 2 próbki versicolor sklasyfikowano jako virginica.
""")


if __name__ == "__main__":
    main()
