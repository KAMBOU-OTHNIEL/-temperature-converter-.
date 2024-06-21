import tkinter as tk

def fahrenheit_to_celsius():
    """Convertir Fahrenheit en Celsius et afficher le résultat."""
    try:
        fahrenheit = float(ent_temperature.get())
        celsius = (fahrenheit - 32) * 5.0 / 9.0
        lbl_result["text"] = f"{round(celsius, 2)} \N{DEGREE CELSIUS}"
    except ValueError:
        lbl_result["text"] = "Invalid input"

# Créer la fenêtre principale
window = tk.Tk()
window.title("Temperature Converter")
window.resizable(width=False, height=False)

# Créer un cadre pour l'entrée de la température en Fahrenheit
frm_entry = tk.Frame(master=window)
frm_entry.grid(row=0, column=0, padx=10)

# Créer un widget d'entrée pour accepter la température en Fahrenheit
ent_temperature = tk.Entry(master=frm_entry, width=10)
ent_temperature.grid(row=0, column=0, sticky="e")

# Créer un widget d'étiquette pour afficher le symbole du degré et le texte "F"
lbl_temp = tk.Label(master=frm_entry, text="\N{DEGREE FAHRENHEIT}")
lbl_temp.grid(row=0, column=1, sticky="w")

# Créer un bouton pour lancer le processus de conversion
btn_convert = tk.Button(master=window, text="\N{RIGHTWARDS BLACK ARROW}", command=fahrenheit_to_celsius)
btn_convert.grid(row=0, column=1, pady=10)

# Créer un widget d'étiquette pour afficher le résultat de la conversion en Celsius
lbl_result = tk.Label(master=window, text="\N{DEGREE CELSIUS}")
lbl_result.grid(row=0, column=2, padx=10)

# Démarrer l'application
window.mainloop()
