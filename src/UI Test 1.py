import customtkinter as ctk
from tkinter import messagebox  # Für die MessageBox
from tkcalendar import Calendar  # Falls du den Kalender verwenden möchtest

def on_button_click():
    label.config(text="Button wurde geklickt!")

def on_switch_toggle():
    label_switch.config(text=f"Switch ist {'AN' if switch_var.get() else 'AUS'}")

def show_messagebox():
    messagebox.showinfo("Info", "Dies ist eine Nachricht!")

def on_slider_change(value):
    progressbar.set(float(value) / 100)

def tab_changed_callback():
    current_tab = tabview.get()
    print(f"Tab gewechselt zu: {current_tab}")

# Hauptfenster erstellen
root = ctk.CTk()
root.geometry("800x600")
root.title("CustomTkinter Widget Übersicht")

# Label
label = ctk.CTkLabel(root, text="Hallo, CustomTkinter!")
label.pack(pady=10)

# Button
button = ctk.CTkButton(root, text="Klick mich", command=on_button_click)
button.pack(pady=10)

# Entry
entry = ctk.CTkEntry(root, placeholder_text="Gib etwas ein")
entry.pack(pady=10)

# Slider
slider = ctk.CTkSlider(root, from_=0, to=100, command=on_slider_change)
slider.pack(pady=10)

# Checkbox
checkbox = ctk.CTkCheckBox(root, text="Option auswählen")
checkbox.pack(pady=10)

# Radiobuttons
radiobutton1 = ctk.CTkRadioButton(root, text="Option 1", value=1)
radiobutton2 = ctk.CTkRadioButton(root, text="Option 2", value=2)
radiobutton1.pack(pady=10)
radiobutton2.pack(pady=10)

# Switch (Umschalter)
switch_var = ctk.BooleanVar(value=False)
switch = ctk.CTkSwitch(root, text="Schalter", command=on_switch_toggle, variable=switch_var)
switch.pack(pady=10)

label_switch = ctk.CTkLabel(root, text="Switch ist AUS")
label_switch.pack(pady=10)

# ProgressBar (Fortschrittsbalken)
progressbar = ctk.CTkProgressBar(root)
progressbar.pack(pady=10)
progressbar.set(0.5)  # Setzt den Fortschritt auf 50%

# OptionMenu
option_menu = ctk.CTkOptionMenu(root, values=["Option 1", "Option 2", "Option 3"])
option_menu.pack(pady=10)

# Combobox
combobox = ctk.CTkComboBox(root, values=["Option A", "Option B", "Option C"])
combobox.pack(pady=10)

# Frame (Rahmen)
frame = ctk.CTkFrame(root)
frame.pack(pady=10, padx=10, fill="both", expand=True)

label_in_frame = ctk.CTkLabel(frame, text="Text im Rahmen")
label_in_frame.pack(pady=10)

# Tabview (Tabs)
tabview = ctk.CTkTabview(root)
tabview.pack(pady=10)
tabview.add("Tab 1")
tabview.add("Tab 2")
tabview.set("Tab 1")

# Funktion aufrufen, wenn Tab gewechselt wird
tabview.configure(command=tab_changed_callback)

label_tab1 = ctk.CTkLabel(tabview.tab("Tab 1"), text="Inhalt von Tab 1")
label_tab1.pack(pady=10)

label_tab2 = ctk.CTkLabel(tabview.tab("Tab 2"), text="Inhalt von Tab 2")
label_tab2.pack(pady=10)

# ScrollableFrame (Scrollbarer Rahmen)
scroll_frame = ctk.CTkScrollableFrame(root, width=200, height=100)
scroll_frame.pack(pady=10)

for i in range(1, 11):
    ctk.CTkLabel(scroll_frame, text=f"Label {i}").pack(pady=5)

# Textbox (Mehrzeiliges Textfeld)
textbox = ctk.CTkTextbox(root, width=300, height=100)
textbox.pack(pady=10)
textbox.insert("1.0", "Mehrzeiliger Text")

# SegmentedButton (Segmentierte Schaltflächen)
segmented_button = ctk.CTkSegmentedButton(root, values=["Segment 1", "Segment 2", "Segment 3"])
segmented_button.pack(pady=10)

# Leinwand (Canvas)
canvas = ctk.CTkCanvas(root, width=200, height=100)
canvas.pack(pady=10)
canvas.create_rectangle(50, 20, 150, 80, fill="blue")

# Kalender (erfordert tkcalendar)
calendar = Calendar(root, selectmode="day")
calendar.pack(pady=10)

# MessageBox Button
messagebox_button = ctk.CTkButton(root, text="Zeige MessageBox", command=show_messagebox)
messagebox_button.pack(pady=10)

# Hauptschleife starten
root.mainloop()
