import matplotlib.pyplot as plt
from datetime import datetime
import calendar

def leArquivo():
    arq = open("Anexo_Arquivo_Dados_Projeto_Logica_e_programacao_de_computadores.csv", "r")
    primeiraLinha = arq.readline()
    colunas = primeiraLinha[:-1].split(',')  # :-1 para tirar o \n que tem no final

    dados = []
    for linha in arq:
        valores = [val for val in linha.split(',')]
        for i in range(1, len(valores)):
          valores[i] = float(valores[i])
        dados.append(valores)

    return colunas, dados


def exibeDados(dados, colunas): # incluir cabeçalho
    print(" \n* Aqui serão exibidos dados do arquivo\n* Você deve informar mês/ano inicial e final")

    mesAnoInicial = input("\n -> Digite o mês e ano inicial (MM/AAAA): ")
    mesAnoFinal = input("\n -> Digite o mês e ano final (MM/AAAA): ")

    opcao = int(input("\nVocê deseja ver:\n 1 - Todos os dados\n 2 - Apenas precipitação\n 3 - Apenas temperatura\n 4 - Apenas umidade e vento\n"))
    while opcao != 1 and opcao != 2 and opcao != 3 and opcao != 4:
        print("\n ! Opção inválida. Tente novamente. !")
        opcao = int(input("\nVocê deseja ver:\n 1 - Todos os dados\n 2 - Apenas precipitação\n 3 - Apenas temperatura\n 4 - Apenas umidade e vento\n"))

    dataInicialStr = f"01/{mesAnoInicial}"
    dataFinalStr = f"{calendar.monthrange(int(mesAnoFinal.split('/')[1]), int(mesAnoFinal.split('/')[0]))[1]:02d}/{mesAnoFinal}"

    dataInicial = datetime.strptime(dataInicialStr, "%d/%m/%Y")
    dataFinal = datetime.strptime(dataFinalStr, "%d/%m/%Y")

    print()
    colunas = formataColunas(colunas)
    if opcao == 1:
        for i in range(len(colunas)):
            if i+1 == len(colunas):  # Caso o indice + 1 for igual ao tamanho das colunas, não vai adicionar o " - " no final
                print(colunas[i])
            else:
                print(colunas[i], end=" - ")
    elif opcao == 2:
        print(colunas[0], end=" - ")
        print(colunas[1])
    elif opcao == 3:
        print(colunas[0], end=" - ")
        print(colunas[2], end=" - ")
        print(colunas[3], end=" - ")
        print(colunas[5], end=" - ")
    else:
        print(colunas[0], end=" - ")
        print(colunas[6], end=" - ")
        print(colunas[7], end=" - ")   # Arredondar velocidade do vento para duas casas decimais
    print()

    for dado in dados:
        dataStr = dado[0]
        data = datetime.strptime(dataStr, "%d/%m/%Y")
        if data >= dataInicial and data <= dataFinal:
            if opcao == 1:                    # Todos os dados
                for i in range(len(dado)):
                    if i+1 == len(dado):
                        print(dado[i])
                    else: 
                        print(dado[i], end=" - ")
            elif opcao == 2:                  # Precipitação
                print(dataStr, end=" - ")
                print(dado[1])
            elif opcao == 3:                  # Temperatura Máxima, Mínima e Média
                print(dataStr, end=" - ")
                print(dado[2], end=" - ")
                print(dado[3], end=" - ")
                print(dado[5])
            else:                             # Umidade Relativa e Velocidade do Vento
                print(dataStr, end=" - ")
                print(dado[6], end=" - ")
                print(dado[7])
            print()


def mesMenosChuvoso(dados):
    menorPrecipitacao = float('inf')      # Inicializa com um valor infinito
    mesAnoMenorPrecipitacao = None

    cont = 0
    for dado in dados:
        data = dado[0]
        precipitacao = float(dado[1])
        if precipitacao < menorPrecipitacao:
            data = data.split("/")
            mesAno = data[1] + "/" + data[2]
            menorPrecipitacao = precipitacao
            mesAnoMenorPrecipitacao = mesAno
        if precipitacao == menorPrecipitacao:
            cont = cont + 1

    mensagem = {
        'mesAno': mesAnoMenorPrecipitacao,
        'menorPrecipitacao': menorPrecipitacao,
        'cont': cont,
        'mensagem': f" --> O mês/ano com menor precipitação foi {mesAnoMenorPrecipitacao} com {menorPrecipitacao} mm de precipitação."
    }

    return mensagem


