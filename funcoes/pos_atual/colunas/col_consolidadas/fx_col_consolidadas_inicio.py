# Início de df_pos_atual: Parte 1 - 4 colunas
# Partindo do extrato (df_mov_fin) e consolidando 4 colunas de início.
# Depois serão inseridas  outras colunas consolidadas que são criadas separadamente pois são mais complexas que essas iniciais.
#     Colunas avulsas serão criadas como df, e na sequencia incluidas no df principal. Assim como a col cotação.


# Técnicamente todas as colunas são calculadas, porém no contexto do df_pos_atual:
# Consolidada: Significa que foi calculada pelo df_mov_fin e muito provavelmente foram agraupadas.
# Calculada: Significa que foi calculada já pelo próprio df_pos_atual. Ou seja, depende de que já existam certas colunas


def criar_df_pos_atual_col_consolidadas_inicio(df_mov_financeiras):

    # __________________________________________ Mantendo apenas Compras e vendas.
    df_pos_atual_col_consolidadas_inicio = df_mov_financeiras.loc[df_mov_financeiras['Movimentação'] == 'Transferência - Liquidação'].copy()
    df_pos_atual_col_consolidadas_inicio = df_pos_atual_col_consolidadas_inicio.drop(columns=['Instituição', 'Movimentação', 'Produto'])
    df_pos_atual_col_consolidadas_inicio = df_pos_atual_col_consolidadas_inicio.sort_values(by='Data') # Ajuda a interpretar o df


    # __________________________________________ criar_col_qtd_acumulada (Atualizada a cada compra/venda)
    df_pos_atual_col_consolidadas_inicio['Qtd Acumulada'] = df_pos_atual_col_consolidadas_inicio.groupby('Ativo')['Quantidade'].cumsum()



    # __________________________________________ criar_col_custo_medio
    # Coluna vai ajustando o 'Valor Aplicado/Total Investido/ PM Total/ Custo Médio' conforme compras e vendas.
    # Quando há vendas ele não debita o valor da venda (Preço vendido*qtde vendas), mas sim o PM atual*qtd vendas

    df_pos_atual_col_consolidadas_inicio = df_pos_atual_col_consolidadas_inicio.copy()  # Evita modificar o DataFrame original

    # Inicializa a coluna 'Custo médio'
    df_pos_atual_col_consolidadas_inicio['Custo Médio'] = 0.0


    # Agrupa o DataFrame por 'Ativo' para calcular o custo médio separadamente para cada ativo
    for ativo, grupo in df_pos_atual_col_consolidadas_inicio.groupby('Ativo'):
        indices = grupo.index  # Obtém os índices reais do DataFrame original
        custo_medio_acumulado = 0  # Inicializa o custo médio acumulado

        for i, idx in enumerate(indices):
            qtd_acumulada = df_pos_atual_col_consolidadas_inicio.loc[idx, 'Qtd Acumulada']
            entrada_saida = df_pos_atual_col_consolidadas_inicio.loc[idx, 'Entrada/Saída']
            valor_operacao = df_pos_atual_col_consolidadas_inicio.loc[idx, 'Valor da Operação']

            # Primeira linha do ativo: apenas copia o valor da operação
            if i == 0:
                custo_medio_acumulado = valor_operacao

            elif qtd_acumulada == 0:
                custo_medio_acumulado = 0  # Se a quantidade acumulada for 0, o custo médio também deve ser zerado

            elif entrada_saida == 'Credito':
                # Se for uma compra, soma o valor da operação ao custo médio acumulado
                custo_medio_acumulado += valor_operacao

            elif entrada_saida == 'Debito':
                # Se for uma venda, reduz o custo médio proporcionalmente à quantidade vendida
                qtd_movimentada = abs(df_pos_atual_col_consolidadas_inicio.loc[idx, 'Quantidade']) # Garante que a quantidade seja positiva para o cálculo
                custo_medio_acumulado -= (custo_medio_acumulado / (qtd_acumulada + qtd_movimentada)) * qtd_movimentada

            # Atualiza o DataFrame com o custo médio calculado para a linha atual
            df_pos_atual_col_consolidadas_inicio.loc[idx, 'Custo Médio'] = custo_medio_acumulado



    # # __________________________________________ criar_col_pm - DEIXAR COMENTADA
    # # Poderia ser criada aqui, mas para manter a organização, vou criá-la no outro arq, pois coluna não é consolidada, e sim calculada.
    # # Caso um dia eu queira verificar evolução de PM e PREÇO PAGO a cada compra, esse df será útil.
    # df_pos_atual_col_consolidadas_inicio['Preço Médio'] = df_pos_atual_col_consolidadas_inicio['Custo Médio'] / df_pos_atual_col_consolidadas_inicio['Qtd Acumulada']



    # __________________________________________ Consolidando df

    # Deixando apenas a linha mais recente de cada ativo. Assim a coluna qtd_acumulada virará a coluna qtd_atual
    # Ordena pela data em ordem decrescente e mantém apenas a primeira ocorrência de cada ativo, sem groupby mesmo.
    df_pos_atual_col_consolidadas_inicio = df_pos_atual_col_consolidadas_inicio.sort_values('Data', ascending=False).drop_duplicates(subset='Ativo', keep='first')



    # __________________________________________ Deixando apenas as colunas necessárias, com nomes menores e/ou melhores.
    df_pos_atual_col_consolidadas_inicio = df_pos_atual_col_consolidadas_inicio[['Ativo', 'Tipo de Ativo', 'Qtd Acumulada', 'Custo Médio']]
    df_pos_atual_col_consolidadas_inicio.rename(columns={'Tipo de Ativo': 'Tipo', 'Qtd Acumulada': 'Qtd'}, inplace=True)


    return df_pos_atual_col_consolidadas_inicio



















# ------------------------------------------------------------------------------------------------------- Fx simples
# Jeito direto ao ponto. Resolve para PM mas pode atrapalhar 'Custo Médio' e com certeza atrapalha 'Performance %'

# def consolidar_pm(df_mov_financeiras):
#     df_pm = df_mov_financeiras.loc[(df_mov_financeiras['Movimentação'] == 'Transferência - Liquidação') &
#                                             (df_mov_financeiras['Valor da Operação'] > 0)
#                                             ].copy()
#     df_pm = df_pm[['Ativo', 'Valor da Operação', 'Quantidade']]
#     df_pm = df_pm.groupby('Ativo').sum()
#     # Criando a coluna preço médio
#     df_pm['Preço Médio'] = df_pm['Valor da Operação'] / df_pm['Quantidade']
#     df_pm = df_pm[['Preço Médio']]
#     return df_pm