import pandas as pd 
import matplotlib.pyplot as plt # Carregar o arquivo CSV 

file_path = '/home/kamy/Desktop/graficos-antenas/LACAP01-A.csv' # Substitua pelo caminho do seu arquivo 
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

def encontrar_minimo_intervalo(coluna, limite=-10.0): # Extrair a coluna de valores do eixo x 
    valores_y = valores_x[coluna] # Inicializar variáveis 
    intervalo_iniciado = False 
    menor_valor = None  
    i = 0
    indice = 0
    bw_1 = 0
    bw_2 = 0
    for valor in valores_y:        
        if valor < limite and not intervalo_iniciado: 
            intervalo_iniciado = True # O intervalo começa quando o valor cai abaixo de -10 
            menor_valor = valor # Inicializa o menor valor com o primeiro valor do intervalo 
            indice = i
            if bw_1 == 0: bw_1 = i-1
        elif intervalo_iniciado:
            if valor < menor_valor: 
                menor_valor = valor # Atualiza o menor valor se encontrar um valor menor 
                indice = i
            if valor >= limite: 
                bw_2 = i
                break # Termina o intervalo quando o valor sobe novamente acima de -10 
        i+=1
        # print(i)
    bw_final = frequencia[bw_2] - frequencia[bw_1] 
    if menor_valor!= None: return f"{menor_valor: .5f}", frequencia[i], bw_final
    else: return menor_valor, None, None



for coluna in valores_x.columns: 
    gerarGrafico(j)
    s11,ress, bw_local= encontrar_minimo_intervalo(coluna)
    freqRess.append(ress)
    s11Ress.append(s11)
    BW.append(bw_local)
    figuras.append({coluna}) 
    j+=1

df = pd.DataFrame({'Gráfico': figuras, 'frequência de ressonância': freqRess, 'S11': s11Ress, 'BW': BW}) # Salvar o DataFrame em um arquivo .csv 
file_path = 'analise-antenas-A.csv' # Substitua pelo caminho onde deseja salvar o arquivo 
df.to_csv(file_path, index=False) 