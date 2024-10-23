import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import joblib

# Beispiel-Daten laden (CSV-Datei mit Text und Label)
df = pd.read_csv('../training_data/synthetic_medical_training_1000000.csv')

# Train-Test-Split
X_train, X_test, y_train, y_test = train_test_split(df['Text'], df['Label'], test_size=0.2, random_state=42)

# TF-IDF Vektorisierung der Texte
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Naive Bayes Modell trainieren
model = MultinomialNB()
model.fit(X_train_tfidf, y_train)

# Vorhersagen treffen
y_pred = model.predict(X_test_tfidf)

# Genauigkeit ausgeben
accuracy = accuracy_score(y_test, y_pred)
print(f"Genauigkeit: {accuracy * 100:.2f}%")

# Speichern des Modells
joblib.dump(model, '../trained_model/brainy_smurf.pkl')

# Speichern des TF-IDF-Vektorisierers
joblib.dump(vectorizer, '../trained_model/tfidf_vectorizer.pkl')

print("Das Modell und der Vektorisierer wurden erfolgreich gespeichert.")
