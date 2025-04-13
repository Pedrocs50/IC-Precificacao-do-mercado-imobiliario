import matplotlib.pyplot as plt
import numpy as np
import mplcursors

class AnaliseDados:
    def __init__(self, df):
        self._df = df

    def criar_grafico(self, coluna_avaliar):
        plt.figure(figsize=(12, 6))
        plt.plot(self._df["Data"], self._df[coluna_avaliar], color="blue")
        plt.xticks(np.arange(0, len(self._df), step=5), rotation=50, fontsize=10)
        mplcursors.cursor(hover=True)
        plt.xlabel("Data")
        plt.ylabel(f"{coluna_avaliar} por m²")
        plt.title("Gráfico de Linhas")
        plt.show()
