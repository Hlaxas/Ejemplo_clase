# Librerías necesarias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox, simpledialog, filedialog
from Analisis import DataAnalyzer
from PIL import ImageTk
import subprocess

# ------------------ cargar datos ------------------
data = pd.read_csv('adult.csv') #Puedo colocar la ruta del archivo .csv o de otro archivo .csv
analizar = DataAnalyzer(data)

# ------------------ Funciones de la interfaz ------------------
info = analizar.summary()
def informacion():
    try:
        text_area.delete('1.0', tk.END)  # Limpiar el área de texto antes de mostrar la nueva información
        info = analizar.summary()
        text_area.insert(tk.END, info)
    except:
        messagebox.showerror("Error", "No se pudo obtener la información del DataFrame.")
        
def mostrar_imagenes(pill_img):
    image_tk = ImageTk.PhotoImage(pill_img)
    image_label.config(image=image_tk) #Muestra la imagen
    image_label.image = image_tk  # Mantener una referencia a la imagen para evitar que se elimine por el recolector de basura
    
def mostrar_matriz_correlacion():
    img = analizar.correlation_matrix() #muestra la matriz de correlación
    mostrar_imagenes(img) #esta función muestra la imagen de la matriz de correlación

def mostrar_categorico():
    cols = analizar.df.select_dtypes(include = 'object').columns.tolist()
    if not cols:
        messagebox.showinfo("Categorico", "No hay columnas categóricas en el DataFrame.")
    else:
        sel = simpledialog.askstring("Columna", f"elige una columna de las siguientes: \n {cols}")
        if sel in cols:
            img = analizar.categorical_analisis_col(sel)
            mostrar_imagenes(img)
    
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

tk.Button(frame_botones, text="Resumen", width=15, command=informacion).grid(row=0, column=0, padx=10)
tk.Button(frame_botones, text="Matriz Numérica", width=15, command=mostrar_matriz_correlacion).grid(row=0, column=1, padx=10)
tk.Button(frame_botones, text="Análisis Categórico", width=18, command=mostrar_categorico).grid(row=0, column=2, padx=10)
tk.Button(frame_botones, text="Agregar Muestra", width=15, command=agregar_nueva_muestra).grid(row=0, column=3, padx=10)


text_area = ScrolledText(ventana, width=70, height=30)
text_area.grid(row=1, column=1, padx=10, pady=10)

# Área para visualización de imágenes
frame_imagen = tk.Frame(ventana)
frame_imagen.grid(row=1, column=0, padx=10, pady=10)

image_label = tk.Label(frame_imagen)
image_label.grid(row=0, column=0, padx=10, pady=10)

ventana.mainloop()
