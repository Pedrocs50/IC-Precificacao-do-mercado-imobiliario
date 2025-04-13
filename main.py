from src.leitor_csv import LeitorCsv
from src.analise_dados import AnaliseDados

def main():
    leitor = LeitorCsv("data/processed/Preço-venda-aluguel.csv")
    df = leitor.ler()

    print("\nGRÁFICO DE PREÇOS DE VENDAAS E  ALUGUEIS POR METRO QUADRADO (R$/m²)")
    print("POSSÍVEIS COLUNAS A SEREM AVALIADA:")
    opcoes_colunas =  {
        1: 'venda',
        2: 'venda_1D',
        3: 'venda_2D',
        4: 'venda_3D',
        5: 'venda_4D',
        6: 'aluguel',
        7: 'aluguel_1D',
        8: 'aluguel_2D',
        9: 'aluguel_3D',
        10: 'aluguel_4D'
    }

    for k, v in opcoes_colunas.items():
        print(f"{k}. {v}")

    while True:
        try:
            escolha = int(input("\nQual coluna gostaria de visualizar? (1-10): "))
            if escolha in opcoes_colunas:
                coluna_avaliar = opcoes_colunas[escolha]
                break
            else:
                print("Digite um número entre 1 e 10: ")

        except ValueError:
            print("Por favor, digite um número válido.")

    print(f"Você escolheu a coluna: {coluna_avaliar}")

    analise = AnaliseDados(df)
    analise.criar_grafico(coluna_avaliar)

if __name__ == "__main__":
    main()
