
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg
from PIL import Image

# Función auxiliar para convertir figura matplotlib a imagen PIL
def fig_to_pil(fig):
    buf = io.BytesIO()
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    canvas.print_png(buf)
    buf.seek(0)
    return Image.open(buf)

class DataAnalyzer:
    def __init__(self, data):
        self.df = data
        self.categorical_analisis_cols = data.select_dtypes(include='object').columns
        self.numeric_cols = data.select_dtypes(include=np.number).columns

    def summary(self):
        buffer = io.StringIO()
        self.df.info(buf=buffer)
        salida_info = buffer.getvalue()
        salida_describe = self.df.describe().to_string()
        salida = salida_info + "\n\n" + salida_describe
        return salida

    def missing_values(self):
        return self.df.isnull()

    def imprimir(self):
        print("Hola")

    def correlation_matrix(self):
        corr = self.df[self.numeric_cols].corr()
        fig, ax = plt.subplots()
        sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
        ax.set_title('Matriz de Correlación')
        return fig_to_pil(fig)

    def categorical_analisis(self):
        print(f"Las columnas categóricas son: {self.categorical_analisis_cols}")
        column = input("Digite la columna a visualizar: ")
        if column in self.categorical_analisis_cols:
            fig, ax = plt.subplots()
            sns.countplot(data=self.df, x=column, order=self.df[column].value_counts().index, ax=ax)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
            ax.set_title(f'Análisis de: {column}')
            return fig_to_pil(fig)
        else:
            print("Columna no válida.")
            return None

    def categorical_analisis_col(self, column):
        if column in self.categorical_analisis_cols:
            fig, ax = plt.subplots()
            sns.countplot(data=self.df, x=column, order=self.df[column].value_counts().index, ax=ax)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
            ax.set_title(f'Análisis de: {column}')
            return fig_to_pil(fig)
        else:
            print("Columna no válida.")
            return None
