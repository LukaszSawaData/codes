from sklearn.datasets import load_iris
iris = load_iris()
print(iris.data)


X = iris.data
y = iris.target

print(X.shape)  # (150, 4)
print(y.shape)  # (150,)
print(iris.target_names)  # ['setosa' 'versicolor' 'virginica']

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,       # 20% do testu
    random_state=42,     # powtarzalność
    stratify=y           # zachowaj proporcje klas
)
from sklearn.naive_bayes import GaussianNB

model = GaussianNB()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nConfusion matrix (rows=true, cols=pred):\n", confusion_matrix(y_test, y_pred))
print("\nRaport:\n", classification_report(y_test, y_pred, target_names=iris.target_names))

print("\nPriory:", model.class_prior_)
print("\nŚrednie (theta_):\n", model.theta_)
print("\nWariancje (var_):\n", model.var_)