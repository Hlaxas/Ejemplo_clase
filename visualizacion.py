# Librerías necesarias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox, filedialog
from PIL import ImageTk
from Analisis import DataAnalyzer
import subprocess

# Cargar datos
try:
    data = pd.read_csv('adult.csv')  # Puedes cambiar la ruta del archivo
    analizar = DataAnalyzer(data)
except Exception as e:
    messagebox.showerror("Error al cargar los datos", str(e))
    exit()

# Función: Mostrar resumen de datos
def mostrar_informacion():
    try:
        resumen = analizar.summary()
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.END, resumen)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo mostrar el resumen.\n{e}")

# Función: Mostrar imagen en el área designada
def mostrar_imagen(pil_img):
    try:
        imagen_tk = ImageTk.PhotoImage(pil_img)
        image_label.config(image=imagen_tk)
        image_label.image = imagen_tk  # Referencia para evitar recolección de basura
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo mostrar la imagen.\n{e}")

# Función: Mostrar matriz de correlación
def mostrar_matriz_correlacion():
    try:
        img = analizar.correlation_matrix()
        mostrar_imagen(img)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo generar la matriz de correlación.\n{e}")

# Función: Mostrar análisis categórico con selección por Listbox
def mostrar_analisis_categorico():
    columnas = analizar.df.select_dtypes(include='object').columns.tolist()
    if not columnas:
        messagebox.showinfo("Categorico", "No hay columnas categóricas en el DataFrame.")
        return

    # Crear ventana emergente
    popup = tk.Toplevel(ventana)
    popup.title("Selecciona una columna categórica")

    tk.Label(popup, text="Elige una columna:", font=('Arial', 10, 'bold')).pack(pady=(10, 0))

    listbox = tk.Listbox(popup, height=min(12, len(columnas)), exportselection=False)
    for col in columnas:
        listbox.insert(tk.END, col)
    listbox.pack(padx=15, pady=10)

    def confirmar_seleccion():
        seleccion = listbox.get(tk.ACTIVE)
        if seleccion:
            try:
                img = analizar.categorical_analisis_col(seleccion)
                mostrar_imagen(img)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo analizar la columna.\n{e}")
        popup.destroy()

    tk.Button(popup, text="Confirmar", command=confirmar_seleccion).pack(pady=5)
    
def subir_a_github():
    try:
        # Comando para subir a GitHub
        subprocess.run(["git", "add", "adult.csv"], check=True)
        subprocess.run(["git", "commit", "-m", "Nueva muestra agregada desde la interfaz"], check=True)
        subprocess.run(["git", "push"], check=True)
        messagebox.showinfo("Éxito", "Datos subidos a GitHub correctamente.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"No se pudo subir a GitHub.\n{e}")
    
def agregar_nueva_muestra():
    # Función para agregar una nueva muestra al DataFrame
    columnas = analizar.df.columns.tolist()
    
    popup = tk.Toplevel(ventana)
    popup.title("Agregar Nueva Muestra")
    
    entradas = {}
    
    for i, col in enumerate(columnas):
        tk.Label(popup, text = col).grid(row=i, column=0, sticky='w', padx=10, pady=2)
        entrada = tk.Entry(popup, width=30)
        entrada.grid(row=i, column=1, padx=5, pady=2)
        entradas[col] = entrada
    def guardar():
        nueva_muestra = {}
        for col, entrada in entradas.items():
            valor = entrada.get()
            if col in analizar.numeric_cols:
                try:
                    valor = float(valor)
                except ValueError:
                    messagebox.showerror("Error", f"El valor de {col} no es numérico.")
                    return
            nueva_muestra[col] = valor
        # Agregar la nueva muestra al DataFrame
        try:
            nueva_df = pd.DataFrame([nueva_muestra])
            analizar.df = pd.concat([analizar.df, nueva_df], ignore_index=True)
            analizar.df.to_csv('adult.csv', index=False)  # Guardar el DataFrame actualizado
            messagebox.showinfo("Éxito", "Nueva muestra agregada correctamente.")
            popup.destroy()
            subir_a_github()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar la nueva muestra.\n{e}")
    tk.Button(frame_botones, text="Guardar", command=guardar).grid(row = len(columnas), column=0, columnspan=2, pady=10)


# ------------------ Interfaz Gráfica ------------------

ventana = tk.Tk()
ventana.title("Análisis de Datos")
ventana.geometry("1000x600")

# Botones de navegación
frame_botones = tk.Frame(ventana)
frame_botones.grid(row=0, column=0, columnspan=2, pady=10)

tk.Button(frame_botones, text="Resumen", width=15, command=mostrar_informacion).grid(row=0, column=0, padx=10)
tk.Button(frame_botones, text="Matriz Numérica", width=15, command=mostrar_matriz_correlacion).grid(row=0, column=1, padx=10)
tk.Button(frame_botones, text="Análisis Categórico", width=18, command=mostrar_analisis_categorico).grid(row=0, column=2, padx=10)
tk.Button(frame_botones, text="Agregar Muestra", width=15, command=agregar_nueva_muestra).grid(row=0, column=3, padx=10)

# Área de texto para resumen
text_area = ScrolledText(ventana, width=70, height=30)
text_area.grid(row=1, column=1, padx=10, pady=10)

# Área para visualización de imágenes
frame_imagen = tk.Frame(ventana)
frame_imagen.grid(row=1, column=0, padx=10, pady=10)

image_label = tk.Label(frame_imagen)
image_label.grid(row=0, column=0)

ventana.mainloop()
