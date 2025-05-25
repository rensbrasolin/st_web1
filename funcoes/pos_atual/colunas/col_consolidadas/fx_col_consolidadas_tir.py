# Parte 5 - 1 coluna e 1 medida de total
# Inserí-las por último, pois no cálculo elas precisam da col calculada 'Patrimônio Atual'

# Importante entender que as fxs TIR de coluna (por ativo) e TIR total/indicador têm sua diferenças:
#     Na por ativo, é necessário separar as mov_fin de cada ativo e utilizar a fx xirr em cada um deles.
#     Enquanto na fx total, o df_mov_fin completo é filtrado conforme o filtro (por tipo) aplicado no df_pos_atual,
#     e usa a fx xirr apenas uma vez.
# Claro que nas 2 fxs é obrigatório inverter os sinais e inserir a última (linha) que representa a última movimentação,
# que nada mais é do que a simulaçãa da liquidação da carteira.

import pandas as pd
from datetime import date, timedelta
import numpy as np


def criar_df_pos_atual_col_consolidadas_tir(df_mov_financeiras, df_pos_atual):
    # Vou criar a data_util, depois definir a fx xirr e só depois desenvolver a fx consolidar TIR

# ------------------------------------------------------------------------- Criando data

    data_hoje = date.today() # data hj será sempre a data de hj.
    data_util = data_hoje # Data útil inicialmente é hj, mas se hj naõ for dia útil, vira o dia útil anterior.

    if data_hoje.weekday() == 6:  # Domingo é o dia 6
        data_util = data_hoje - timedelta(days=2)

    # Se hoje for sábado, subtraia 1 dia (para obter a cotação de sexta-feira)
    elif data_hoje.weekday() == 5:  # Sábado é o dia 5
        data_util = data_hoje - timedelta(days=1)

