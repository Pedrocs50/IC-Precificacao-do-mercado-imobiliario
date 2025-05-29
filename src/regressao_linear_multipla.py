import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


class DataLoader:
    def __init__(self, path_venda_aluguel, path_macro):
        self.path_venda_aluguel = path_venda_aluguel
        self.path_macro = path_macro
        self.mes_pt_en = {
            "jan": "Jan", "fev": "Feb", "mar": "Mar", "abr": "Apr",
            "mai": "May", "jun": "Jun", "jul": "Jul", "ago": "Aug",
            "set": "Sep", "out": "Oct", "nov": "Nov", "dez": "Dec"
        }

    def carregar_dados(self):
        df_venda_aluguel = pd.read_csv(self.path_venda_aluguel, decimal=",")
        df_macro = pd.read_csv(self.path_macro, decimal=",")

        # Corrigir meses para inglês no df_venda_aluguel
        for pt, en in self.mes_pt_en.items():
            df_venda_aluguel["Data"] = df_venda_aluguel["Data"].str.replace(pt, en, regex=False)

        # Corrigir ano (ex: /08 → /2008)
        df_venda_aluguel["Data"] = df_venda_aluguel["Data"].str.replace(r"/(\d{2})$", r"/20\1", regex=True)

        # Converter para datetime
        df_venda_aluguel["Data"] = pd.to_datetime(df_venda_aluguel["Data"], format="%b/%Y")
        df_macro["Data"] = pd.to_datetime(df_macro["Data"], format="%Y.%m")

        # Mesclar DataFrames
        df = pd.merge(df_venda_aluguel, df_macro, on="Data", how="inner")

        return df

    def preparar_variaveis(self, df, alvo="venda"):
        # Seleciona y e X
        y = df[alvo]
        X = df[["ipca", "desemprego", "dolar", "selic", "igp-m", "incc", "rendimento"]]

        # Normalizar números que usam vírgula como decimal e ponto como milhar
        def normaliza_coluna(col):
            col = col.astype(str).str.replace(".", "", regex=False)
            col = col.str.replace(",", ".", regex=False)
            return pd.to_numeric(col, errors="coerce")

        X = X.apply(normaliza_coluna)
        y = normaliza_coluna(y)

        # Remover linhas com valores NaN em X ou y
        mask_validos = X.notnull().all(axis=1) & y.notnull()
        X = X.loc[mask_validos]
        y = y.loc[mask_validos]
        df = df.loc[mask_validos]

        return df, X, y


class Regressor:
    def __init__(self):
        self.modelo = LinearRegression()

    def treinar(self, X, y):
        self.modelo.fit(X, y)

    def prever(self, X):
        return self.modelo.predict(X)

    def avaliar(self, y_true, y_pred):
        r2 = r2_score(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        return r2, rmse

    def coeficientes(self, colunas):
        return pd.Series(self.modelo.coef_, index=colunas)


class Plotter:
    def __init__(self, df, y_true, y_pred):
        self.df = df
        self.y_true = y_true
        self.y_pred = y_pred

    def plotar(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.df["Data"], self.y_true, label="Real", marker="o")
        plt.plot(self.df["Data"], self.y_pred, label="Predito", marker="x")
        plt.xlabel("Data")
        plt.ylabel("Preço de Venda")
        plt.title("Regressão Linear Múltipla - Preço de Venda")
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    # Caminhos dos arquivos
    caminho_venda_aluguel = "data/processed/Preço-venda-aluguel.csv"
    caminho_macro = "data/processed/Dados-Unificados.csv"

    # Carregar e preparar dados
    loader = DataLoader(caminho_venda_aluguel, caminho_macro)
    df = loader.carregar_dados()
    df, X, y = loader.preparar_variaveis(df, alvo="venda")  # ou alvo="aluguel"

    # Treinar modelo
    reg = Regressor()
    reg.treinar(X, y)

    # Prever e avaliar
    y_pred = reg.prever(X)
    r2, rmse = reg.avaliar(y, y_pred)

    print(f"R²: {r2:.2f}")
    print(f"RMSE: {rmse:.2f}")

    print("\nCoeficientes da regressão:")
    print(reg.coeficientes(X.columns))

    # Plotar resultados
    plotter = Plotter(df, y, y_pred)
    plotter.plotar()
