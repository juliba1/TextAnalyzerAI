import customtkinter as ctk
from TextAnalyzerAI.src.views.Keywords import open_keywords


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
    button = ctk.CTkButton(root, width=250, height=70, font=("Arial", 18), text="Word-Datei einlesen")
    button.pack(pady=10)

    # Button, um zur Einstellungen-Seite zu wechseln
    button = ctk.CTkButton(root, width=250, height=70, font=("Arial", 18), text="Statistik auslesen")
    button.pack(pady=10)

    # Hauptschleife starten
    root.mainloop()


if __name__ == "__main__":
    main()
