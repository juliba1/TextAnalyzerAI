import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
import os

def open_analysis_window(parent, analysis_output):
    def convert_result(result):
        return "Druckschmerz erkannt" if result == 1 else "Druckschmerz nicht erkannt"

    def save_analysis():
        # Implement save functionality here
        print("Analyse gespeichert")

    def discard_analysis():
        # Implement discard functionality here
        print("Analyse verworfen")

    def populate_treeview():
        for sentence, keyword, result in analysis_output:
            tree.insert("", "end", values=(sentence, keyword, convert_result(result)))

    analysis_window = ctk.CTkToplevel(parent)
    analysis_window.geometry("750x400")
    analysis_window.title("Analyse Ergebniss")

    # Padding values
    outer_padding = 15

    analysis_window.grab_set()

    # Create a frame for the table
    frame = ctk.CTkFrame(analysis_window)
    frame.grid(row=0, column=0, padx=outer_padding, pady=outer_padding, sticky="nsew")

    # Create the table
    style = ttk.Style()
    style.configure("Treeview.Heading", background="lightblue", foreground="black", font=("Arial", 12, "bold"))
    style.configure("Treeview", rowheight=25, font=("Arial", 14))
    style.map("Treeview", background=[("selected", "lightgray")])
    style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])  # Remove borders

    tree = ttk.Treeview(frame, columns=("Sentence", "Keyword", "Result"), show="headings")
    tree.heading("Sentence", text="Schlagwort")
    tree.heading("Keyword", text="Anzahl")
    tree.heading("Result", text="Result")

    tree.tag_configure('oddrow', background='lightgray')
    tree.tag_configure('evenrow', background='white')

    tree.grid(row=0, column=0, sticky="nsew")

    # Create buttons
    button_frame = ctk.CTkFrame(analysis_window)
    button_frame.grid(row=1, column=0, padx=outer_padding, pady=outer_padding, sticky="ew")

    save_button = ctk.CTkButton(button_frame, text="Analyse Speichern", command=save_analysis)
    save_button.pack(side="left", padx=(0, 10))

    discard_button = ctk.CTkButton(button_frame, text="Analyse Verwerfen", command=discard_analysis)
    discard_button.pack(side="left")

    populate_treeview()

    analysis_window.mainloop()