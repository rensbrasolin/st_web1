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
    df_pos_atual['Variação de Cota %'] = (( df_pos_atual['Preço'] / df_pos_atual['Preço Médio']) -1) * 100

    # Variação $
    df_pos_atual['Variação de Cota $'] = (df_pos_atual['Patrimônio Atual'] - df_pos_atual['Custo Médio'])

    # Yield %
    df_pos_atual['Yield %'] = ( df_pos_atual['Remunerações $'] / df_pos_atual['Custo Médio']) * 100

    # Performance $ - Reflete a diferença entre aplicado e saldo atual, e não o saldo atual.
    df_pos_atual['Performance $'] = df_pos_atual['Resultado de Vendas $'] + df_pos_atual['Remunerações $'] + df_pos_atual['Variação de Cota $']

    # Performance % - Dá no mesmo usar 'Variação $' ou 'Patimônio Atual'-1
    df_pos_atual['Performance %'] = (
            (df_pos_atual['Resultado de Vendas $'] + df_pos_atual['Remunerações $'] + df_pos_atual['Variação de Cota $'])
            / df_pos_atual['Custo Médio'] * 100
    )



    return df_pos_atual

