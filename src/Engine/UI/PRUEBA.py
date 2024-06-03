import tkinter as tk
from tkinter import messagebox

# Funciones para cada opción
def opcion1():
    messagebox.showinfo("Opción 1", "Has seleccionado la opción 1.")

def opcion2():
    messagebox.showinfo("Opción 2", "Has seleccionado la opción 2.")

def opcion3():
    messagebox.showinfo("Opción 3", "Has seleccionado la opción 3.")

def salir():
    root.destroy()

# Configuración de la ventana principal
root = tk.Tk()
root.title("Menú de opciones")
root.geometry("300x200")

# Creación de botones
btn_opcion1 = tk.Button(root, text="Opción 1", command=opcion1)
btn_opcion1.pack(pady=10)

btn_opcion2 = tk.Button(root, text="Opción 2", command=opcion2)
btn_opcion2.pack(pady=10)

btn_opcion3 = tk.Button(root, text="Opción 3", command=opcion3)
btn_opcion3.pack(pady=10)

btn_salir = tk.Button(root, text="Salir", command=salir)
btn_salir.pack(pady=10)

# Ejecución de la ventana principal
root.mainloop()
