# Importación de Tkinter
import tkinter as tk

# Se crea la ventana del programa
root = tk.Tk()
# Se crea el menú de la ventana
menu = tk.Menu()

# Se crean las opciones principales
menu_Clima = tk.Menu(menu, tearoff=0)
menu_Tiempo = tk.Menu(menu, tearoff=0)
menu_Volumen = tk.Menu(menu, tearoff=0)
menu_Salir = tk.Menu(menu, tearoff=0)

# Agregar las opciones principales al menú
menu.add_cascade(label="Clima", menu=menu_Clima)
menu.add_cascade(label="Tiempo", menu=menu_Tiempo)
menu.add_cascade(label="Volumen", menu=menu_Volumen)
menu.add_cascade(label="Salir", menu=menu_Salir)

# Se crean las subopciones para "Clima"
menu_Clima.add_command(label="Lluvia")
menu_Clima.add_command(label="Soleado")
menu_Clima.add_separator()
menu_Clima.add_command(label="Salir", command=root.quit)

# Se crean las subopciones para "Tiempo"
menu_Tiempo.add_command(label="Dia")
menu_Tiempo.add_command(label="Tarde")
menu_Tiempo.add_command(label="Noche")
menu_Tiempo.add_separator()
menu_Tiempo.add_command(label="Salir", command=root.quit)

# Se crean las subopciones para "Volumen"
menu_Volumen.add_command(label="Subir")
menu_Volumen.add_command(label="Bajar")
menu_Volumen.add_separator()
menu_Volumen.add_command(label="Salir", command=root.quit)

# Se crean las subopciones para "Archivo > Preferencias"
menu_preferencias = tk.Menu(menu_Clima, tearoff=0)
menu_preferencias.add_command(label="Opción 1")
menu_preferencias.add_command(label="Opción 2")
menu_preferencias.add_command(label="Opción 3")

# Se crea la cascada de "Preferencias" al menú "Archivo"
menu_Clima.add_cascade(label="Preferencias", menu=menu_preferencias)

# Se muestra la barra de menú en la ventana principal
root.config(menu=menu)

# Bucle de ejecución del programa
root.mainloop()