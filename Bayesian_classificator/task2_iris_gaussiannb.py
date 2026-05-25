import numpy as np

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report


def main():

    iris = load_iris()
    X = iris.data        # 4 cechy: długość/szerokość działki i płatka [cm]
    y = iris.target      # etykiety: 0=setosa, 1=versicolor, 2=virginica
    class_names = iris.target_names  # ["setosa", "versicolor", "virginica"]


    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y          
    )



    model = GaussianNB()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    print(f"Dokładność (accuracy): {acc:.4f}  ({acc*100:.1f}%)")
    print()


    sample = np.array([[5.1, 3.5, 1.4, 0.2]])  
    pred_class = model.predict(sample)[0]
    pred_proba = model.predict_proba(sample)[0]




if __name__ == "__main__":
    main()
