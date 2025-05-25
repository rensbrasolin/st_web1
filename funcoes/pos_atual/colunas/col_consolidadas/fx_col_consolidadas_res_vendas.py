# Parte 4 - 1 coluna
# Resultado de vendas. df só cria linha se houver registro, mas o merge acontece normalmente preenchendo c/ 0 se vazio.

# ----------------------------------------------------------------------------------------------------- Nova fx
# Problema resolvido: GPT
# Quando o investidor zera sua posição em um ativo (ou seja, vende tudo) e volta a comprar depois, o cálculo do
# preço médio não deve considerar as compras anteriores à zeragem. Atualmente o código mantém o acumulado mesmo após
# zerar a posição, o que causa erro no cálculo do preço médio da nova sequência de compras.

#  Explicações dos comentários:
# saldo_posicao é como um estoque corrente: soma as compras, subtrai as vendas.
# Se o investidor zerar a posição (saldo 0), reiniciamos o preço médio.
# Assim, novas compras feitas após zerar não misturam o PM com as compras antigas, como você queria.


def criar_df_pos_atual_col_consolidadas_res_vendas(df_mov_financeiras):
    # Obtendo apenas movimentações de compras e vendas
    df_pos_atual_col_consolidadas_res_vendas = df_mov_financeiras.loc[
        (df_mov_financeiras['Movimentação'] == 'Transferência - Liquidação')].copy().reset_index()

    # Deixando apenas as colunas necessárias
    df_pos_atual_col_consolidadas_res_vendas = df_pos_atual_col_consolidadas_res_vendas[
        ['Ativo', 'Data', 'Quantidade', 'Valor da Operação']]

    # VER EXPLICAÇÃO NAS ANOTAÇÕES

    # Ordena o DataFrame por ativo e data
    df_pos_atual_col_consolidadas_res_vendas.sort_values(by=['Ativo', 'Data'], inplace=True)

    # Cria a nova coluna com valor zero inicialmente
    df_pos_atual_col_consolidadas_res_vendas['PM na Venda'] = 0.0

    # Itera sobre cada ativo para calcular o preço médio na venda
    for ativo, grupo in df_pos_atual_col_consolidadas_res_vendas.groupby('Ativo'):
        # Inicializa acumuladores de quantidade, valor e saldo da posição
        qtde_acumulada = 0
        valor_acumulado = 0.0
        saldo_posicao = 0  # Novo: acompanha posição líquida do ativo

        # Itera pelas linhas do grupo
        for idx in grupo.index:
            row = df_pos_atual_col_consolidadas_res_vendas.loc[idx]

            if row['Quantidade'] > 0:  # É uma compra
                # Atualiza acumuladores
                qtde_acumulada += row['Quantidade']
                valor_acumulado += row['Valor da Operação']
                saldo_posicao += row['Quantidade']  # Novo
                # Atribui 0 ao preço médio na coluna para compras
                df_pos_atual_col_consolidadas_res_vendas.loc[idx, 'PM na Venda'] = 0.0

            else:  # É uma venda
                if qtde_acumulada > 0:
                    preco_medio = valor_acumulado / qtde_acumulada
                else:
                    preco_medio = 0.0  # Caso não haja histórico de compras

                # Atribui o preço médio na venda para a linha de venda
                df_pos_atual_col_consolidadas_res_vendas.loc[idx, 'PM na Venda'] = preco_medio

                # Atualiza saldo da posição
                saldo_posicao += row['Quantidade']  # row['Quantidade'] é negativa

                # Se posição for zerada, zera os acumuladores
                if saldo_posicao == 0:
                    qtde_acumulada = 0
                    valor_acumulado = 0.0

    # Agora que não preciso mais das compras, vou fazer alguns ajustes

    # Manter só Vendas
    df_pos_atual_col_consolidadas_res_vendas = df_pos_atual_col_consolidadas_res_vendas.loc[
        (df_pos_atual_col_consolidadas_res_vendas['Quantidade'] < 0)].copy().reset_index(drop=True)

    # Alterar nome da coluna para un nome intuitivo
    df_pos_atual_col_consolidadas_res_vendas.rename(columns={'Valor da Operação': 'Total Vendido'}, inplace=True)

    # Transpor números negativos
    df_pos_atual_col_consolidadas_res_vendas[['Quantidade', 'Total Vendido']] *= -1

    # Criando coluna de Preço Médio Total, para poder encontrar a diferença, que se for positiva será lucro e se for negativa será prejuízo na venda
    df_pos_atual_col_consolidadas_res_vendas['PM Total'] = df_pos_atual_col_consolidadas_res_vendas['Quantidade'] * \
                                                           df_pos_atual_col_consolidadas_res_vendas[
                                                               'PM na Venda']

    # Criando coluna de lucro/prej. nas vendas
    df_pos_atual_col_consolidadas_res_vendas['Resultado de Vendas $'] = df_pos_atual_col_consolidadas_res_vendas[
                                                                            'Total Vendido'] - \
                                                                        df_pos_atual_col_consolidadas_res_vendas[
                                                                            'PM Total']

    df_pos_atual_col_consolidadas_res_vendas = df_pos_atual_col_consolidadas_res_vendas[
        ['Ativo', 'Resultado de Vendas $']]

    # Agrupando por ativos
    df_pos_atual_col_consolidadas_res_vendas = df_pos_atual_col_consolidadas_res_vendas.groupby('Ativo').sum()

    # Para que índice "Ativo" vire coluna
    df_pos_atual_col_consolidadas_res_vendas = df_pos_atual_col_consolidadas_res_vendas.reset_index()

    # Mudando titulo col só no final para não dar conflito no cod. que já funcionava.
    # Mudando titulo (não pode ser 'Ativo') para não dar conflito com fx de merge.
    df_pos_atual_col_consolidadas_res_vendas.rename(columns={'Ativo': 'Ticker'}, inplace=True)

    return df_pos_atual_col_consolidadas_res_vendas


