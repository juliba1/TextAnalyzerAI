import customtkinter as ctk
import os
import json
from tkinter import filedialog, messagebox, ttk
import TextAnalyzerAI.src.classes.Constants as Constants
from TextAnalyzerAI.src.classes.Generator import start_generation

# Path for the JSON file
statistics_file = Constants.get_statistics_path()


def open_statistics_window(parent):
    def init_settings():
        settings = load_statistics()
        if 'directory' in settings:
            entry_directory.insert(0, settings['directory'])  # Pfad in die Textbox einfügen

    def load_statistics():
        if os.path.exists(statistics_file):
            with open(statistics_file, "r") as file:
                return json.load(file)
        return {"statistics": [], "directory": ""}

    def save_statistics(statistics, directory):
        data = {"statistics": statistics, "directory": directory}
        with open(statistics_file, "w") as file:
            json.dump(data, file)

    def populate_treeview():
        data = load_statistics()
        statistics = data["statistics"]
        for i, entry in enumerate(statistics):
            keyword, count = entry['keyword'], entry['count']
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            treeview_statistics.insert("", "end", values=(keyword, count), tags=(tag,))

    def get_directory():
        directory = filedialog.askdirectory(title="Select Directory")
        if directory:
            entry_directory.delete(0, ctk.END)
            entry_directory.insert(0, directory)

        statistics = load_statistics()["statistics"]
        save_statistics(statistics, directory)

    def generate_pdf():
        directory = entry_directory.get()
        pdf_name = entry_pdf_name.get()
        if not directory or not pdf_name:
            messagebox.showerror("Error", "Please specify both directory and PDF name.")
            return
        # Here you would add the code to generate the PDF
        start_generation(directory + "/" + pdf_name)
        messagebox.showinfo("Success", f"PDF '{pdf_name}.pdf' generated in '{directory}'")

    statistics_window = ctk.CTkToplevel(parent)
    statistics_window.geometry("850x750")
    statistics_window.title("Statistics")

    outer_padding = 15

    statistics_window.grab_set()

    label_title = ctk.CTkLabel(statistics_window, text="Aufgenommene Werte", font=("Arial", 20))
    label_title.grid(row=0, column=0, columnspan=4, padx=outer_padding, pady=(outer_padding, 10), sticky="ew")

    # Configure Treeview style
    style = ttk.Style()
    style.configure("Treeview.Heading", background="lightblue", foreground="black", font=("Arial", 12, "bold"))
    style.configure("Treeview", rowheight=25, font=("Arial", 14))
    style.map("Treeview", background=[("selected", "lightgray")])
    style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])  # Remove borders

    treeview_statistics = ttk.Treeview(statistics_window, columns=("Keyword", "Count"), show="headings")
    treeview_statistics.heading("Keyword", text="Schlagwort")
    treeview_statistics.heading("Count", text="Anzahl")
    treeview_statistics.grid(row=1, column=0, columnspan=4, padx=outer_padding, pady=10, sticky="nsew")

    # Add striped rows
    treeview_statistics.tag_configure('oddrow', background='lightgray')
    treeview_statistics.tag_configure('evenrow', background='white')

    button_generate_pdf = ctk.CTkButton(
        statistics_window,
        text="Generate PDF",
        height=50,
        font=("Arial", 18),
        command=generate_pdf)
    button_generate_pdf.grid(row=2, column=0, columnspan=4, padx=outer_padding, pady=10, sticky="ew")

    entry_directory = ctk.CTkEntry(statistics_window, placeholder_text="Save Directory", width=250, font=("Arial", 16))
    entry_directory.grid(row=3, column=0, columnspan=2, padx=(outer_padding, 10), pady=10, sticky="ew")

    button_get_directory = ctk.CTkButton(
        statistics_window,
        text="Get Directory",
        height=50,
        font=("Arial", 18),
        command=get_directory)
    button_get_directory.grid(row=3, column=2, columnspan=2, padx=(10, outer_padding), pady=10, sticky="ew")

    entry_pdf_name = ctk.CTkEntry(statistics_window, placeholder_text="PDF Name", width=250, font=("Arial", 16))
    entry_pdf_name.grid(row=4, column=0, columnspan=4, padx=outer_padding, pady=10, sticky="ew")

    button_back_to_home = ctk.CTkButton(
        statistics_window,
        text="Back to Home",
        height=50,
        font=("Arial", 18),
        command=statistics_window.destroy)
    button_back_to_home.grid(row=5, column=1, columnspan=2, padx=outer_padding, pady=10, sticky="ew")

    statistics_window.grid_columnconfigure(0, weight=1)
    statistics_window.grid_columnconfigure(1, weight=1)
    statistics_window.grid_columnconfigure(2, weight=1)
    statistics_window.grid_columnconfigure(3, weight=1)
    statistics_window.grid_rowconfigure(0, weight=0)
    statistics_window.grid_rowconfigure(1, weight=1)
    statistics_window.grid_rowconfigure(2, weight=0)
    statistics_window.grid_rowconfigure(3, weight=0)
    statistics_window.grid_rowconfigure(4, weight=0)
    statistics_window.grid_rowconfigure(5, weight=0)

    populate_treeview()

    init_settings()

    statistics_window.mainloop()