def mediaTempMinima(dados, mes):
    tempMinimaMes = {}
    
    for dado in dados:
        data = dado[0]
        ano = int(data.split("/")[2])
        mes_dado = int(data.split("/")[1])
        temperaturaMinima = dado[3]

        if mes_dado == mes and (ano >= 2006 and ano <= 2016):
            if ano not in tempMinimaMes:
                tempMinimaMes[ano] = []
            tempMinimaMes[ano].append(temperaturaMinima)

    if not tempMinimaMes:
        return None

    mediaMes = {}
    for ano, temperaturas in tempMinimaMes.items():
        mediaMes[ano] = sum(temperaturas) / len(temperaturas)

    return mediaMes


def criaGrafico(registros, mesInformado):
    dados = mediaTempMinima(registros, mesInformado)
    anos = list(dados.keys())
    medias = list(dados.values())

    plt.bar(anos, medias)
    plt.xlabel("Ano")
    plt.ylabel("Média da Temperatura Mínima")
    plt.title(f"Média da Temperatura Mínima para o mês {mesInformado}")
    plt.show()

def obterNomeMes(numMes):
    meses = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    if 1 <= numMes <= 12:
        return meses[numMes - 1]
    else:
        return "Mês inválido"


def formataColunas(colunas):
    coluna_dict = {
        "data": "Data",
        "precip": "Precipitação",
        "maxima": "Temperatura Máxima",
        "minima": "Temperatura Mínima",
        "horas_insol": "Horas Insol",
        "temp_media": "Temperatura Média",
        "um_relativa": "Umidade Relativa",
        "vel_vento": "Velocidade do Vento"
    }

    newColunas = [coluna_dict.get(coluna, coluna) for coluna in colunas]
    return newColunas


colunas, dados = leArquivo()
colunas = formataColunas(colunas)
opcao = -1
while opcao != 0:
    print("\n0 - Sair")
    print("1 - Exibe dados")
    print("2 - Mês menos chuvoso")
    print("3 - Média da temperatura mínima de um determinado mês (2006 a 2016)")
    print("4 - Gráfico com as médias de temperatura mínima de um determinado mês (2006 a 2016)")
    opcao = int(input("Digite a opção desejada: "))

    if opcao == 0:
        print("\nFim do programa...")
        break

    elif opcao == 1:
        exibeDados(dados, colunas)
    
    elif opcao == 2:
        resultado = mesMenosChuvoso(dados)
        print("\n" + resultado['mensagem'])
        if (resultado['cont'] > 0):
            print(f" --> Houveram outras {resultado['cont']} ocorrências dessa mesma precipitação entre os anos de 1961 e 2016.")
    
    elif opcao == 3:
        mesInformado = int(input("Digite o número do mês (1-12): "))
        while mesInformado < 1 and mesInformado > 12:
            print("Entrada inválida! Tente novamente.")
            mesInformado = int(input("Digite o número do mês (1-12): "))
        
        mediaMes = mediaTempMinima(dados, mesInformado)
        if mediaMes is not None:
            mesInformado = obterNomeMes(mesInformado)
            print()
            print(f" * A média da temperatura mínima para o mês de {mesInformado} é:")
            cont = 0
            soma = 0
            for ano, media in mediaMes.items():
                print(f"  -> {mesInformado}/{ano}: {media:.2f}")
                soma = soma + media
                cont = cont + 1
            print(f" * Média geral da temperatura mínima: {(soma/cont):.2f}")
    
    elif opcao == 4:
        mesInformado = int(input("Digite o número do mês (1-12): "))
        while mesInformado < 1 and mesInformado > 12:
            print("Entrada inválida! Tente novamente.")
            mesInformado = int(input("Digite o número do mês (1-12): "))
    
        criaGrafico(dados, mesInformado)

    else:
        print("\n ! Opção inválida. Tente novamente. ! \n")
