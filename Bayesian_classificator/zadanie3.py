"""Zadanie 3: Analiza sentymentu recenzji z walidacją krzyżową Zadanie dla bardziej zaawansowanych, łączące przetwarzanie tekstu z rzetelną oceną modelu.

Dane: Możesz pobrać niewielki zbiór recenzji filmowych lub stworzyć własną listę 20-30 opinii (pozytywnych i negatywnych).

Cel:

Użyj TfidfVectorizer zamiast zwykłego liczenia słów, aby nadać większą wagę istotnym wyrazom.

Zastosuj Pipeline z sklearn.pipeline, aby połączyć wektoryzację z modelem MultinomialNB.

Przeprowadź 5-krotną walidację krzyżową (cross-validation), aby sprawdzić stabilność swojego modelu.

Kluczowe zagadnienie: Sprawdź, jak zmiana parametrów ngram_range w wektoryzatorze (np. analizowanie par słów zamiast pojedynczych wyrazów) wpływa na wynik.

Przydatne biblioteki do importu: Python import numpy as np from sklearn.model_selection import train_test_split, cross_val_score from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer from sklearn.naive_bayes import MultinomialNB, GaussianNB from sklearn.metrics import accuracy_score, confusion_matrix Zadanie 4: Prognoza pogody i decyzja „Grać czy nie grać?” (BernoulliNB) To klasyczny przykład z podręczników uczenia maszynowego. Skupia się na cechach binarnych (tak/nie, 0/1).

Dane: Stwórz ramkę danych (np. w pandas), która zawiera kolumny: Słonecznie, Wysoka_Wilgotność, Silny_Wiatr. Wszystkie wartości to 0 lub 1. Etykieta to Zagra w tenisa (0/1).

Cel:

Wykorzystaj BernoulliNB, który jest zoptymalizowany pod kątem cech binarnych.

Przetestuj model dla scenariusza: Jest słonecznie, ale jest silny wiatr i wysoka wilgotność.

Kluczowe zagadnienie: Użycie LabelEncoder z sklearn.preprocessing, jeśli Twoje dane wejściowe to napisy ("Tak"/"Nie"), zamiast liczb."""



from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import cross_val_score
reviews = [
    # pozytywne
    "This movie was fantastic and inspiring",
    "Absolutely loved the acting and story",
    "Brilliant film with amazing soundtrack",
    "A masterpiece, highly recommend it",
    "Great plot and excellent characters",
    "Wonderful experience, very emotional",
    "Superb direction and cinematography",
    "One of the best movies ever",
    "Outstanding performance by the cast",
    "I enjoyed every minute of it",
    "Beautiful story and strong message",
    "The film was powerful and touching",
    "Incredible visuals and storytelling",
    "A truly uplifting movie",
    "Excellent script and pacing",

    # negatywne
    "Terrible movie and boring plot",
    "I hated the acting",
    "Worst film I have ever seen",
    "Awful experience and bad script",
    "The movie was disappointing",
    "Very slow and predictable",
    "Poorly written and badly directed",
    "Not worth watching at all",
    "Extremely dull and uninteresting",
    "Waste of time",
    "The acting was horrible",
    "The story made no sense",
    "Very weak characters",
    "Completely forgettable film",
    "I regret watching this movie"
]

labels = [1]*15 + [0]*15   # 1=positive, 0=negative
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("nb", MultinomialNB())
])
print("pipeline", pipeline)
scores = cross_val_score(pipeline, reviews, labels, cv=5)

print("Wyniki foldów:", scores)
print("Średnia accuracy:", scores.mean())

pipeline_bigram = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1,2))),
    ("nb", MultinomialNB())
])

scores_bigram = cross_val_score(pipeline_bigram, reviews, labels, cv=5)

print("Średnia accuracy (1-2 grams):", scores_bigram.mean())






