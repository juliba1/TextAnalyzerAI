import pandas as pd
import random

# Stichworte und Satzbausteine für die Texte
body_parts = ['Leiste', 'Bauchdecke', 'Patella', 'Condylus', 'Oberschenkel', 'Tibiakopf', 'Lendenregion',
              'Vastus medialis', 'Rhomboidei', 'Gluteus maximus']
symptoms = ['Druckschmerz', 'kein Druckschmerz', 'leichter Druckschmerz', 'starker Druckschmerz', 'unauffällig']
sides = ['rechts', 'links', 'beidseits']

# Zusätzliche Phrasen, die als "Kein Druckschmerz" gewertet werden sollen
no_pain_phrases = [
    "scheint in Ordnung zu sein",
    "ist unauffällig",
    "zeigt keine Auffälligkeiten",
    "ist ohne Druckschmerz",
    "ist nicht schmerzhaft"
]

# Phrasen, die auf eine Auffälligkeit hindeuten und als Druckschmerz gewertet werden sollten
pain_indicating_phrases = ['stärker', 'auffällig', 'empfindlich', 'druckempfindlich']

# Zusätzliche "positiv/negativ"-Diagnosephrasen für generelle medizinische Sätze
diagnosis_phrases = ['positiv', 'negativ']
general_phrases = [
    "zeigt keine Auffälligkeiten",
    "ist stabil",
    "ist normal",
    "kein Hinweis auf Pathologie",
    "funktioniert wie erwartet"
]

# Funktion zur zufälligen Generierung von Texten
def generate_medical_text():
    part = random.choice(body_parts)
    side = random.choice(sides)

    # Zufällig entscheiden, ob wir eine reguläre Symptom-Beschreibung, eine "Kein Druckschmerz"-Phrase oder eine "Auffälligkeit"
    if random.random() < 0.2:  # 20% Wahrscheinlichkeit für eine "kein Druckschmerz"-Phrase
        phrase = random.choice(no_pain_phrases)
        return f"Die {part} {side} {phrase}."
    elif random.random() < 0.3:  # 30% Wahrscheinlichkeit für eine Auffälligkeit (Druckschmerz)
        return f"{part} {side}, {random.choice(pain_indicating_phrases)}."
    elif random.random() < 0.2:  # 20% Wahrscheinlichkeit für eine Diagnose (positiv/negativ)
        return f"{part} {side} {random.choice(diagnosis_phrases)}."
    elif random.random() < 0.1:  # 10% Wahrscheinlichkeit für eine allgemeine medizinische Phrase
        return f"Der Zustand der {part} {side} {random.choice(general_phrases)}."
    else:
        symptom = random.choice(symptoms)
        return f"{symptom} in der {part} {side}."

# Funktion zur Festlegung des Labels basierend auf dem Text
def assign_label(text):
    # Wenn der Text "kein Druckschmerz", "unauffällig" oder eine ähnliche Phrase enthält, ist das Label 0
    if any(phrase in text for phrase in
           ['kein Druckschmerz', 'unauffällig', 'scheint in Ordnung zu sein', 'zeigt keine Auffälligkeiten',
            'ist ohne Druckschmerz', 'nicht schmerzhaft', 'negativ']):
        return 0
    # Wenn der Text eine Auffälligkeit erwähnt, wie z.B. "stärker", wird das Label auf 1 gesetzt
    elif any(phrase in text for phrase in pain_indicating_phrases) or 'positiv' in text:
        return 1
    else:
        # Standardmäßig wird nach Symptomen wie "Druckschmerz" oder "starker Druckschmerz" gesucht
        return 1 if 'Druckschmerz' in text else 0

# Generiere den Datensatz mit 10.000 Einträgen
data = []
for _ in range(1000000):
    text = generate_medical_text()
    label = assign_label(text)
    data.append([text, label])

# In DataFrame umwandeln
df = pd.DataFrame(data, columns=['Text', 'Label'])

# CSV-Datei speichern
df.to_csv('synthetic_medical_training_1000000.csv', index=False)

print("CSV-Datei erfolgreich erstellt: 'synthetic_medical_training_data_with_pain_and_strength_phrases.csv'")
