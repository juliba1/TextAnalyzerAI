import customtkinter as ctk
from tkinter import ttk, messagebox

from TextAnalyzerAI.src.classes.Analyzer import update_statistics


def open_analysis_window(parent, analysis_output):
    def update_statistic_button():
        keywords = [
            tree.item(item, "values")[1]  # Get the keyword (2nd column)
            for item in tree.get_children()  # Iterate over all rows
            if tree.item(item, "values")[2] == "Druckschmerz erkannt"  # Filter by Result
        ]

        update_statistics(keywords)
        analysis_window.destroy()

    def convert_result(result):
        return "Druckschmerz erkannt" if result == 1 else "Druckschmerz nicht erkannt"

    def toggle_result():
        # Get the selected item
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie eine Zeile aus, um sie zu bearbeiten.")
            return

        # Get current values
        current_values = tree.item(selected_item, "values")
        sentence, keyword, result = current_values

        # Toggle the result
        new_result = "Druckschmerz erkannt" if result == "Druckschmerz nicht erkannt" else "Druckschmerz nicht erkannt"
        tree.item(selected_item, values=(sentence, keyword, new_result))

    def populate_treeview():
        for idx, (sentence, keyword, result) in enumerate(analysis_output):
            tag = 'oddrow' if idx % 2 == 0 else 'evenrow'
            tree.insert("", "end", values=(sentence, keyword, convert_result(result)), tags=(tag,))

    # Create Analysis Window
    analysis_window = ctk.CTkToplevel(parent)
    analysis_window.geometry("1000x600")
    analysis_window.title("Analyse Ergebnis")

    # Allow resizing
    analysis_window.columnconfigure(0, weight=1)
    analysis_window.rowconfigure(2, weight=1)  # Table row expands with window

    # Padding values
    outer_padding = 15

    analysis_window.grab_set()

    # Title Label
    title_label = ctk.CTkLabel(
        analysis_window,
        text="Analyse Übersicht",
        font=("Arial", 24)
    )
    title_label.grid(row=0, column=0, padx=outer_padding, pady=outer_padding, sticky="ew")

    # Button Frame (top of the window)
    button_frame = ctk.CTkFrame(analysis_window)
    button_frame.grid(row=1, column=0, padx=outer_padding, pady=(outer_padding, 5), sticky="ew")

    # Buttons
    edit_button = ctk.CTkButton(
        button_frame,
        text="Ergebnis ändern",
        height=50,
        command=toggle_result,
        fg_color="#f07000",
        hover_color="#db6600",
        font=("Arial", 18),
        compound="left"
    )
    edit_button.pack(side="left", padx=(0, 10))

    update_button = ctk.CTkButton(
        button_frame,
        text="Ergebnisse speichern",
        height=50,
        command=update_statistic_button,
        fg_color="#00ad09",
        hover_color="#009408",
        font=("Arial", 18),
        compound="left"
    )
    update_button.pack(side="left", padx=(0, 10))

    update_button = ctk.CTkButton(
        button_frame,
        text="Analyse abbrechen",
        height=50,
        command=analysis_window.destroy,
        fg_color="#007bff",
        hover_color="#0056b3",
        font=("Arial", 18),
        compound="left"
    )
    update_button.pack(side="right", padx=(0, 0))

    # Table Frame
    frame = ctk.CTkFrame(analysis_window)
    frame.grid(row=2, column=0, padx=outer_padding, pady=(5, outer_padding), sticky="nsew")

    # Configure resizing for the table frame
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    # Create and style Treeview
    style = ttk.Style()
    style.configure("Treeview.Heading", background="lightblue", foreground="black", font=("Arial", 12, "bold"))
    style.configure("Treeview", rowheight=25, font=("Arial", 14))
    style.map("Treeview", background=[("selected", "lightgray")])
    style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

    tree = ttk.Treeview(frame, columns=("Sentence", "Keyword", "Result"), show="headings")
    tree.heading("Sentence", text="Gefundener Satz")
    tree.heading("Keyword", text="Schlagwort")
    tree.heading("Result", text="Bewertung")

    # Add alternating row colors
    tree.tag_configure('oddrow', background='lightgray')
    tree.tag_configure('evenrow', background='white')

    # Make Treeview scrollable
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="ns")
    tree.grid(row=0, column=0, sticky="nsew")

    populate_treeview()

    analysis_window.mainloop()