# ------------------------------------------------------- fx antiga, deixar um pouco e depois excluir

# def criar_df_pos_atual_col_consolidadas_res_vendas(df_mov_financeiras):
#     # Obtendo apenas movimentações de compras e vendas
#     df_pos_atual_col_consolidadas_res_vendas = df_mov_financeiras.loc[
#         (df_mov_financeiras['Movimentação'] == 'Transferência - Liquidação')].copy().reset_index()
#
#     # Deixando apenas as colunas necessárias
#     df_pos_atual_col_consolidadas_res_vendas = df_pos_atual_col_consolidadas_res_vendas[['Ativo', 'Data', 'Quantidade', 'Valor da Operação']]
#
#
#     # VER EXPLICAÇÃO NAS ANOTAÇÕES
#
#     # Ordena o DataFrame por ativo e data
#     df_pos_atual_col_consolidadas_res_vendas.sort_values(by=['Ativo', 'Data'], inplace=True)
#
#     # Cria a nova coluna com valor zero inicialmente
#     df_pos_atual_col_consolidadas_res_vendas['PM na Venda'] = 0.0
#
#     # Itera sobre cada ativo para calcular o preço médio na venda
#     for ativo, grupo in df_pos_atual_col_consolidadas_res_vendas.groupby('Ativo'):
#         # Inicializa acumuladores de quantidade e valor
#         qtde_acumulada = 0
#         valor_acumulado = 0.0
#
#         # Itera pelas linhas do grupo
#         for idx, row in grupo.iterrows():
#             if row['Quantidade'] > 0:  # É uma compra
#                 # Atualiza acumuladores
#                 qtde_acumulada += row['Quantidade']
#                 valor_acumulado += row['Valor da Operação']
#                 # Atribui 0 ao preço médio na coluna para compras
#                 df_pos_atual_col_consolidadas_res_vendas.loc[idx, 'PM na Venda'] = 0.0
#             else:  # É uma venda
#                 # Calcula o preço médio considerando as compras anteriores
#                 if qtde_acumulada > 0:
#                     preco_medio = valor_acumulado / qtde_acumulada
#                 else:
#                     preco_medio = 0.0  # Caso não haja histórico de compras
#
#                 # Atribui o preço médio na venda para a linha de venda
#                 df_pos_atual_col_consolidadas_res_vendas.loc[idx, 'PM na Venda'] = preco_medio
#
#
#
#     # Agora que não preciso mais das compras, vou fazer alguns ajustes
#
#     # Manter só Vendas
#     df_pos_atual_col_consolidadas_res_vendas = df_pos_atual_col_consolidadas_res_vendas.loc[
#         (df_pos_atual_col_consolidadas_res_vendas['Quantidade'] < 0)].copy().reset_index(drop=True)
#
#     # Alterar nome da coluna para un nome intuitivo
#     df_pos_atual_col_consolidadas_res_vendas.rename(columns={'Valor da Operação': 'Total Vendido'}, inplace=True)
#
#     # Transpor números negativos
#     df_pos_atual_col_consolidadas_res_vendas[['Quantidade', 'Total Vendido']] *= -1
#
#     # Criando coluna de Preço Médio Total, para poder encontrar a diferença, que se for positiva será lucro e se for negativa será prejuízo na venda
#     df_pos_atual_col_consolidadas_res_vendas['PM Total'] = df_pos_atual_col_consolidadas_res_vendas['Quantidade'] * df_pos_atual_col_consolidadas_res_vendas[
#         'PM na Venda']
#
#     # Criando coluna de lucro/prej. nas vendas
#     df_pos_atual_col_consolidadas_res_vendas['Resultado de Vendas $'] = df_pos_atual_col_consolidadas_res_vendas['Total Vendido'] - \
#                                                        df_pos_atual_col_consolidadas_res_vendas['PM Total']
#
#     df_pos_atual_col_consolidadas_res_vendas = df_pos_atual_col_consolidadas_res_vendas[['Ativo', 'Resultado de Vendas $']]
#
#     # Agrupando por ativos
#     df_pos_atual_col_consolidadas_res_vendas = df_pos_atual_col_consolidadas_res_vendas.groupby('Ativo').sum()
#
#     # Para que índice "Ativo" vire coluna
#     df_pos_atual_col_consolidadas_res_vendas = df_pos_atual_col_consolidadas_res_vendas.reset_index()
#
#     # Mudando titulo col só no final para não dar conflito no cod. que já funcionava.
#     # Mudando titulo (não pode ser 'Ativo') para não dar conflito com fx de merge.
#     df_pos_atual_col_consolidadas_res_vendas.rename(columns={'Ativo': 'Ticker'}, inplace=True)
#
#     return df_pos_atual_col_consolidadas_res_vendas