import json
import os
from tkinter import messagebox

import customtkinter as ctk

from TextAnalyzerAI.src.classes import Constants
from TextAnalyzerAI.src.views.Keywords import open_keywords
from TextAnalyzerAI.src.views.Read_File import open_read_file
from TextAnalyzerAI.src.views.Statistics import open_statistics_window


def main():
    root = ctk.CTk()

    root.title("Automatische Texterkennung")
    root.geometry("800x600")  # Setze die Standardgröße des Fensters

    # Titel der Startseite
    label = ctk.CTkLabel(root, text="Hauptseite", font=("Arial", 24))
    label.pack(pady=20)

    # Button, um zur Einstellungen-Seite zu wechseln
    button = ctk.CTkButton(root, width=250, height=70, font=("Arial", 18), text="Schlagwörter verwalten", command=lambda:open_keywords(root))
    button.pack(pady=10)

    # Button, um zur Einstellungen-Seite zu wechseln
    button = ctk.CTkButton(root, width=250, height=70, font=("Arial", 18), text="Word-Datei einlesen", command=lambda:open_read_file(root))
    button.pack(pady=10)

    # Button, um zur Einstellungen-Seite zu wechseln
    button = ctk.CTkButton(root, width=250, height=70, font=("Arial", 18), text="Statistik auslesen", command=lambda:open_statistics_window(root))
    button.pack(pady=10)

    # Button, um zur Einstellungen-Seite zu wechseln
    button = ctk.CTkButton(root, width=250, height=40, font=("Arial", 16), text="Eingelesene Dateien löschen", command=deleted_read_file)
    button.pack(pady=10)

    # Hauptschleife starten
    root.mainloop()


def deleted_read_file():
    file_path = Constants.get_settings_path()
    with open(file_path, 'r') as file:
        data = json.load(file)
    data['eingelesene_dateien'] = []
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

    messagebox.showinfo("Erfolgreich", "Alle Einträge wurden erfolgreich gelöscht.")


if __name__ == "__main__":
    main()
