import customtkinter as ctk


# Seite 1 (Startseite)
class StartPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Titel der Startseite
        label = ctk.CTkLabel(self, text="Startseite", font=("Arial", 24))
        label.pack(pady=20)

        # Button, um zur Einstellungen-Seite zu wechseln
        button = ctk.CTkButton(self, text="Zu Einstellungen", command=lambda: controller.show_frame("SettingsPage"))
        button.pack(pady=10)


# Seite 2 (Einstellungen)
class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Titel der Einstellungen-Seite
        label = ctk.CTkLabel(self, text="Einstellungen", font=("Arial", 24))
        label.pack(pady=20)

        # Button, um zur Startseite zurückzukehren
        button = ctk.CTkButton(self, text="Zurück zur Startseite", command=lambda: controller.show_frame("StartPage"))
        button.pack(pady=10)


# Hauptanwendung
class MyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Mehrseitige Anwendung mit CustomTkinter")
        self.geometry("800x600")  # Setze die Standardgröße des Fensters

        # Erstelle einen Container, der die Seiten enthält
        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)

        # Grid-Konfiguration, um die Seiten im Container vollständig auszufüllen
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Hier werden alle Frames (Seiten) gespeichert
        self.frames = {}

        # Füge die Seiten (Frames) zum Container hinzu
        for Page in (StartPage, SettingsPage):
            page_name = Page.__name__
            frame = Page(parent=container, controller=self)
            self.frames[page_name] = frame

            # Alle Seiten sollen das gesamte Fenster füllen
            frame.grid(row=0, column=0, sticky="nsew")

        # Zeige die Startseite beim Start der Anwendung
        self.show_frame("StartPage")

    # Methode, um eine bestimmte Seite anzuzeigen
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()  # Bringt den Frame nach vorne


# Anwendung starten
if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
