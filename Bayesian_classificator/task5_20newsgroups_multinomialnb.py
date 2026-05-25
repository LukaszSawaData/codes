
import numpy as np

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report


CATEGORIES = [
    "sci.space",
    "comp.graphics",
    "rec.sport.baseball",
    "talk.politics.mideast",
]


SHORT_NAMES = ["sci.space", "comp.graph", "rec.baseball", "talk.politics"]


def fetch_data():

    train = fetch_20newsgroups(
        subset="train",
        categories=CATEGORIES,
        remove=("headers", "footers", "quotes"),  
        random_state=42,
    )

    test = fetch_20newsgroups(
        subset="test",
        categories=CATEGORIES,
        remove=("headers", "footers", "quotes"),
        random_state=42,
    )
    return train, test




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

    vectorizer = TfidfVectorizer(
        max_features=20_000,   # ogranicz słownik do 20k najczęstszych tokenów
        sublinear_tf=True,     # zamień TF na 1 + log(TF) — spłaszcza rozkład
        min_df=2,              # ignoruj słowa występujące tylko 1 raz
    )

    X_train = vectorizer.fit_transform(train_data.data)
    X_test  = vectorizer.transform(test_data.data)

    model = MultinomialNB(alpha=0.1)
    model.fit(X_train, train_data.target)

    # ------------------------------------------------------------------ #
    # 4. Ewaluacja                                                         #
    # ------------------------------------------------------------------ #
    y_pred = model.predict(X_test)
    y_true = test_data.target

    acc = accuracy_score(y_true, y_pred)
    print(f"Dokładność (accuracy): {acc:.4f}  ({acc * 100:.1f}%)")



    new_texts = [
        "NASA launched a new rocket to the International Space Station.",
        "The pitcher threw a fastball in the ninth inning.",
        "OpenGL shaders and GPU rendering pipelines for 3D graphics.",
        "The president signed a new peace agreement in the Middle East.",
    ]
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


if __name__ == "__main__":
    main()
