"""
Zadanie 1: Klasyfikacja spamu używając MultinomialNB

Cel:
- Zastosować CountVectorizer do przekształcenia tekstów w macierz zliczeń słów
- Wytrenować model MultinomialNB do klasyfikacji spam/ham
- Zrozumieć problem OOV (Out-Of-Vocabulary) w NLP
- Interpretować wyniki modelu: accuracy, confusion matrix, predict_proba

Kluczowe zagadnienie:
OOV (out-of-vocabulary) - słowa, które nie występowały w zbiorze treningowym
są ignorowane przez wektoryzator. To może wpływać na dokładność predykcji.
"""

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report


def create_spam_dataset():
    """
    Tworzy mini zbiór danych z wiadomościami spam i ham (nie-spam).

    Returns:
        texts (list): Lista wiadomości tekstowych
        labels (list): Lista etykiet (0=ham, 1=spam)
    """
    # Przykładowe wiadomości - spam (1) i ham (0)
    texts = [
        # Spam messages (1)
        "Win a free prize now! Click here!",
        "Congratulations! You won a lottery! Claim your prize!",
        "Free money! Get rich quick! Limited offer!",
        "Click here for amazing deals! Special promotion!",
        "You are a winner! Claim your free gift now!",
        "Earn money fast! Work from home! Easy money!",

        # Ham messages (0)
        "Hi, how are you? Let's meet tomorrow for coffee.",
        "The meeting is scheduled for 3pm on Monday.",
        "Can you please send me the report by end of day?",
        "Thanks for your help with the project yesterday.",
        "I will be out of office next week on vacation.",
        "Please review the attached document and provide feedback."
    ]

    # Etykiety: 0 = ham (normalna wiadomość), 1 = spam
    labels = [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]

    return texts, labels


