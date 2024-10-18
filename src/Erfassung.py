import joblib

# Geladenes Modell und Vektorisierer
model = joblib.load('Trained Model/druckschmerz_model.pkl')
vectorizer = joblib.load('Trained Model/tfidf_vectorizer.pkl')


def check_druckschmerz(text, keyword, model, vectorizer):
    if keyword.lower() in text.lower():
        # Den Text vektorisieren
        vectorized_text = vectorizer.transform([text])

        # Vorhersage treffen (0 = Kein Druckschmerz, 1 = Druckschmerz)
        prediction = model.predict(vectorized_text)[0]

        if prediction == 1:
            return f"Druckschmerz für '{keyword}' vorhanden."
        else:
            return f"Kein Druckschmerz für '{keyword}'."
    else:
        return f"Stichwort '{keyword}' nicht im Text gefunden."


# Beispieltext und Stichwort
# Liste von Test-Sätzen und Stichwörtern
test_cases = [
    ("Druckschmerz in der Leiste rechts, stärker bei Bewegung.", "Leiste"),
    ("Die Leiste scheint in Ordnung zu sein.", "Leiste"),
    ("Kein Druckschmerz über dem medialen Condylus links.", "Condylus"),
    ("Starker Druckschmerz im Bereich der Bauchdecke links.", "Bauchdecke"),
    ("Die Bauchdecke zeigt keine Auffälligkeiten.", "Bauchdecke"),
    ("Leichter Druckschmerz im Vastus medialis beidseits, links stärker.", "Vastus medialis"),
    ("Vastus lateralis zeigt keine Empfindlichkeit, beidseits unauffällig.", "Vastus lateralis"),
    ("Patella rechts druckempfindlich, links unauffällig.", "Patella"),
    ("Kein Druckschmerz im Bereich des Tibiakopfes links.", "Tibiakopf"),
    ("Mäßiger Druckschmerz über dem Condylus rechts.", "Condylus"),
    ("Die Oberschenkel zeigen keine Auffälligkeiten, kein Druckschmerz beidseits.", "Oberschenkel"),
    ("Im Bereich des Oberschenkels rechts ist der Druckschmerz stärker.", "Oberschenkel"),
    ("Tibiakopf beidseits ohne Anzeichen von Druckschmerz.", "Tibiakopf"),
    ("Starke Druckempfindlichkeit in der Lendenregion, besonders bei Bewegung.", "Lendenregion"),
    ("Kein Druckschmerz in der Lendenregion, normale Beweglichkeit.", "Lendenregion"),
    ("Rhomboidei beidseits negativ.", "Rhomboidei"),
    ("Rotation der Hände in Beugung seitengleich. Die Außenrotation ist rechts etwas weniger.", "Hände"),
    ("Diskretes Streckdefizit des rechten Kniegelenkes. Kein Schmerz bei forcierter Kniestreckung.", "Knie"),
    ("Fingerstrecker beidseits, rechts stärker.", "Fingerstrecker"),
]

# Teste jedes Stichwort und jeden Text
for text, keyword in test_cases:
    result = check_druckschmerz(text, keyword, model, vectorizer)
    print(f"Text: {text}")
    print(f"Ergebnis: {result}\n")
