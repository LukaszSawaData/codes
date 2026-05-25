"""
Zadanie 1: Klasyfikacja spamu używając MultinomialNB

"""

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report


def create_spam_dataset():

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


    labels = [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]

    return texts, labels


def main():


    texts, labels = create_spam_dataset()

    print(f"Liczba wiadomości: {len(texts)}")
    print(f"Liczba spam: {sum(labels)}")
    print(f"Liczba ham: {len(labels) - sum(labels)}")

    X_train, X_test, y_train, y_test = train_test_split(
        texts,
        labels,
        test_size=0.25,
        random_state=42,
        stratify=labels
    )

    row_id = 0
    vectorizer = CountVectorizer(lowercase=True)

    X_train_counts = vectorizer.fit_transform(X_train)

    vectorizer.get_feature_names_out()
    print("full_vector", X_train_counts[row_id].toarray())
    print("vector", vectorizer.vocabulary_)
    # fit_transform() - uczy się słownika ze zbioru treningowego
    # i przekształca teksty w macierz zliczeń
    X_test_counts = vectorizer.transform(X_test)

   

    print(f"Rozmiar słownika: {len(vectorizer.vocabulary_)} unikalnych słów")
    print(f"Kształt macierzy treningowej: {X_train_counts.shape}")
    print(f"  (dokumenty: {X_train_counts.shape[0]}, cechy/słowa: {X_train_counts.shape[1]})")


    # MultinomialNB jest odpowiedni dla danych zliczeniowych (np. częstość słów)
    # alpha=1.0 to wygładzanie Laplace'a (pomaga z problemem zero-frequency)
    model = MultinomialNB(alpha=1.0)

    model.fit(X_train_counts, y_train)
    print(model.class_log_prior_)
    print(model.feature_log_prob_)

    y_pred = model.predict(X_test_counts)

    # Dokładność (accuracy) - procent poprawnie sklasyfikowanych wiadomości
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy (dokładność): {accuracy:.2%}")


    # Testowa wiadomość SPAM
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


    probabilities = model.predict_proba(new_message_counts)[0]

    print("Prawdopodobieństwa (predict_proba):")
    print(f"  P(ham)  = {probabilities[0]:.4f} ({probabilities[0]*100:.2f}%)")
    print(f"  P(spam) = {probabilities[1]:.4f} ({probabilities[1]*100:.2f}%)")
    print()


if __name__ == "__main__":
    # Uruchomienie programu - kod wykonuje się tylko gdy plik jest uruchomiony
    # bezpośrednio (nie gdy jest importowany jako moduł)
    main()