def main():
    """
    Główna funkcja demonstrująca klasyfikację spam/ham za pomocą MultinomialNB.
    """
    print("=" * 70)
    print("ZADANIE 1: Klasyfikacja spamu (MultinomialNB)")


    # ========================================================================
    # KROK 1: Przygotowanie danych
    # ========================================================================

    texts, labels = create_spam_dataset()

    print(f"Liczba wiadomości: {len(texts)}")
    print(f"Liczba spam: {sum(labels)}")
    print(f"Liczba ham: {len(labels) - sum(labels)}")
    print()

    print("Przykładowe wiadomości:")
    print(f"  SPAM: {texts[0]}")
    print(f"  HAM:  {texts[6]}")
    print()

    # ========================================================================
    # KROK 2: Podział danych na zbiór treningowy i testowy
    # ========================================================================

    # random_state=42 zapewnia powtarzalność wyników
    # test_size=0.25 oznacza 75% danych do treningu, 25% do testów
    # stratify=labels zapewnia proporcjonalny podział klas w obu zbiorach
    X_train, X_test, y_train, y_test = train_test_split(
        texts,
        labels,
        test_size=0.25,
        random_state=42,
        stratify=labels
    )

    print(f"Zbiór treningowy: {len(X_train)} wiadomości")
    print(f"Zbiór testowy: {len(X_test)} wiadomości")
    print()

    # ========================================================================
    # KROK 3: Wektoryzacja tekstów (CountVectorizer)
    # ========================================================================
    print("KROK 3: Wektoryzacja tekstów (CountVectorizer)")


    # CountVectorizer przekształca tekst w macierz zliczeń słów
    # Każda kolumna = jedno słowo ze słownika
    # Każda wartość = liczba wystąpień słowa w dokumencie
    row_id = 0
    vectorizer = CountVectorizer(lowercase=True)
    
    print("vectoriezed", vectorizer)
    X_train_counts = vectorizer.fit_transform(X_train)
    print("X_train_counts", X_train_counts)
    vectorizer.get_feature_names_out()
    print("full_vector", X_train_counts[row_id].toarray())
    print("vector", vectorizer.vocabulary_)
    # fit_transform() - uczy się słownika ze zbioru treningowego
    # i przekształca teksty w macierz zliczeń

    feature_names = vectorizer.get_feature_names_out()
    print("feature name",feature_names)

    # transform() - przekształca nowe teksty używając wyuczonego słownika
    # UWAGA: słowa spoza słownika (OOV) są IGNOROWANE!
    X_test_counts = vectorizer.transform(X_test)
    print("X_test_counts", X_test_counts)
   

    print(f"Rozmiar słownika: {len(vectorizer.vocabulary_)} unikalnych słów")
    print(f"Kształt macierzy treningowej: {X_train_counts.shape}")
    print(f"  (dokumenty: {X_train_counts.shape[0]}, cechy/słowa: {X_train_counts.shape[1]})")
    print()

    # Przykład: pierwsze 10 słów ze słownika (posortowane alfabetycznie)
    vocab_items = sorted(vectorizer.vocabulary_.items(), key=lambda x: x[1])[:10]
    print("Przykładowe słowa ze słownika:")
    for word, idx in vocab_items:
        print(f"  '{word}' -> indeks {idx}")
    print()

    # ========================================================================
    # KROK 4: Trenowanie modelu MultinomialNB
    # ========================================================================
    print("KROK 4: Trenowanie modelu MultinomialNB")
    print("-" * 70)

    # MultinomialNB jest odpowiedni dla danych zliczeniowych (np. częstość słów)
    # alpha=1.0 to wygładzanie Laplace'a (pomaga z problemem zero-frequency)
    model = MultinomialNB(alpha=1.0)

    # Trenowanie modelu na danych treningowych
    model.fit(X_train_counts, y_train)
    print(model.class_log_prior_)
    print(model.feature_log_prob_)
    print("Model został wytrenowany!")
    print(f"Liczba klas: {len(model.classes_)}")
    print(f"Klasy: {model.classes_} (0=ham, 1=spam)")
    print()
 
    # ========================================================================
    # KROK 5: Ewaluacja modelu na zbiorze testowym
    # ========================================================================
    print("KROK 5: Ewaluacja modelu")
    print("-" * 70)

    # Predykcja na zbiorze testowym
    y_pred = model.predict(X_test_counts)

    # Dokładność (accuracy) - procent poprawnie sklasyfikowanych wiadomości
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy (dokładność): {accuracy:.2%}")
    print()
    """
    # Confusion Matrix - macierz pomyłek
    # Wiersze = rzeczywiste klasy, Kolumny = predykcje
    cm = confusion_matrix(y_test, y_pred)
    print("Confusion Matrix:")
    print("                Predicted")
    print("              Ham    Spam")
    print(f"Actual Ham  | {cm[0][0]:3d} | {cm[0][1]:3d} |")
    print(f"Actual Spam | {cm[1][0]:3d} | {cm[1][1]:3d} |")
    print()

    # Classification Report - szczegółowe metryki dla każdej klasy
    print("Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['ham', 'spam']))
    print()

    # ========================================================================
    # KROK 6: Test na nowym zdaniu
    # ========================================================================
    print("KROK 6: Test na nowej wiadomości")
    print("-" * 70)

    # Testowa wiadomość wyraźnie przypomina spam
    new_message = "Win a free prize now!"

    print(f"Nowa wiadomość: '{new_message}'")
    print()

    # Wektoryzacja nowej wiadomości
    new_message_counts = vectorizer.transform([new_message])

    # Predykcja klasy
    prediction = model.predict(new_message_counts)[0]
    prediction_label = "SPAM" if prediction == 1 else "HAM"

    print(f"Predykcja: {prediction_label} (klasa {prediction})")
    print()

    # predict_proba() - prawdopodobieństwa przynależności do każdej klasy
    # Wartości od 0 do 1, suma = 1.0
    probabilities = model.predict_proba(new_message_counts)[0]

    print("Prawdopodobieństwa (predict_proba):")
    print(f"  P(ham)  = {probabilities[0]:.4f} ({probabilities[0]*100:.2f}%)")
    print(f"  P(spam) = {probabilities[1]:.4f} ({probabilities[1]*100:.2f}%)")
    print()

    # ========================================================================
    # KROK 7: Demonstracja problemu OOV (Out-Of-Vocabulary)
    # ========================================================================
    print("KROK 7: Problem OOV (Out-Of-Vocabulary)")
    print("-" * 70)

    # Wiadomość ze słowami całkowicie spoza słownika treningowego
    oov_message = "cryptocurrency blockchain bitcoin ethereum mining"

    print(f"Wiadomość OOV: '{oov_message}'")
    print()

    # Sprawdzamy, które słowa są w słowniku
    words_in_message = oov_message.lower().split()
    print("Analiza słów:")
    for word in words_in_message:
        in_vocab = word in vectorizer.vocabulary_
        status = "✓ W SŁOWNIKU" if in_vocab else "✗ BRAK (OOV)"
        print(f"  '{word}': {status}")
    print()

    # Wektoryzacja i predykcja dla OOV
    oov_counts = vectorizer.transform([oov_message])
    oov_prediction = model.predict(oov_counts)[0]
    oov_proba = model.predict_proba(oov_counts)[0]

    print(f"Predykcja dla OOV: {'SPAM' if oov_prediction == 1 else 'HAM'}")
    print(f"Prawdopodobieństwa: P(ham)={oov_proba[0]:.4f}, P(spam)={oov_proba[1]:.4f}")
    print()

    print("UWAGA WAŻNA - Problem OOV:")
    print("  Słowa spoza słownika treningowego są CAŁKOWICIE IGNOROWANE")
    print("  przez CountVectorizer. Model podejmuje decyzję na podstawie")
    print("  apriori prawdopodobieństw klas (prior probabilities).")
    print("  Dla danych z dużą ilością nieznanych słów, model może")
    print("  nie działać poprawnie!")
    print()

    # ========================================================================
    # KROK 8: Wiadomość z miksem znanych i nieznanych słów
    # ========================================================================
    print("KROK 8: Wiadomość z miksem znanych/nieznanych słów")
    print("-" * 70)

    mixed_message = "Click here for cryptocurrency deals and bitcoin prizes!"

    print(f"Wiadomość: '{mixed_message}'")
    print()

    words_mixed = mixed_message.lower().replace('!', '').split()
    print("Analiza słów:")
    known_count = 0
    for word in words_mixed:
        in_vocab = word in vectorizer.vocabulary_
        if in_vocab:
            known_count += 1
        status = "✓ W SŁOWNIKU" if in_vocab else "✗ BRAK (OOV)"
        print(f"  '{word}': {status}")

    print(f"\nPodsumowanie: {known_count}/{len(words_mixed)} słów rozpoznanych")
    print()

    mixed_counts = vectorizer.transform([mixed_message])
    mixed_prediction = model.predict(mixed_counts)[0]
    mixed_proba = model.predict_proba(mixed_counts)[0]

    print(f"Predykcja: {'SPAM' if mixed_prediction == 1 else 'HAM'}")
    print(f"Prawdopodobieństwa: P(ham)={mixed_proba[0]:.4f}, P(spam)={mixed_proba[1]:.4f}")
    print()

    print("Obserwacja:")
    print("  Mimo że niektóre słowa są nieznane (cryptocurrency, bitcoin),")
    print("  model poprawnie klasyfikuje wiadomość jako SPAM dzięki")
    print("  rozpoznanym słowom charakterystycznym dla spamu (click, deals, prizes).")
    print()

    # ========================================================================
    # PODSUMOWANIE
    # ========================================================================
    print("=" * 70)
    print("PODSUMOWANIE")
    print("=" * 70)
    print()
    print("Kluczowe wnioski:")
    print("  1. MultinomialNB dobrze działa z danymi zliczeniowymi (bag-of-words)")
    print("  2. CountVectorizer przekształca tekst w macierz częstości słów")
    print("  3. Rozmiar słownika determinuje możliwości rozpoznawania")
    print(f"     (tutaj: {len(vectorizer.vocabulary_)} słów)")
    print("  4. Problem OOV: nieznane słowa są całkowicie ignorowane!")
    print("  5. predict_proba() pozwala ocenić pewność klasyfikacji")
    print()
    print("Accuracy na zbiorze testowym: {:.2%}".format(accuracy))
    print()
    print("Zadanie ukończone pomyślnie! ✓")
    print("=" * 70)

"""
if __name__ == "__main__":
    # Uruchomienie programu - kod wykonuje się tylko gdy plik jest uruchomiony
    # bezpośrednio (nie gdy jest importowany jako moduł)
    main()
