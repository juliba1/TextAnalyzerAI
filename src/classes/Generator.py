import os
import json
import matplotlib.pyplot as plt
import TextAnalyzerAI.src.classes.Constants as Constants

json_statistics = Constants.get_statistics_path()


def load_data():
    if os.path.exists(json_statistics):
        with open(json_statistics, "r") as file:
            return json.load(file)
    return {"statistics": [], "directory": ""}


def generate_bar_chart(save_path):
    statistics = load_data()["statistics"]
    if not statistics:
        print("No statistics data available.")
        return

    if os.path.exists(save_path + ".png"):
        print("File already exists.")
        return

    keywords = [entry['keyword'] for entry in statistics]
    counts = [entry['count'] for entry in statistics]

    plt.figure(figsize=(10, 6))
    plt.bar(keywords, counts, color='skyblue')
    plt.ylabel('Zahl druckschmerzhafter Orte')
    plt.title('Häufigkeit druckschmerzhafter Lokalisationen bei glutealem und lumbalem Schmerz')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    save_path = os.path.join(save_path + ".png")
    plt.savefig(save_path)
    plt.close()


def start_generation(savepath):
    generate_bar_chart(savepath)
