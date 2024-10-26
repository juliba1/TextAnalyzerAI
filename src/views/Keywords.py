import customtkinter as ctk
import json
import os
from tkinter import messagebox, ttk
from PIL import Image
import TextAnalyzerAI.src.classes.Constants as Constants

# Pfad für die JSON-Datei
json_file = Constants.get_keywords_path()


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
        data = load_schlagworte()

        # Find the longest word in the 'singular' column
        max_singular_length = max(len(item['singular']) for item in data) if data else 0
        max_singular_width = (max_singular_length * 10) + 20  # Estimate width (10 pixels per character)

        # Configure columns
        treeview_schlagworte.column("Singular", width=max_singular_width, stretch=False)
        treeview_schlagworte.column("Plural", stretch=True)

        for i, item in enumerate(data):
            singular, plural = item['singular'], item['plural']
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            treeview_schlagworte.insert("", "end", values=(singular, plural), tags=(tag,))

    # Bearbeitungsmethode
    def edit_entry():
        try:
            selected_index = treeview_schlagworte.selection()[0]
            selected_value = treeview_schlagworte.item(selected_index, "values")

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
            selected_item = treeview_schlagworte.selection()[0]

            # Bestätigung für das Löschen anfordern
            confirm = messagebox.askyesno("Eintrag löschen", "Möchtest du diesen Eintrag wirklich löschen?")
            if confirm:
                # Eintrag aus der JSON-Liste löschen
                schlagworte.pop(selected_item)

                # Neue Daten in die JSON-Datei speichern
                save_schlagworte(schlagworte)

                # Listbox aktualisieren
                update_schlagwort_liste()
        except IndexError:
            messagebox.showerror("Fehler", "Bitte einen Eintrag auswählen, um ihn zu löschen.")

    # Erstelle ein neues Fenster für die Schlagwortverwaltung
    verwaltung_window = ctk.CTkToplevel(parent)  # Toplevel erstellt ein neues Fenster über dem Hauptfenster
    verwaltung_window.geometry("1000x600")
    verwaltung_window.title("Schlagwort-Verwaltung")

    # Sperre das Hauptfenster, während das neue Fenster geöffnet ist
    verwaltung_window.grab_set()

    # Grid-Konfiguration
    verwaltung_window.grid_columnconfigure(0, weight=1)
    verwaltung_window.grid_columnconfigure(1, weight=1)
    verwaltung_window.grid_columnconfigure(2, weight=1)
    verwaltung_window.grid_columnconfigure(3, weight=1)
    verwaltung_window.grid_rowconfigure(4, weight=1)  # Zeile 3 (Listbox) dehnt sich vertikal aus

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
    button_hinzufuegen.grid(row=1, column=0, padx=(outer_padding, 5), pady=20, sticky="ew")

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
    button_bearbeiten.grid(row=1, column=1, padx=5, pady=20, sticky="ew")

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
    button_loeschen.grid(row=1, column=2, padx=5, pady=20, sticky="ew")

    # Zurück Button auf der rechten Seite
    button_zurueck = ctk.CTkButton(
        verwaltung_window,
        text="Zurück",
        height=50,
        font=("Arial", 18),
        command=verwaltung_window.destroy)
    button_zurueck.grid(row=1, column=3, padx=(5, outer_padding), pady=20, sticky="e")

    label_singular = ctk.CTkLabel(verwaltung_window, text="Bitte den Singular eingeben:", font=("Arial", 16), anchor="w")
    label_singular.grid(row=2, column=0, columnspan=2, padx=(outer_padding, 5), pady=0, sticky="ew")

    label_plural = ctk.CTkLabel(verwaltung_window, text="Bitte den Plural eingeben: (optional)", font=("Arial", 16), anchor="w")
    label_plural.grid(row=2, column=2, columnspan=2, padx=(5, outer_padding), pady=0, sticky="ew")

    # Zweite Reihe: Zwei Textboxen, jeweils halb so breit wie das Fenster
    entry_singular = ctk.CTkEntry(verwaltung_window, placeholder_text="Schlagwort (Singular)", font=("Arial", 16))
    entry_singular.grid(row=3, column=0, columnspan=2, padx=(outer_padding, 5), pady=(0, 10), sticky="ew")

    entry_plural = ctk.CTkEntry(verwaltung_window, placeholder_text="Schlagwort (Plural)", font=("Arial", 16))
    entry_plural.grid(row=3, column=2, columnspan=2, padx=(5, outer_padding), pady=(0, 10), sticky="ew")

    # Dritte Reihe: Listbox über die gesamte Breite, füllt den restlichen Platz aus
    style = ttk.Style()
    style.configure("Treeview.Heading", background="lightblue", foreground="black", font=("Arial", 12, "bold"))
    style.configure("Treeview", rowheight=25, font=("Arial", 14))
    style.map("Treeview", background=[("selected", "lightgray")])
    style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])  # Remove borders

    treeview_schlagworte = ttk.Treeview(verwaltung_window, columns=("Singular", "Plural"), show="headings")
    treeview_schlagworte.heading("Singular", text="Singular", anchor="w")
    treeview_schlagworte.heading("Plural", text="Plural", anchor="w")
    treeview_schlagworte.grid(row=4, column=0, columnspan=4, padx=outer_padding, pady=(10, outer_padding),sticky="nsew")

    # Add striped rows
    treeview_schlagworte.tag_configure('oddrow', background='lightgray')
    treeview_schlagworte.tag_configure('evenrow', background='white')

    # Schlagworte aus JSON-Datei laden und anzeigen
    schlagworte = load_schlagworte()
    update_schlagwort_liste()

    # Warte, bis das Fenster geschlossen wird, bevor das Hauptfenster wieder aktiviert wird
    verwaltung_window.wait_window()
