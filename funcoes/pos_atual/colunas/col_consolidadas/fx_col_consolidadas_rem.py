# Parte 3 - 1 coluna

def criar_df_pos_atual_col_consolidadas_rem(df_mov_financeiras, df_pos_atual):
    # Obtendo apenas movimentações de recebimento de remuneração (linhas)
    df_pos_atual_col_consolidadas_rem = df_mov_financeiras.loc[(df_mov_financeiras['Movimentação'] == 'Rendimento') |
                                             (df_mov_financeiras['Movimentação'] == 'Dividendo') |
                                             (df_mov_financeiras['Movimentação'] == 'Juros Sobre Capital Próprio')
                                             ].copy()

    df_pos_atual_col_consolidadas_rem = df_pos_atual_col_consolidadas_rem[['Ativo', 'Valor da Operação']]
    df_pos_atual_col_consolidadas_rem.rename(columns={'Valor da Operação': 'Remunerações $'}, inplace=True)

    # Agrupando por ativos e somando
    df_pos_atual_col_consolidadas_rem = df_pos_atual_col_consolidadas_rem.groupby('Ativo').sum()

    # Trazendo as remunerações consolidadas para o df principal
    df_pos_atual_col_consolidadas_rem = df_pos_atual.merge(df_pos_atual_col_consolidadas_rem, on='Ativo', how='left')

    # Preenche valores ausentes em "Remunerações" com 0, se preferir
    df_pos_atual_col_consolidadas_rem['Remunerações'] = df_pos_atual_col_consolidadas_rem['Remunerações $'].fillna(
        0)  # Depois ver se é melhor NaN ou 0

    # Deixando apenas as colunas necessárias
    df_pos_atual_col_consolidadas_rem = df_pos_atual_col_consolidadas_rem[['Ativo', 'Remunerações $']]

    # Mudando titulo col só no final para não dar conflito no cod. que já funcionava.
    # Mudando titulo (não pode ser 'Ativo') para não dar conflito com fx de merge.
    df_pos_atual_col_consolidadas_rem.rename(columns={'Ativo': 'Ticker'}, inplace=True)

    return df_pos_atual_col_consolidadas_rem