import pandas as pd 
import matplotlib.pyplot as plt # Carregar o arquivo CSV 
import numpy as np
from scipy.signal import find_peaks

file_path = '/home/kamy/Desktop/graficos-antenas/LACAP02-B.csv' # Substitua pelo caminho do seu arquivo 
data = pd.read_csv(file_path) # A primeira coluna é a frequência 
frequencia = data.iloc[:, 0] # As demais colunas são os valores do eixo x 
valores_x = data.iloc[:, 1:] # Plotar cada coluna de valores x contra a frequência 

freqRess = []
s11Ress = []
BW = []
figuras = []

j = 0

def gerarGrafico(j):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_facecolor("#FFFFFF") 
    #plt.subplots_adjust(right=0.97, top=0.97)
    plt.plot(frequencia, valores_x[coluna], label=coluna, color = 'r') 
    plt.xlabel('Frequência') 
    plt.ylabel('dB') 
    plt.title(f'Gráfico de {coluna} vs Frequência') 
    plt.grid(color = 'gray', linestyle = '-', linewidth = 0.15)
    plt.savefig(f'Gráfico de {coluna} vs Frequência_'+ str(j)+'.png' ,format='png')
    return 0

# def encontrar_minimo_intervalo(coluna, limite=-10.0): # Extrair a coluna de valores do eixo x 
#     valores_y = valores_x[coluna] # Inicializar variáveis 
#     intervalo_iniciado = False 
#     menor_valor = None  
#     i = 0
#     indice = 0
#     bw_1 = 0
#     bw_2 = 0
#     for valor in valores_y:        
#         if valor < limite and not intervalo_iniciado: 
#             intervalo_iniciado = True # O intervalo começa quando o valor cai abaixo de -10 
#             menor_valor = valor # Inicializa o menor valor com o primeiro valor do intervalo 
#             # indice = valor.idx()
#             if bw_1 == 0: bw_1 = i-1
#         elif intervalo_iniciado:
#             if valor < menor_valor: 
#                 menor_valor = valor # Atualiza o menor valor se encontrar um valor menor 
#                 indice = i
#             if valor >= limite: 
#                 bw_2 = i
#                 break # Termina o intervalo quando o valor sobe novamente acima de -10 
#         i+=1
#         # print(i)
#     bw_final = frequencia[bw_2] - frequencia[bw_1] 
#     if menor_valor!= None: return f"{menor_valor: .5f}", frequencia[i-1], bw_final
#     else: return menor_valor, None, None

def encontrar_minimo_intervalo(coluna, limite=-10.0):
    valores_y = valores_x[coluna].values 
    frequencias = frequencia.values  

    intervalo_iniciado = False
    menor_valor = None
    indice_menor_valor = None
    i_inicio = 0
    i_fim = 0

    for i, valor in enumerate(valores_y):
        if valor < limite and not intervalo_iniciado:
            intervalo_iniciado = True
            if i_inicio == 0: i_inicio = i-1
            menor_valor = valor
            indice_menor_valor = i
        elif intervalo_iniciado:
            if valor < menor_valor:
                menor_valor = valor
                indice_menor_valor = i
            if valor >= limite:
                i_fim = i
                break

    if intervalo_iniciado and i_fim == 0:
        i_fim = len(valores_y) - 1

    # if intervalo_iniciado and menor_valor is not None:
    #     bw_final = frequencias[i_fim] - frequencias[i_inicio]
    #     return f"{menor_valor:.5f}", frequencias[indice_menor_valor], bw_final
    # else:
    #     return None, None, None
    if intervalo_iniciado and menor_valor is not None:
        bw_final = frequencias[i_fim] - frequencias[i_inicio]
        return bw_final
    else:
        return None

def formatar_lista_em_string(lista):
    return ', '.join(map(str, lista)) if lista else 'Nenhum'

def EncontrarFreqRessonancia(limite=-10.0):
    # Invertir los valores en la columna seleccionada
    frequencias_ressonancia = []
    ganho = []
    y_invertido = -valores_x[coluna].values
    
    # Encontrar picos en los datos invertidos
    vales, _ = find_peaks(y_invertido)
    # print(vales) 
    # Filtrar los picos que cumplen con el límite
    for i in vales:
        frequencias_ressonancia1 = frequencia[i] # if -y_invertido[i] <= limite else None
        frequencias_ressonancia.append(frequencias_ressonancia1)
        ganho.append(f"{-y_invertido[i]:.5f}")

    return frequencias_ressonancia, ganho if frequencias_ressonancia else None

for coluna in valores_x.columns: 
    # gerarGrafico(j)
    ress,s11 = EncontrarFreqRessonancia()
    bw_local = encontrar_minimo_intervalo(coluna)
    freqRess.append(formatar_lista_em_string(ress))
    s11Ress.append(formatar_lista_em_string(s11))
    BW.append(bw_local)
    figuras.append({coluna}) 
    j+=1

df = pd.DataFrame({'Gráfico': figuras, 'frequência de ressonância': freqRess, 'S11': s11Ress, 'BW': BW}) # Salvar o DataFrame em um arquivo .csv 
file_path = 'analise-antenas-B.csv' # Substitua pelo caminho onde deseja salvar o arquivo 
df.to_csv(file_path, index=False) 