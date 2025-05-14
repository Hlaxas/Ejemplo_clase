# Librerías necesarias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
from Analisis import DataAnalyzer

data = pd.read_csv('adult.csv') #Puedo colocar la ruta del archivo .csv o de otro archivo .csv
analizar = DataAnalyzer(data)
info = analizar.summary()
def informacion():
    try:
        text_area.delete('1.0', tk.END)  # Limpiar el área de texto antes de mostrar la nueva información
        info = analizar.summary()
        text_area.insert(tk.END, info)
    except:
        messagebox.showerror("Error", "No se pudo obtener la información del DataFrame.")
        
        
ventana = tk.Tk()
ventana.title("Análisis de Datos")

boton_summary = tk.Button(ventana, text="Información del DataFrame", command= informacion )
boton_summary.pack()

text_area = ScrolledText(ventana, width=100, height=30)
text_area.pack()
ventana.mainloop()