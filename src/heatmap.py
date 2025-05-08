import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class DataLoader:
    """Classe para carregar e preparar os dados."""
    
    def __init__(self, caminho_arquivo, caminho_venda_aluguel):
        self.caminho_arquivo = caminho_arquivo
        self.caminho_venda_aluguel = caminho_venda_aluguel
        self.df = self.carregar_dados()
        self.df_venda_aluguel = self.carregar_venda_aluguel()

    def carregar_dados(self):
        """Carrega o arquivo CSV com dados econômicos e retorna um DataFrame."""
        df = pd.read_csv(self.caminho_arquivo, decimal=',')  
        return df

    def carregar_venda_aluguel(self):
        """Carrega o arquivo CSV com dados de venda e aluguel."""
        df = pd.read_csv(self.caminho_venda_aluguel, decimal=',')  
        return df

    def selecionar_colunas_numericas(self, df):
        """Seleciona apenas as colunas numéricas, removendo a coluna 'Data'."""
        df_numerico = df.select_dtypes(include=['float64', 'int64'])
        if 'Data' in df_numerico.columns:
            df_numerico = df_numerico.drop(columns='Data')  
        return df_numerico

    def combinar_dados(self):
        """Combina os dados econômicos com os dados de venda e aluguel."""
        # Ajuste da conversão de data
        self.df['Data'] = pd.to_datetime(self.df['Data'], format='%Y.%m', errors='coerce')
        self.df_venda_aluguel['Data'] = pd.to_datetime(self.df_venda_aluguel['Data'], format='%b/%y', errors='coerce')

        # Juntar os dois DataFrames pela coluna 'Data'
        df_completo = pd.merge(self.df, self.df_venda_aluguel, on='Data', how='inner')
        return df_completo


class CorrelationCalculator:
    """Classe para calcular a correlação entre variáveis numéricas."""
    
    def __init__(self, df):
        self.df = df

    def calcular_correlacao(self, metodo='spearman'):
        """Calcula a correlação entre as colunas numéricas."""
        return self.df.corr(method=metodo)


class HeatmapGenerator:
    """Classe para gerar o heatmap a partir da correlação."""
    
    def __init__(self, correlacao):
        self.correlacao = correlacao

    def gerar_heatmap(self):
        """Gera e exibe o heatmap da correlação."""
        plt.figure(figsize=(10, 8))
        sns.heatmap(self.correlacao, annot=True, cmap='YlGnBu', fmt='.2f')
        plt.title('Mapa de Correlação de Variáveis Numéricas', fontsize=16)
        plt.show()


# Fluxo do código
if __name__ == '__main__':
    # Caminhos para os arquivos CSV
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
