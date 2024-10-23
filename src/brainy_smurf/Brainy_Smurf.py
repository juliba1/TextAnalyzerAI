import joblib

# Geladenes Modell und Vektorisierer
model = joblib.load('C:/CodeProjekte/TextAnalyzerAI/TextAnalyzerAI/src/trained_model/brainy_smurf.pkl')
vectorizer = joblib.load('C:/CodeProjekte/TextAnalyzerAI/TextAnalyzerAI/src/trained_model/tfidf_vectorizer.pkl')


def ask_brainy_smurf(text, keyword):
    if keyword.lower() in text.lower():
        # Den Text vektorisieren
        vectorized_text = vectorizer.transform([text])

        # Vorhersage treffen (0 = Kein Druckschmerz, 1 = Druckschmerz)
        prediction = model.predict(vectorized_text)[0]

        return prediction
    else:
        return 2
