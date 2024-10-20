import customtkinter as ctk
import json
import os
from tkinter import Listbox, messagebox
from PIL import Image

# Pfad für die JSON-Datei
json_file = "C:/CodeProjekte/TextAnalyzerAI/TextAnalyzerAI/src/views_data/keywords.json"


def open_keywords(parent):

    # Funktion zum Laden der Schlagworte aus der JSON-Datei
    def load_schlagworte():
        if os.path.exists(json_file):
            with open(json_file, "r") as file:
                return json.load(file)
        return []

    # Funktion zum Speichern der Schlagworte in der JSON-Datei
    def save_schlagworte(schlagworte):
        with open(json_file, "w") as file:
            json.dump(schlagworte, file, indent=4)

    # Funktion, um ein neues Schlagwort hinzuzufügen
    def add_schlagwort():
        schlagwort = entry_singular.get().strip()
        plural = entry_plural.get().strip()

        if schlagwort:
            if plural:
                schlagworte.append({"singular": schlagwort, "plural": plural})
            else:
                schlagworte.append({"singular": schlagwort, "plural": "-"})

            save_schlagworte(schlagworte)
            update_schlagwort_liste()
            entry_singular.delete(0, ctk.END)
            entry_plural.delete(0, ctk.END)
        # else:
        # Fehlerbehebung

    # Funktion, um die Liste der Schlagworte in der GUI zu aktualisieren
    def update_schlagwort_liste():
        listbox_schlagworte.delete(0, ctk.END)  # Löscht die Listbox-Einträge
        for item in schlagworte:
            listbox_schlagworte.insert(ctk.END, f" {item['singular']} ({item['plural']})")

    # Bearbeitungsmethode
    def edit_entry():
        try:
            selected_index = listbox_schlagworte.curselection()[0]
            selected_value = schlagworte[selected_index]

            # Eingabe für Singular und Plural anfordern
            new_singular = ctk.CTkInputDialog(text=f"Bearbeite Singular: {selected_value['singular']}",
                                              title="Eintrag bearbeiten").get_input()
            new_plural = ctk.CTkInputDialog(text=f"Bearbeite Plural: {selected_value['plural']}",
                                            title="Eintrag bearbeiten").get_input()

            if new_singular:
                # JSON-Daten aktualisieren
                schlagworte[selected_index]['singular'] = new_singular
            elif new_plural:
                schlagworte[selected_index]['plural'] = new_plural

            # Neue Daten in die JSON-Datei speichern
            save_schlagworte(schlagworte)

            # Listbox aktualisieren
            update_schlagwort_liste()

        except IndexError:
            messagebox.showerror("Fehler", "Bitte einen Eintrag auswählen, um ihn zu bearbeiten.")

    # Löschmethode
    def delete_entry():
        try:
            selected_index = listbox_schlagworte.curselection()[0]

            # Bestätigung für das Löschen anfordern
            confirm = messagebox.askyesno("Eintrag löschen", "Möchtest du diesen Eintrag wirklich löschen?")
            if confirm:
                # Eintrag aus der JSON-Liste löschen
                schlagworte.pop(selected_index)

                # Neue Daten in die JSON-Datei speichern
                save_schlagworte(schlagworte)

                # Listbox aktualisieren
                update_schlagwort_liste()
        except IndexError:
            messagebox.showerror("Fehler", "Bitte einen Eintrag auswählen, um ihn zu löschen.")

    # Erstelle ein neues Fenster für die Schlagwortverwaltung
    verwaltung_window = ctk.CTkToplevel(parent)  # Toplevel erstellt ein neues Fenster über dem Hauptfenster
    verwaltung_window.geometry("1200x600")
    verwaltung_window.title("Schlagwort-Verwaltung")

    # Sperre das Hauptfenster, während das neue Fenster geöffnet ist
    verwaltung_window.grab_set()

    # Grid-Konfiguration
    verwaltung_window.grid_columnconfigure(0, weight=1)
    verwaltung_window.grid_columnconfigure(1, weight=1)
    verwaltung_window.grid_columnconfigure(2, weight=1)
    verwaltung_window.grid_columnconfigure(3, weight=1)
    verwaltung_window.grid_rowconfigure(3, weight=1)  # Zeile 3 (Listbox) dehnt sich vertikal aus

    # Padding-Werte für außen (15 Pixel)
    outer_padding = 15

    # Überschrift hinzufügen
    label_title = ctk.CTkLabel(verwaltung_window, text="Schlagwort-Verwaltung", font=("Arial", 24))
    label_title.grid(row=0, column=0, columnspan=4, padx=outer_padding, pady=(outer_padding, 10), sticky="ew")

    # Erste Reihe: Buttons "Hinzufügen", "Bearbeiten", "Löschen" und "Zurück"
    icon_add = "icons/add.png"  # Pfad zum Icon
    icon_image_add = ctk.CTkImage(light_image=Image.open(icon_add), size=(25, 25))

    button_hinzufuegen = ctk.CTkButton(
        verwaltung_window,
        text="Hinzufügen",
        height=50,
        command=add_schlagwort,
        fg_color="#00ad09",
        hover_color="#009408",
        font=("Arial", 18),
        image=icon_image_add,
        compound="left"
    )
    button_hinzufuegen.grid(row=1, column=0, padx=(outer_padding, 5), pady=10, sticky="ew")

    icon_edit = "icons/edit.png"  # Pfad zum Icon
    icon_image_edit = ctk.CTkImage(light_image=Image.open(icon_edit), size=(25, 25))

    button_bearbeiten = ctk.CTkButton(
        verwaltung_window,
        text="Bearbeiten",
        height=50,
        command=edit_entry,
        fg_color="#f07000",
        hover_color="#db6600",
        font=("Arial", 18),
        image=icon_image_edit,
        compound="left"
    )
    button_bearbeiten.grid(row=1, column=1, padx=5, pady=10, sticky="ew")

    icon_delete = "icons/delete.png"  # Pfad zum Icon
    icon_image_delete = ctk.CTkImage(light_image=Image.open(icon_delete), size=(25, 25))

    button_loeschen = ctk.CTkButton(
        verwaltung_window,
        text="Löschen",
        height=50,
        command=delete_entry,
        fg_color="#fc2626",
        hover_color="#e02222",
        font=("Arial", 18),
        image=icon_image_delete,
        compound="left"
    )
    button_loeschen.grid(row=1, column=2, padx=5, pady=10, sticky="ew")

    # Zurück Button auf der rechten Seite
    button_zurueck = ctk.CTkButton(
        verwaltung_window,
        text="Zurück",
        height=50,
        font=("Arial", 18),
        command=verwaltung_window.destroy)
    button_zurueck.grid(row=1, column=3, padx=(5, outer_padding), pady=10, sticky="e")

    # Zweite Reihe: Zwei Textboxen, jeweils halb so breit wie das Fenster
    entry_singular = ctk.CTkEntry(verwaltung_window, placeholder_text="Schlagwort (Singular)", font=("Arial", 16))
    entry_singular.grid(row=2, column=0, columnspan=2, padx=(outer_padding, 5), pady=10, sticky="ew")

    entry_plural = ctk.CTkEntry(verwaltung_window, placeholder_text="Schlagwort (Plural)", font=("Arial", 16))
    entry_plural.grid(row=2, column=2, columnspan=2, padx=(5, outer_padding), pady=10, sticky="ew")

    # Dritte Reihe: Listbox über die gesamte Breite, füllt den restlichen Platz aus
    listbox_schlagworte = Listbox(verwaltung_window, font=("Arial", 14))
    listbox_schlagworte.grid(row=3, column=0, columnspan=4, padx=outer_padding, pady=(10, outer_padding), sticky="nsew")

    # Schlagworte aus JSON-Datei laden und anzeigen
    schlagworte = load_schlagworte()
    update_schlagwort_liste()

    # Warte, bis das Fenster geschlossen wird, bevor das Hauptfenster wieder aktiviert wird
    verwaltung_window.wait_window()
