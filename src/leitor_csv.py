import pandas as pd

class LeitorCsv:
    def __init__(self, caminho):
        self._arquivo = caminho
        self._df = None

    def ler(self):
        self._df = pd.read_csv(self._arquivo, decimal=",", thousands=".")
        return self._df
