import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class DataLoader:    
    def __init__(self, caminho_arquivo, caminho_venda_aluguel):
        self.caminho_arquivo = caminho_arquivo
        self.caminho_venda_aluguel = caminho_venda_aluguel
        self.df = self.carregar_dados()
        self.df_venda_aluguel = self.carregar_venda_aluguel()

    def carregar_dados(self):
        df = pd.read_csv(self.caminho_arquivo, decimal=',')  
        # converter colunas numéricas que podem estar como string por causa do decimal
        colunas_numericas = ['rendimento', 'icc', 'ipca', 'desemprego', 'dolar', 'ibc-br', 'selic', 'igp-m', 'incc']
        for col in colunas_numericas:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace('.', '').str.replace(',', '.'), errors='coerce')
        return df


    def carregar_venda_aluguel(self):
        df = pd.read_csv(self.caminho_venda_aluguel, decimal=',')  
        return df

    def selecionar_colunas_numericas(self, df):
        df_numerico = df.select_dtypes(include=['float64', 'int64'])
        if 'Data' in df_numerico.columns:
            df_numerico = df_numerico.drop(columns='Data')  
        return df_numerico

    def combinar_dados(self):
        # Ajuste da conversão de data
        self.df['Data'] = pd.to_datetime(self.df['Data'], format='%Y.%m', errors='coerce')
        self.df_venda_aluguel['Data'] = pd.to_datetime(self.df_venda_aluguel['Data'], format='%b/%y', errors='coerce')

        # Juntar os dois DataFrames pela coluna 'Data'
        df_completo = pd.merge(self.df, self.df_venda_aluguel, on='Data', how='inner')
        return df_completo


class CorrelationCalculator:
    
    def __init__(self, df):
        self.df = df

    def calcular_correlacao(self, metodo='spearman'):
        return self.df.corr(method=metodo)


class HeatmapGenerator:
    
    def __init__(self, correlacao):
        self.correlacao = correlacao

    def gerar_heatmap(self):
        plt.figure(figsize=(10, 8))
        sns.heatmap(self.correlacao, annot=True, cmap='YlGnBu', fmt='.2f')
        plt.title('Mapa de Correlação de Variáveis Numéricas', fontsize=16)
        plt.show()


# fluxo do código
if __name__ == '__main__':
    # caminhos para os arquivos
    caminho_arquivo = 'data/processed/Dados-Unificados.csv' 
    caminho_venda_aluguel = 'data/processed/Preço-venda-aluguel.csv'  

    # Carregar e preparar os dados
    data_loader = DataLoader(caminho_arquivo, caminho_venda_aluguel)
    df_completo = data_loader.combinar_dados()

    # Selecionar as colunas numéricas para análise
    df_numerical = data_loader.selecionar_colunas_numericas(df_completo)

    # Calcular a correlação
    correlation_calculator = CorrelationCalculator(df_numerical)
    correlacao = correlation_calculator.calcular_correlacao(metodo='spearman')

    # Gerar e exibir o heatmap
    heatmap_generator = HeatmapGenerator(correlacao)
    heatmap_generator.gerar_heatmap()
