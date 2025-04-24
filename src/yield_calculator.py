import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import mplcursors

class Yield:
    def __init__(self, df, aluguel_coluna, venda_coluna):
        self._df = df
        self.aluguel_coluna = aluguel_coluna
        self.venda_coluna = venda_coluna

    def calcular_yield(self):
        if self._df is None or self._df.empty:
            print("Erro: Necessário que um arquivo seja lido para criar o gráfico.")
            return
        
        self._df[self.aluguel_coluna] = pd.to_numeric(self._df[self.aluguel_coluna], errors='coerce')
        self._df[self.venda_coluna] = pd.to_numeric(self._df[self.venda_coluna], errors='coerce')

        # CALCULANDO O ALUGUEL ANUAL
        self._df['aluguel_anual'] = self._df[self.aluguel_coluna] * 12

        # CALCULANDO O YIELD
        self._df['yield'] = self._df['aluguel_anual'] / self._df[self.venda_coluna] / 10 # GAMBIARRA, OU SEJA, TENHO QUE AJUSTAS OS DADOS, OU MELHORAR A FORMA DE CHAMRA OS DADOS NO ARQUIVO EXCEL.

        print(f"Coluna de venda escolhida: {self.venda_coluna}")
        print(f"Coluna de venda escolhida: {self.aluguel_coluna}")
        pd.set_option('display.max_rows', None)
        print(f"Todas as linhas dos dados calculados de yield:\n{self._df[['Data', self.venda_coluna, self.aluguel_coluna, 'yield']].round(2)}")

        plt.figure(figsize=(12, 6))
        plt.plot(self._df["Data"], self._df['yield'], color="green")
        plt.xlabel("Data")
        plt.ylabel("Yield (Aluguel / Venda)")
        plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100))
        plt.title(f"Gráfico de Yield entre {self.aluguel_coluna} e {self.venda_coluna}")
        plt.xticks(np.arange(0, len(self._df), step=5), rotation=50, fontsize=10)

        mplcursors.cursor(hover=True)

        plt.show()
