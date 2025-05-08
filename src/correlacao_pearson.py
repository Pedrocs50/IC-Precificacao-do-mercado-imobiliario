import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class CorrelacaoPearson:
    def __init__(self, caminho_dados_economicos, caminho_venda_aluguel):
        self.caminho_dados_economicos = caminho_dados_economicos
        self.caminho_venda_aluguel = caminho_venda_aluguel
        self.df = self._carregar_e_preparar_dados()

    def _carregar_e_preparar_dados(self):
        # carregando os dados
        df_economico = pd.read_csv(self.caminho_dados_economicos, decimal=',')
        df_venda_aluguel = pd.read_csv(self.caminho_venda_aluguel, decimal=',')

        # Convertendo datas
        df_economico['Data'] = pd.to_datetime(df_economico['Data'], format='%Y.%m', errors='coerce')
        df_venda_aluguel['Data'] = pd.to_datetime(df_venda_aluguel['Data'], format='%b/%y', errors='coerce')

        # Unindo os dados
        df = pd.merge(df_economico, df_venda_aluguel, on='Data', how='inner')
        return df

    def obter_colunas_numericas(self):
        return self.df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    def calcular_e_plotar_correlacao(self, var1, var2):
        correlacao = self.df[[var1, var2]].corr(method='pearson').iloc[0, 1]
        print(f"\n📈 Correlação de Pearson entre '{var1}' e '{var2}': {correlacao:.4f}")

        plt.figure(figsize=(8, 6))
        sns.regplot(x=var1, y=var2, data=self.df, line_kws={"color": "red"})
        plt.title(f"Dispersão entre {var1} e {var2} (r = {correlacao:.2f})")
        plt.xlabel(var1)
        plt.ylabel(var2)
        plt.grid(True)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    caminho_dados = "data/processed/Dados-Unificados.csv"
    caminho_venda_aluguel = "data/processed/Preço-venda-aluguel.csv"

    correlacao = CorrelacaoPearson(caminho_dados, caminho_venda_aluguel)
    colunas = correlacao.obter_colunas_numericas()

    print("\n🔢 Variáveis disponíveis para correlação:")
    for i, col in enumerate(colunas):
        print(f"{i + 1}. {col}")

    try:
        indice1 = int(input("\nDigite o número da 1ª variável: ")) - 1
        indice2 = int(input("Digite o número da 2ª variável: ")) - 1

        var1 = colunas[indice1]
        var2 = colunas[indice2]

        correlacao.calcular_e_plotar_correlacao(var1, var2)
    except (IndexError, ValueError):
        print("\n❌ Entrada inválida. Certifique-se de digitar números válidos.")
