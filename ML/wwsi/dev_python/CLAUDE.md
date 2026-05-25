# CLAUDE.md — Naive Bayes mini-lab (scikit-learn)

## Cel projektu
Zaimplementować 6 krótkich zadań edukacyjnych z Naiwnym Bayesem w Pythonie (scikit-learn), z naciskiem na:
- poprawny dobór wariantu NB do typu danych,
- interpretację wyników (accuracy, confusion matrix, classification_report),
- zrozumienie problemów NLP (OOV, zero-frequency) i wpływu `alpha`,
- powtarzalność eksperymentów.
- należy rozpisywać cały kod w celach edukacyjnych dla osoby bez doświadczenia. 
- przygotować dokumentacje techniczna z przygotowanych propozycji

## Stos technologiczny
- Python 3.10+ (preferowane 3.11)
- scikit-learn
- numpy
- pandas (zadanie 4)
- (opcjonalnie) matplotlib do prostych wykresów

## Struktura repo (proponowana)
- `src/`
  - `task1_spam_multinomialnb.py`
  - `task2_iris_gaussiannb.py`
  - `task3_sentiment_cv_pipeline.py`
  - `task4_play_tennis_bernoullinb.py`
  - `task5_20newsgroups_multinomialnb.py`
  - `task6_alpha_zero_frequency.py`
- `README.md` (jak uruchamiać)
- `requirements.txt` lub `pyproject.toml`

Jeśli użytkownik nie ma repo — generuj kod w formie “po jednym pliku na zadanie” + krótkie instrukcje uruchomienia.

## Wspólne zasady kodu
- Kod ma być uruchamialny “od strzała” (z `if __name__ == "__main__":`).
- Determinizm: ustaw `random_state=42` tam gdzie to ma sens (np. `train_test_split`).
- Czytelność > spryt: krótkie funkcje, sensowne nazwy, komentarze tam gdzie model może mylić.
- Przy ewaluacji zawsze wypisz:
  - metrykę główną (accuracy),
  - oraz dodatkowo (tam gdzie pasuje) confusion matrix / classification_report.
- Dla NLP (zad. 1,3,5,6) zawsze pokaż:
  - rozmiar słownika (np. `len(vectorizer.vocabulary_)`),
  - przykład działania na nowym tekście,
  - `predict_proba()` dla interpretacji pewności.

## Zasady odpowiedzi (jak masz pracować jako Claude)
Zanim napiszesz kod:
1) krótko powiedz co zrobisz (plan 5–10 linijek),
2) wypisz założenia (np. język danych, minimalna liczba przykładów),
3) dopiero potem kod.

Po kodzie:
- po

- wskaż “kluczowe zagadnienie” dla zadania (OOV, dobór NB, ngramy, alpha, itd.).

Nie zmieniaj bibliotek ani algorytmu, jeśli użytkownik nie poprosi.

---

# Zadania

## Zadanie 1: Klasyfikacja spamu (MultinomialNB)
### Dane
Utwórz mini zbiór tekstów (ok. 10 zdań) oznaczonych jako `spam` / `ham`.

### Cel implementacyjny
- Użyć `CountVectorizer` do macierzy zliczeń.
- Wytrenować `MultinomialNB`.
- Przetestować na zdaniu: `"Win a free prize now!"`.
- Wypisać `predict_proba()`.

### Kluczowe zagadnienie
OOV (out-of-vocabulary): pokaż co się dzieje, gdy nowe zdanie ma słowa, których nie było w treningu.
W kodzie dodaj komentarz, że słowa spoza słownika są ignorowane przez wektoryzator.

## Zadanie 2: Iris (GaussianNB)
### Dane
`from sklearn.datasets import load_iris`

### Cel implementacyjny
- `train_test_split` 80/20, `random_state=42`, (opcjonalnie `stratify=y`).
- `GaussianNB`
- `confusion_matrix` + `accuracy_score`

### Kluczowe zagadnienie
Wyjaśnij w komentarzu i/lub w output:
- GaussianNB zakłada cechy ciągłe ~ rozkład normalny w klasach,
- MultinomialNB jest pod dane zliczeniowe (np. częstości słów).

## Zadanie 3: Sentyment + 5-fold CV (Pipeline)
### Dane
20–30 krótkich opinii (pozytywne/negatywne) — można stworzyć ręcznie.

### Cel implementacyjny
- `TfidfVectorizer` zamiast CountVectorizer
- `Pipeline([("tfidf", ...), ("nb", MultinomialNB())])`
- `cross_val_score(..., cv=5, scoring="accuracy")`
- Eksperyment z `ngram_range`:
  - porównaj (1,1) vs (1,2) (i ewentualnie inne)

### Kluczowe zagadnienie
Jak n-gramy wpływają na wynik i dlaczego bigramy czasem pomagają (frazy typu “not good”).

## Zadanie 4: „Grać czy nie grać?” (BernoulliNB)
### Dane
Pandas DataFrame z kolumnami binarnymi:
- `Slonecznie`, `Wysoka_Wilgotnosc`, `Silny_Wiatr`
Etykieta: `Zagra` (0/1).

Jeśli dane wejściowe są tekstowe ("Tak"/"Nie"):
- użyj `LabelEncoder` lub mapowania do 0/1 (pokaż obie opcje krótko; implementuj jedną).

### Cel implementacyjny
- Trenować `BernoulliNB`
- Predykcja dla scenariusza:
  - Słonecznie=1, Silny_Wiatr=1, Wysoka_Wilgotnosc=1
- Wypisać `predict_proba()`

### Kluczowe zagadnienie
BernoulliNB jest do cech binarnych (występuje/nie występuje), a nie zliczeń.

## Zadanie 5: 20 Newsgroups (MultinomialNB)
### Dane
`from sklearn.datasets import fetch_20newsgroups`
Kategorie (przykład):
- `sci.space`
- `comp.graphics`
- `rec.sport.baseball`
- `talk.politics.mideast`

### Cel implementacyjny
- `TfidfVectorizer`
- `MultinomialNB`
- `classification_report`
- Dodatkowo: `confusion_matrix` i krótka analiza, które klasy się mylą.

### Kluczowe zagadnienie
Pokaż najczęstsze pomyłki (np. para klas o najwyższej liczbie błędów).

Uwaga: dataset jest pobierany z internetu; dodaj komunikat, że pierwsze uruchomienie może chwilę potrwać.

## Zadanie 6: Zero Frequency + Alpha
### Dane
Bardzo mały zbiór, gdzie słowo `"promocja"` występuje tylko w spamie.

### Cel implementacyjny
- Trenować `MultinomialNB(alpha=1.0)` i `MultinomialNB(alpha=0.0001)`
- Porównać `predict_proba()` dla wiadomości zawierającej `"promocja"`
- (mile widziane) wypisać log-probabilities lub różnicę pewności

### Kluczowe zagadnienie
Bez wygładzania (alpha→0) brak słowa w klasie daje “prawie zero” prawdopodobieństwa i może zdominować decyzję.

---

## Przydatne importy (preferowane)
```python
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import LabelEncoder