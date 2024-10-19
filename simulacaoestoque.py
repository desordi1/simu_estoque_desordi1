import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def fCustoTotal(q_values, n, DemandaDiaria, Frete, CustoDia):
    """
Calcula o custo total do estoque, estocagem e frete baseado em diferentes quantidades de lotes iniciais.

Parâmetros:
q_values : list[int]
    Lista de quantidades/valores de cada lote para testar.
n : int
    Número total de dias(período) para o cálculo do estoque.
DemandaDiaria : int
    Quantidade diária(p/ período) de produto demandado.
Frete : float
    Custo de frete por lote.
CustoDia : float
    Custo diário de manter uma unidade em estoque.
    
Retorna:
df : pandas.DataFrame
    DataFrame contendo as quantidades testadas e seus respectivos custos totais, custos de estocagem e custos de frete.
"""
    resultados = []

    for q in q_values:
        Estoque = np.zeros(n)
        Lote = q
        Estoque[0] = Lote
        k = 1
        for i in range(1, n):
            Estoque[i] = Estoque[i - 1] - DemandaDiaria
            if Estoque[i] < DemandaDiaria:
                Estoque[i] = Estoque[i] + Lote
                k += 1
        Estocagem = CustoDia * Estoque
        CustoTotal = Estocagem.sum() + k*Frete
        resultado = {
            'Quantidade': q,
            'CustoTotal': CustoTotal,
            'Estocagem': Estocagem.sum(),
            'Frete': k*Frete
        }
        resultados.append(resultado)

    df = pd.DataFrame(resultados)
    return df

def fGraficoEstoque (q_values, n, DemandaDiaria):
    """
Plota o gráfico baseado em diferentes quantidades de lotes iniciais, dias e Demanda.

Parâmetros:
q_values : list[int]
    Lista de quantidades/valores de cada lote para testar.
n : int
    Número total de dias(período) para o cálculo do estoque.
DemandaDiaria : int
    Quantidade diária(p/ período) de produto demandado.

"""
    Dia = np.arange(1,n+1)
    for q in q_values:
        Estoque = np.zeros(n)
        Lote = q
        Estoque[0] = q
        k = 1
        for i in range(1, n):
            Estoque[i] = Estoque[i - 1] - DemandaDiaria
            if Estoque[i] < DemandaDiaria:
                Estoque[i] = Estoque[i] + Lote
                k = k + 1
        plt.figure()
        plt.bar(Dia, Estoque)
        plt.xlabel('Dia')
        plt.ylabel('Estoque')
        plt.title(f'Gráfico de Estoque para q = {q}')
        plt.show()

def fGraficoEstocagem (q_values, n, DemandaDiaria, CustoDia):
    """
Plota o gráfico de estocagem baseado em diferentes quantidades de lotes iniciais.

Parâmetros:
q_values : list[int]
    Lista de quantidades/valores de cada lote para testar.
n : int
    Número total de dias(período) para o cálculo do estoque.
DemandaDiaria : int
    Quantidade diária(p/ período) de produto demandado.
CustoDia : float
    Custo diário de manter uma unidade em estoque.
    
Retorna:
Gráfico:
    gráfico de estocagem.
"""
    Dia = np.arange(1,n+1)
    for q in q_values:
        Estoque = np.zeros(n)
        Lote = q
        Estoque[0] = q
        k = 1
        for i in range(1, n):
            Estoque[i] = Estoque[i - 1] - DemandaDiaria
            if Estoque[i] < DemandaDiaria:
                Estoque[i] = Estoque[i] + Lote
                k += 1
        Estocagem = CustoDia * Estoque
        plt.figure()
        plt.bar(Dia, Estocagem, color = 'red')
        plt.xlabel('Dia')
        plt.ylabel('Estocagem')
        plt.title(f'Gráfico de Custo de Estocagem para q = {q}')
        plt.show()
        
def fLoteEconomico (DemandaTotal, Frete, CustoEstocagemTotal):
    """
Calcula o custo total do estoque, estocagem e frete baseado em diferentes quantidades de lotes iniciais.

Parâmetros:
    
 - DemandaTotal (float): Lista de quantidades/valores de cada lote para testar.
    
 - Frete (float): Custo de frete por lote.
 
 - CustoEstocagemTotal (float): Custo Total de Estocagem (pro período todo).
    
Retorna:
    - q (float): Retorna o valor da quantidade que minimiza os custos de estoque.
"""
    from numpy import sqrt
    q=sqrt((2*Frete*DemandaTotal)/CustoEstocagemTotal)
    return q

def fPerdaTotal(q, n, PrecoExcesso, PrecoFalta, p0, p1, x01, p2, p3, x23, p4, p5, x45):
    """
Calcula o total de perdas financeiras com base na quantidade disponível e na demanda em diferentes períodos.

Parâmetros:
    
- q (float): Quantidade de estoque disponível/médio.

- n (int): Número total de períodos a serem analisados.

- PrecoExcesso (float): Perda por unidade de excesso de estoque.

- PrecoFalta (float): Perda por unidade de falta de estoque.

- p0 (int): Índice inicial do intervalo de demanda baixa.

- p1 (int): Índice final do intervalo de demanda baixa.

- x01 (float): Valor da demanda nos períodos de demanda baixa.

- p2 (int): Índice inicial do intervalo de demanda média.

- p3 (int): Índice final do intervalo de demanda média.

- x23 (float): Valor da demanda nos períodos de demanda média.

- p4 (int): Índice inicial do intervalo de demanda alta.

- p5 (int): Índice final do intervalo de demanda alta.

- x45 (float): Valor da demanda nos períodos de demanda alta.

Retorna:

    - PerdaTotal (float): Soma total das perdas por excesso e falta de estoque.
"""
    Demanda = np.zeros(n)
    Demanda[p0:p1] = x01 # demanda baixa
    Demanda[p2:p3] = x23 # demanda média
    Demanda[p4:p5] = x45 # demanda alta
    Perda = np.zeros(n) # Vetor para armazenar as perdas financeiras
    for i in range(0,n):
        if q >= Demanda[i]: # Perda por excesso
            Perda[i] = PrecoExcesso*(q - Demanda[i])
        else:
            Perda[i] = PrecoFalta*(Demanda[i] - q) # Perda por falta
            
    PerdaTotal = sum(Perda) # Cálculo da perda total de excesso e falta
    return PerdaTotal   
    






































