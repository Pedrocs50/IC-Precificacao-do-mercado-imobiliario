from src.leitor_csv import LeitorCsv
from src.analise_dados import AnaliseDados
from src.yield_calculator import Yield  

def menu_colunas():
    opcoes_colunas = {
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
            escolha = int(input("\nEscolha uma coluna (1-10): "))
            if escolha in opcoes_colunas:
                return opcoes_colunas[escolha]
            else:
                print("Digite um número entre 1 e 10.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

def main():
    leitor = LeitorCsv("data/processed/Preço-venda-aluguel.csv")
    df = leitor.ler()

    print("SISTEMA DE PRECIFICAÇÃO DO MERCADO IMOBILIÁRIO")

    while True:
        print("\nMenu:")
        print("1. Visualizar gráfico de preços")
        print("2. Calcular e visualizar gráfico de Yield")
        print("3. Sair")

        opcao = input("Escolha uma opção (1-3): ")

        if opcao == "1":
            print("\nGráfico de preços de venda e aluguel por m²")
            print("Escolha a coluna que deseja visualizar:")
            coluna = menu_colunas()
            print(f"Você escolheu a coluna: {coluna}")
            analise = AnaliseDados(df)
            analise.criar_grafico(coluna)

        elif opcao == "2":
            print("\nCálculo do Yield")
            print("Escolha a coluna de ALUGUEL:")
            aluguel_col = menu_colunas()

            print("\nEscolha a coluna de VENDA:")
            venda_col = menu_colunas()

            yield_calc = Yield(df, aluguel_col, venda_col)
            yield_calc.calcular_yield()

        elif opcao == "3":
            print("Saindo do programa. Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
