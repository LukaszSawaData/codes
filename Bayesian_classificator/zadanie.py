"""Zadanie 1: Klasyfikacja spamu (MultinomialNB) To klasyczne zastosowanie algorytmu. Twoim zadaniem jest stworzenie prostego filtra antyspamowego.

Dane: Stwórz mały zbiór danych tekstowych (np. 10 zdań), gdzie każde jest oznaczone jako "spam" lub "ham" (nie-spam).

Cel: 1. Wykorzystaj CountVectorizer z sklearn.feature_extraction.text, aby zamienić tekst na postać liczbową (macierz wystąpień słów). 2. Wytrenuj model MultinomialNB. 3. Przetestuj model na nowym zdaniu, np. "Win a free prize now!".

Kluczowe zagadnienie: Zwróć uwagę, jak model radzi sobie ze słowami, których nie było w zbiorze treningowym."""
dataset = {
    "Win a free prize now": "spam",
    "Limited time offer just for you": "spam",
    "Click here to claim your reward": "spam",
    "Exclusive deal available today": "spam",
    "You have won a cash bonus": "spam",
    "Get rich fast with this trick": "spam",
    "Free bonus waiting for you": "spam",
    "Claim your free gift card": "spam",
    "Act now to receive your prize": "spam",
    "Special promotion ends tonight": "spam",
    "Earn money quickly from home": "spam",
    "Congratulations you are selected": "spam",
    "Instant approval no credit check": "spam",
    "Winner claim your reward now": "spam",
    "Cheap loans available instantly": "spam",
    "This is not a scam click now": "spam",
    "Lowest prices guaranteed today": "spam",
    "Buy now pay later offer": "spam",
    "You have been pre approved": "spam",
    "Urgent response needed to claim": "spam",
    "Free vacation waiting for you": "spam",
    "Unlock premium access now": "spam",
    "Double your income fast": "spam",
    "Secret investment opportunity": "spam",
    "Claim your exclusive discount": "spam",
    "Free crypto giveaway today": "spam",
    "Limited bonus act immediately": "spam",
    "You won a brand new phone": "spam",
    "Special discount just arrived": "spam",
    "Risk free trial offer": "spam",
    "Click to verify your account": "spam",
    "Final notice claim prize": "spam",
    "Hot deal do not miss out": "spam",
    "Fast cash transfer available": "spam",
    "Earn passive income easily": "spam",
    "Get your free sample now": "spam",
    "This deal expires soon": "spam",
    "Claim reward before it expires": "spam",
    "Exclusive invitation act now": "spam",
    "Bonus points available today": "spam",
    "Immediate action required": "spam",
    "Win big prizes instantly": "spam",
    "Free access limited time": "spam",
    "Secure your reward today": "spam",
    "Cheap meds without prescription": "spam",
    "Lowest insurance rates here": "spam",
    "You are our lucky winner": "spam",
    "Investment guaranteed profit": "spam",
    "Earn dollars every minute": "spam",
    "Claim your lottery winnings": "spam",
    "Let's schedule a meeting tomorrow": "ham",
    "Please review the attached report": "ham",
    "Lunch at noon works for me": "ham",
    "Project deadline is next week": "ham",
    "Call me when you arrive": "ham",
    "See you at the office": "ham",
    "Can we reschedule the meeting": "ham",
    "The presentation is ready": "ham",
    "Thanks for your help yesterday": "ham",
    "Let's discuss the details later": "ham",
    "Please send the updated document": "ham",
    "Are you joining the call": "ham",
    "Meeting moved to Friday": "ham",
    "I will share the notes soon": "ham",
    "The report looks good": "ham",
    "Can you review this file": "ham",
    "Team lunch next week": "ham",
    "Reminder about the workshop": "ham",
    "I have attached the invoice": "ham",
    "Please confirm receipt": "ham",
    "Let's finalize the budget": "ham",
    "Client meeting at 3pm": "ham",
    "Draft version is completed": "ham",
    "Schedule updated in calendar": "ham",
    "Looking forward to our meeting": "ham",
    "Please provide your feedback": "ham",
    "The system update is done": "ham",
    "I will be on vacation": "ham",
    "Can you call me later": "ham",
    "Thanks for the quick response": "ham",
    "Report submitted successfully": "ham",
    "We need to revise the proposal": "ham",
    "Lunch tomorrow sounds good": "ham",
    "Budget approval received": "ham",
    "Sharing meeting minutes": "ham",
    "Let us plan the next sprint": "ham",
    "The server maintenance is scheduled": "ham",
    "Please check the configuration": "ham",
    "Deployment completed": "ham",
    "Project kickoff meeting today": "ham",
    "I will send the update shortly": "ham",
    "Can we discuss this issue": "ham",
    "The document has been updated": "ham",
    "Reminder about tomorrow call": "ham",
    "Team sync at 10am": "ham",
    "Please review the changes": "ham",
    "Let me know your availability": "ham",
    "We have a new requirement": "ham",
    "Sharing the project timeline": "ham",
    "Thanks for attending the meeting": "ham",
}


import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
data = list(dataset.keys())
labels = list(dataset.values())

X_train_text, X_test_text, y_train, y_test = train_test_split(
    data, labels, test_size=0.2, random_state=42, stratify=labels
)
vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(X_train_text)
X_test = vectorizer.transform(X_test_text)
print(vectorizer.vocabulary_)
print(X_train)
print(X_test),
row = X_train[0]
print("Kolumny:", row.indices)
print("Wartości:", row.data)
X_dense = X_train.toarray()
print(X_dense)
model = MultinomialNB()
model.fit(X_train, y_train)


y_pred = model.predict(X_test)

print(classification_report(y_test, y_pred))
print(model.predict(vectorizer.transform(
    ["You are selected for a free project meeting"]
)))


# test 2
import numpy as np

sentence = ["You are selected for a free project meeting"]
X_vec = vectorizer.transform(sentence)

log_probs = model.predict_log_proba(X_vec)

print("Klasy:", model.classes_)
print("Log-probabilities:", log_probs) # ktora klasa ma wyzszy score