# ------------------------------------------------------------------------- Definindo fx interna
    def xirr(df, guess=0.05, date_column='date', amount_column='amount'):
        '''Calculates XIRR from a series of cashflows.
           Needs a dataframe with columns date and amount, customisable through parameters.
           Requires Pandas, NumPy libraries'''

        df = df.sort_values(by=date_column).reset_index(drop=True)

        amounts = df[amount_column].values
        dates = df[date_column].values

        years = np.array(dates - dates[0], dtype='timedelta64[D]').astype(int) / 365

        step = 0.05
        epsilon = 0.0001
        limit = 1000
        residual = 1

        # Test for direction of cashflows
        disc_val_1 = np.sum(amounts / ((1 + guess) ** years))
        disc_val_2 = np.sum(amounts / ((1.05 + guess) ** years))
        mul = 1 if disc_val_2 < disc_val_1 else -1

        # Calculate XIRR
        for i in range(limit):
            prev_residual = residual
            residual = np.sum(amounts / ((1 + guess) ** years))
            if abs(residual) > epsilon:
                if np.sign(residual) != np.sign(prev_residual):
                    step /= 2
                guess = guess + step * np.sign(residual) * mul
            else:
                return guess  # Retorna a tir em decimal

    # -------------------------------------------------------------------------Desenvolvendo fx consolidar TIR


    # VER ANOTAÇÕES
    # Filtrando para manter só as movimentações que realmente movimentam valores
    df_mov_tir = df_mov_financeiras.loc[(df_mov_financeiras['Movimentação'] == 'Transferência - Liquidação') |
                                  (df_mov_financeiras['Movimentação'] == 'Dividendo') |
                                  (df_mov_financeiras['Movimentação'] == 'Juros Sobre Capital Próprio') |
                                  (df_mov_financeiras['Movimentação'] == 'Rendimento')
                                  ].copy().reset_index(drop=True)

    # Obter valores únicos da coluna 'Ativo'
    lista_fluxo_ativos = df_mov_tir['Ativo'].unique()

    # Dicionário para armazenar os DataFrames separados
    dict_dfs_fluxo = {}

    # Loop sobre cada ativo
    for ativo in lista_fluxo_ativos:
        # Criando um df_fluxo para cada ativo, Filtrar o DataFrame original para obter apenas as linhas com o ativo atual
        df_fluxo = df_mov_tir[df_mov_tir['Ativo'] == ativo].reset_index(drop=True)

        # Invertendo sinais: Compras estão +, Vendas estão - Preciso inverter
        df_fluxo.loc[(df_fluxo[
                          'Movimentação'] == 'Transferência - Liquidação'), 'Valor da Operação'] *= -1  # Usei '=' aqui para atribuir o valor. se não ele multiplica mas não preenche

        # Filtrando só as coluans necessárias
        df_fluxo = df_fluxo[['Data', 'Valor da Operação']]

        # Ordenando para data decrescente
        df_fluxo = df_fluxo.sort_values(by='Data', ascending=True).reset_index(drop=True)

        ###########     INSERINDO A ÚLTIMA LINHA, QUE É O 'PATRIMÔNIO ATUAL'     ########### ['Ativo']

        # Primeiro vou criar uma variável 'patrimonio_atual' puxada lá do df_acoes_patrimonio, que é onde tem o valor que preciso.
        patrimonio_atual_ativo = df_pos_atual['Patrimônio Atual'].loc[df_pos_atual['Ativo'] == ativo]


        # Criando um dict para inserir como ultima linha. Tive que formatar o valor com float.
        # Usei iloc mesmo não sendo em df. Pois só com float daria warning, gpt que sugeriu e funcionou
        dic_venda_simulada_ativo = {'Data': data_util, 'Valor da Operação': float(patrimonio_atual_ativo.iloc[0])}

        # Achando a ultima linha e inserindo dados nela
        tam = len(df_fluxo)
        df_fluxo.loc[tam] = [dic_venda_simulada_ativo['Data'], dic_venda_simulada_ativo['Valor da Operação']]

        # Converter a coluna "Data" para datetime, pois mesmo já sendo (<class 'datetime.date'>), no df dava ruim.
        df_fluxo['Data'] = pd.to_datetime(df_fluxo['Data'])

        # Armazenar o DataFrame filtrado no dicionário, usando o nome do ativo como chave
        dict_dfs_fluxo[ativo] = df_fluxo



    # Agora, com todos os fluxos armazenados, vou calcular a TIR para cada ativo e inserir "ativo:TIR" no dic_tirs
    dic_tirs = {}

    for ativo, df_fluxo in dict_dfs_fluxo.items():
        # Aplicando a função em cada ativo
        tir = xirr(df_fluxo, guess=0.05, date_column='Data', amount_column='Valor da Operação') * 100
        # Iinserindo o item no dicinário (ativo = TIR)
        dic_tirs[ativo] = tir


    # Criando um df com os dados do dic
    df_pos_atual_col_consolidadas_tir = pd.DataFrame.from_dict(dic_tirs, orient='index', columns=['TIR %'])

    # Defenindo um nome para o índice, que estava em branco. Que por sinal tem que ser diferente de 'Ativo'
    df_pos_atual_col_consolidadas_tir.index.name = 'Ticker'

    # Resetando índice para que vire coluna
    df_pos_atual_col_consolidadas_tir = df_pos_atual_col_consolidadas_tir.reset_index()


    return df_pos_atual_col_consolidadas_tir





# ----------------------------------------------------------------------------------------------------------- Fx totais
# Fiz essa fx com base na fx acima (criar_df_pos_atual_col_consolidadas_tir).
# Essa fx aqui, além de ser mais simples (ver anotações no topo), também tem um código mais limpo e organizado.


