import queue
import customtkinter as ctk
import os
import json
from tkinter import filedialog
from TextAnalyzerAI.src.classes.Analyzer import analyze_file
import TextAnalyzerAI.src.classes.Constants as Constants
import threading
import time

from TextAnalyzerAI.src.views.Analysis import open_analysis_window

# Pfad für die JSON-Datei
settings_file = Constants.get_settings_path()


def open_read_file(parent):
    analysis_output_queue = queue.Queue()

    def check_queue():
        try:
            analysis_output = analysis_output_queue.get_nowait()
            open_analysis_window(parent, analysis_output)
        except queue.Empty:
            parent.after(100, check_queue)

    def init_settings():
        settings = load_settings()
        if 'verzeichnis' in settings:
            entry_pfad.insert(0, settings['verzeichnis'])  # Pfad in die Textbox einfügen
        if 'datei' in settings:
            settings['datei'] = ""
            save_settings(settings)

    # Funktion, um Daten in die JSON-Datei zu speichern
    def save_settings(data):
        with open(settings_file, "w") as file:
            json.dump(data, file, indent=4)

    # Funktion, um Daten aus der JSON-Datei zu laden
    def load_settings():
        if os.path.exists(settings_file):
            with open(settings_file, "r") as file:
                return json.load(file)
        return {}

    # Funktion für "Pfad auswählen"
    def pfad_auswaehlen():
        pfad = filedialog.askdirectory(title="Verzeichnis auswählen")
        if pfad:
            settings = load_settings()
            settings['verzeichnis'] = pfad
            save_settings(settings)
            entry_pfad.delete(0, ctk.END)  # Vorherigen Text löschen
            entry_pfad.insert(0, pfad)  # Pfad in die Textbox einfügen

    # Funktion für "Datei auswählen"
    def datei_auswaehlen():
        datei = filedialog.askopenfilename(title="Word-Datei auswählen", filetypes=[("Word files", "*.docx")], initialdir=entry_pfad.get())
        if datei:
            settings = load_settings()
            settings['datei'] = os.path.basename(datei)
            save_settings(settings)
            entry_datei.delete(0, ctk.END)  # Vorherigen Text löschen
            entry_datei.insert(0, os.path.basename(datei))  # Dateiname in die Textbox einfügen

    # Funktion für "Datei auslesen"
    def datei_auslesen():
        settings = load_settings()

        # Prüfen, ob der Dateiname und das Verzeichnis existieren
        if 'datei' in settings and settings['datei'] and 'verzeichnis' in settings and settings['verzeichnis']:
            datei_pfad = os.path.join(settings['verzeichnis'], settings['datei'])
            datei = settings['datei']

            if os.path.exists(datei_pfad):
                # Überprüfen, ob die Datei bereits in der Liste eingelesen wurde
                if 'eingelesene_dateien' not in settings:
                    settings['eingelesene_dateien'] = []

                if datei in settings['eingelesene_dateien']:
                    label_state.configure(text=f"Status: Die Datei {datei} wurde bereits analysiert", text_color="red")
                else:
                    # Datei auslesen und zur Liste hinzufügen
                    settings['eingelesene_dateien'].append(datei)
                    save_settings(settings)

                    show_progressbar()
                    progressbar.set(0.0)
                    progressbar.update_idletasks()

                    label_state.configure(text="Status: Datei wird analysiert...", text_color="orange")
                    label_state.update_idletasks()

                    threading.Thread(target=analyze_and_update, args=(datei_pfad,analysis_output_queue)).start()
                    parent.after(100, check_queue)
            else:
                label_state.configure(text="Status: Datei existiert nicht", text_color="red")
        else:
            label_state.configure(text="Status: Bitte Pfad und Datei auswählen", text_color="red")

    def analyze_and_update(datei_pfad, analysis_output_queue):
        for i in range(10):
            time.sleep(0.1)
            progressbar.set((i + 1) / 10)  # Schrittweise Erhöhung um 1/15
            progressbar.update_idletasks()

        if show_analysis.get():
            analysis_output = analyze_file(datei_pfad, show_analysis.get())  # Replace with your actual analysis function
            analysis_output_queue.put(analysis_output)
        else:
            analyze_file(datei_pfad, show_analysis.get())

        # Ensure the progress bar stops at 100%
        progressbar.set(1.0)
        progressbar.update_idletasks()

        hide_progressbar()
        label_state.configure(text="Status: Datei wurde analysiert", text_color="green")

    def hide_progressbar():
        progressbar.grid_remove()

    def show_progressbar():
        progressbar.grid()

    read_file_window = ctk.CTkToplevel(parent)
    read_file_window.geometry("750x400")
    read_file_window.title("Word-Datei einlesen")

    # Padding-Werte für außen (15 Pixel)
    outer_padding = 15

    read_file_window.grab_set()

    # Label "Word-Datei einlesen"
    label_title = ctk.CTkLabel(read_file_window, text="Word-Datei einlesen", font=("Arial", 20))
    label_title.grid(row=0, column=0, columnspan=2, padx=outer_padding, pady=(outer_padding, 10), sticky="ew")

    # Textbox für den Pfad
    entry_pfad = ctk.CTkEntry(read_file_window, width=250, font=("Arial", 16))
    entry_pfad.grid(row=1, column=0, padx=(outer_padding, 10), pady=10, sticky="ew")

    # Button "Pfad auswählen"
    button_pfad_auswaehlen = ctk.CTkButton(
        read_file_window,
        text="Pfad auswählen",
        height=50,
        font=("Arial", 18),
        command=pfad_auswaehlen)
    button_pfad_auswaehlen.grid(row=1, column=1, padx=(10, outer_padding), pady=10, sticky="ew")

    # Textbox für den Dateinamen
    entry_datei = ctk.CTkEntry(read_file_window, placeholder_text="Ausgewählte Datei", width=250, font=("Arial", 16))
    entry_datei.grid(row=2, column=0, padx=(outer_padding, 10), pady=10, sticky="ew")

    # Button "Datei auswählen"
    button_datei_auswaehlen = ctk.CTkButton(
        read_file_window,
        text="Datei auswählen",
        height=50,
        font=("Arial", 18),
        command=datei_auswaehlen)
    button_datei_auswaehlen.grid(row=2, column=1, padx=(10, outer_padding), pady=10, sticky="ew")

    label_state = ctk.CTkLabel(read_file_window, text="Status: Nichts wird analysiert", font=("Arial", 16))
    label_state.grid(row=3, column=0, padx=(outer_padding, 10), pady=10, sticky="ew")

    progressbar = ctk.CTkProgressBar(read_file_window)
    progressbar.configure(mode="determinate")
    progressbar.set(0.0)
    progressbar.grid(row=4, column=0, padx=(outer_padding, 10), pady=10, sticky="ew")
    hide_progressbar()

    # Button "Datei auslesen"
    button_datei_auslesen = ctk.CTkButton(
        read_file_window,
        text="Datei auslesen",
        height=50,
        font=("Arial", 18),
        command=datei_auslesen)
    button_datei_auslesen.grid(row=3, column=1, padx=(10, outer_padding), pady=10, sticky="ew")

    #Checkbox "Show Analysis"
    show_analysis = ctk.CTkCheckBox(read_file_window, text="Show Analysis", font=("Arial", 16))
    show_analysis.grid(row=4, column=1, padx=(10, outer_padding), pady=10, sticky="ew")

    # Button "zum Hauptmenü"
    button_zum_hauptmenue = ctk.CTkButton(
        read_file_window,
        text="Zurück",
        height=50,
        font=("Arial", 18),
        command=read_file_window.destroy)
    button_zum_hauptmenue.grid(row=5, column=0, columnspan=2, padx=outer_padding, pady=10, sticky="ew")

    # Grid-Konfiguration
    read_file_window.grid_columnconfigure(0, weight=1)
    read_file_window.grid_columnconfigure(1, weight=0)
    read_file_window.grid_rowconfigure(0, weight=0)
    read_file_window.grid_rowconfigure(1, weight=0)
    read_file_window.grid_rowconfigure(2, weight=0)
    read_file_window.grid_rowconfigure(3, weight=0)
    read_file_window.grid_rowconfigure(4, weight=0)
    read_file_window.grid_rowconfigure(5, weight=1)

    init_settings()  # Einstellungen initialisieren

    read_file_window.mainloop()

