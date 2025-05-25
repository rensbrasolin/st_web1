# Fim do df_pos_atual: Parte 6 - 6 colunas
# Partindo das colunas criadas (cosolidadas inicias+cotação+consolidadas separadas) anteriormente e calcula novas colunas usando as medidas já criadas.
# Importante inserir por último pois precisa que outras colunas já existam.

# Técnicamente todas as colunas são calculadas, porém no contexto do df_pos_atual:
# Consolidada: Significa que foi calculada pelo df_mov_fin e muito provavelmente foram agraupadas.
# Calculada: Significa que foi calculada já pelo próprio df_pos_atual. Ou seja, depende de que já existam certas colunas

# Talvez deva se chamar incluir_cols_calc.. algo assim
def criar_col_calculadas(df_pos_atual):

    # Preço Médio
    df_pos_atual['Preço Médio'] = df_pos_atual['Custo Médio'] / df_pos_atual['Qtd']


    # Patrimônio Atual
    df_pos_atual['Patrimônio Atual'] = df_pos_atual["Qtd"] * df_pos_atual["Preço"]


    # Variação %
    df_pos_atual['Variação %'] = (( df_pos_atual['Preço'] / df_pos_atual['Preço Médio']) -1) * 100


    # Variação $
    df_pos_atual['Variação $'] = (df_pos_atual['Patrimônio Atual'] - df_pos_atual['Custo Médio'])


    # Yield on Cost % - Deixar um pouco e depois provavelmente excluir.
    # Não será exibido, pois não faz sentido comparar todos os dividendos recebidos com o Custo Médio atual.
    # A única medida que faz sentido comprar com o Custo Médio Atual é o Patrimônuo Atual, que muda junto com ele.
    # Essa medida faz mais sentido ser calculada acadarecebimento dela, como faço na seção de remunerações
    df_pos_atual['Yield on Cost %'] = ( df_pos_atual['Remunerações $'] / df_pos_atual['Custo Médio']) * 100


    # Performance $ - Não reflete o saldo atual, mas sim o retorno, a diferença.
    df_pos_atual['Performance $'] = df_pos_atual['Resultado de Vendas $'] + df_pos_atual['Remunerações $'] + df_pos_atual['Variação $']


    # Performance % - Deixar um pouco para ver se tem alternativas, se não, depois excluir.
    # Não será exibido, pois não faz sentido comparar a Performance $ de todu um período com o Custo Médio atual.
    # A única medida que faz sentido comprar com o Custo Médio Atual é o Patrimônuo Atual, que muda junto com ele.
    # Imagina que o investidor liquidou toda a posição menos 1. Nesse caso o CM será igual ao PM, e não faria sentido
    # comparar esse CM/PM com Remunerações $ e Resultado de Vendas de todu um período

    # Daria no mesmo usar 'Variação $' ou 'Patimônio Atual'-1.
    # Posições que foram zeradas terão valor vazio pois custo médio será 0
    df_pos_atual['Performance %'] = df_pos_atual['Performance $']/ df_pos_atual['Custo Médio'] * 100



    return df_pos_atual