def criar_tir_total_df_pos_atual(df_pos_atual, df_mov_financeiras, patrimonio_atual_total_df_pos_atual):
    # ------------------------------------------------------- Obtendo o df_mov_filtrado
    lista_ativos = df_pos_atual[
        'Ativo'].unique().tolist()  # lista virá em conformidade com o filtro aplicado no df_pos_atual
    df_mov_fin_filtrado = df_mov_financeiras[df_mov_financeiras['Ativo'].isin(lista_ativos)]

    df_fluxo_caixa = df_mov_fin_filtrado.copy()

    # ------------------------------------------------------ Criando data para usar na última mov

    data_hoje = date.today()  # data hj será sempre a data de hj.
    data_util = data_hoje  # Data útil inicialmente é hj, mas se hj naõ for dia útil, vira o dia útil anterior.

    if data_hoje.weekday() == 6:  # Domingo é o dia 6
        data_util = data_hoje - timedelta(days=2)

    # Se hoje for sábado, subtraia 1 dia (para obter a cotação de sexta-feira)
    elif data_hoje.weekday() == 5:  # Sábado é o dia 5
        data_util = data_hoje - timedelta(days=1)

    # ------------------------------------------------- Tratando df

    # Compras estão (+), Vendas estão (-). Preciso inverter estes sinais antes de passar o df pra fx.
    # Não atribuir variavel a essa linha, se não ele só manterá a coluna 'Valor da Operação'
    # Por isso usei '=', para atribuir o valor. se não ele multiplica mas não preenche.
    df_fluxo_caixa.loc[(df_fluxo_caixa[
                            'Movimentação'] == 'Transferência - Liquidação'), 'Valor da Operação'] *= -1

    df_fluxo_caixa = df_fluxo_caixa[['Data', 'Valor da Operação']]

    # Ordenando para data decrescente
    df_fluxo_caixa = df_fluxo_caixa.sort_values(by='Data', ascending=True).reset_index(drop=True)

    # --------------------- Pegando patrimonio atual e inserindo a ultima linha

    # Criando um dict para inserir como ultima linha. Tive que formatar o valor com float.
    # Usei iloc mesmo não sendo em df. Pois só com float daria warning, gpt que sugeriu e funcionou
    dic_venda_simulada = {'Data': data_util, 'Valor da Operação': patrimonio_atual_total_df_pos_atual}

    # Achando a ultima linha e inserindo dados nela
    tam = len(df_fluxo_caixa)
    df_fluxo_caixa.loc[tam] = [dic_venda_simulada['Data'], dic_venda_simulada['Valor da Operação']]

    # Converter a coluna "Data" para datetime, pois mesmo já sendo (<class 'datetime.date'>), no df dava ruim.
    # Essa conversão precisa ser feita aqui, logo após inserir o dic na última linha.
    df_fluxo_caixa['Data'] = pd.to_datetime(df_fluxo_caixa['Data'])

    # df_fluxo_caixa

    tir_total_df_pos_atual = xirr(df_fluxo_caixa, guess=0.05, date_column='Data', amount_column='Valor da Operação') * 100


    return tir_total_df_pos_atual








# ------------------------------------------------------------------------------------------------------- Fx xir avulsa
# Igual a fx xtir do excel

def xirr(df, guess=0.05, date_column='date', amount_column='amount'):
    '''Calculates XIRR from a series of cashflows.
       Needs a dataframe with columns date and amount, customisable through parameters.
       Requires Pandas, NumPy libraries'''

    df = df.sort_values(by=date_column).reset_index(drop=True)

    amounts = df[amount_column].values
    dates = df[date_column].values

    years = np.array(dates - dates[0], dtype='timedelta64[D]').astype(int) / 365

    step = 0.05
    epsilon = 0.0001
    limit = 1000
    residual = 1

    # Test for direction of cashflows
    disc_val_1 = np.sum(amounts / ((1 + guess) ** years))
    disc_val_2 = np.sum(amounts / ((1.05 + guess) ** years))
    mul = 1 if disc_val_2 < disc_val_1 else -1

    # Calculate XIRR
    for i in range(limit):
        prev_residual = residual
        residual = np.sum(amounts / ((1 + guess) ** years))
        if abs(residual) > epsilon:
            if np.sign(residual) != np.sign(prev_residual):
                step /= 2
            guess = guess + step * np.sign(residual) * mul
        else:
            return guess  # Retorna a tir em decimal