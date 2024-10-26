import docx
from TextAnalyzerAI.src.brainy_smurf.Brainy_Smurf import ask_brainy_smurf
import json
import os
import TextAnalyzerAI.src.classes.Constants as Constants

json_keywords = Constants.get_keywords_path()
json_statistics = Constants.get_statistics_path()


def get_keywords():
    if os.path.exists(json_keywords):
        with open(json_keywords, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Extrahieren der Singular- und Plural-Werte
        singular_words = [entry['singular'] for entry in data if 'singular' in entry and entry['singular'] != '-']
        plural_words = [entry['plural'] for entry in data if 'plural' in entry and entry['plural'] != '-']

        combined_words = singular_words + plural_words

        return combined_words
    return []


def read_word_file(file_path):
    doc = docx.Document(file_path)
    full_text = []

    # Jeden Paragraph in der Word-Datei durchgehen und den Text hinzufügen
    for para in doc.paragraphs:
        full_text.append(para.text)

    # Die Liste der Texte zu einem einzigen String kombinieren
    return '\n'.join(full_text)


def split_into_sentences(text):
    # Den Text anhand von '.' aufteilen
    sentences = text.split('.')

    # Entfernen von Leerzeichen an den Satzanfängen und -enden
    # und Filtern von leeren Sätzen, falls der Text mehrere '.' in Folge hat
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

    return sentences


def find_sentences_with_keyword(sentences):
    matching_sentences = []
    for sentence in sentences:
        for keyword in get_keywords():
            if keyword.lower() in sentence.lower():
                matching_sentences.append((sentence, keyword))

    return matching_sentences


def update_statistics(keywords):
    if os.path.exists(json_statistics):
        with open(json_statistics, 'r', encoding='utf-8') as file:
            data = json.load(file)
    else:
        data = {"statistics": [], "directory": ""}

    # Check if the keyword already exists in the statistics
    for keyword in keywords:
        keyword_found = False
        for entry in data["statistics"]:
            if entry['keyword'] == keyword:
                entry['count'] += 1
                keyword_found = True
                break

        if not keyword_found:
            data["statistics"].append({"keyword": keyword, "count": 1})

    with open(json_statistics, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


def analyze_file(file_path, show_output):
    text = read_word_file(file_path)
    sentences = split_into_sentences(text)
    matching_sentences = find_sentences_with_keyword(sentences)

    if not show_output:
        output = [keyword for sentence, keyword in matching_sentences if ask_brainy_smurf(sentence, keyword) == 1]
        update_statistics(output)
        return
    else:
        output = [(sentence, keyword, ask_brainy_smurf(sentence, keyword)) for sentence, keyword in matching_sentences]

    return output
