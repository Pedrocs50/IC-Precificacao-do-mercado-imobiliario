import streamlit as st
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
        colunas_numericas = ['rendimento', 'icc', 'ipca', 'desemprego', 'dolar', 'ibc-br', 'selic', 'igp-m', 'incc']
        for col in colunas_numericas:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False), errors='coerce')
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
        self.df['Data'] = pd.to_datetime(self.df['Data'], format='%Y.%m', errors='coerce')
        self.df_venda_aluguel['Data'] = pd.to_datetime(self.df_venda_aluguel['Data'], format='%b/%y', errors='coerce')
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
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(self.correlacao, annot=True, cmap='YlGnBu', fmt='.2f', ax=ax)
        plt.title('Mapa de Correlação de Variáveis Numéricas', fontsize=16)
        st.pyplot(fig)

# === Interface Streamlit ===

st.title("🔍 Análise de Correlação de Indicadores Econômicos e Imobiliários")

# Upload de arquivos
caminho_arquivo = 'data/processed/Dados-Unificados.csv'
caminho_venda_aluguel = 'data/processed/Preço-venda-aluguel.csv'

# Carregar dados
data_loader = DataLoader(caminho_arquivo, caminho_venda_aluguel)
df_completo = data_loader.combinar_dados()

# Mostrar preview dos dados
st.subheader("📄 Dados combinados")
st.dataframe(df_completo.head())

# Selecionar método de correlação
metodo = st.selectbox("Método de correlação", ['pearson', 'spearman', 'kendall'])

# Calcular e exibir heatmap
df_numerical = data_loader.selecionar_colunas_numericas(df_completo)
correlation_calculator = CorrelationCalculator(df_numerical)
correlacao = correlation_calculator.calcular_correlacao(metodo=metodo)

st.subheader("📊 Mapa de Correlação")
heatmap_generator = HeatmapGenerator(correlacao)
heatmap_generator.gerar_heatmap()
