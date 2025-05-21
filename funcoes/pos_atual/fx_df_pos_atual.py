# A ideia é constituir o df_pos_atual aqui e só exibilo na pagina

from funcoes.pos_atual.colunas.col_consolidadas.fx_col_consolidadas_inicio import criar_df_pos_atual_col_consolidadas_inicio
from funcoes.pos_atual.colunas.col_cotacao.fx_col_cotacao_tvb3 import criar_df_cotacao_tvb3
from funcoes.pos_atual.colunas.col_consolidadas.fx_col_consolidadas_rem import criar_df_pos_atual_col_consolidadas_rem
from funcoes.pos_atual.colunas.col_consolidadas.fx_col_consolidadas_res_vendas import criar_df_pos_atual_col_consolidadas_res_vendas
from funcoes.pos_atual.colunas.col_calculadas.fx_col_calculadas import criar_col_calculadas


# --------------------------------------------------------------------------------------- Fx inclui df_col no principal

# É obrigatório que a coluna 'Ativo' dos dfs_col não tenham o nome de 'Ativo'. Se não vai dropar a col do df_principal tbm.
def incluir_df_col(df_principal, df_col, col_comum_df_col, col_incluir_df_col):

    df_principal = df_principal.merge(
        df_col[[col_comum_df_col, col_incluir_df_col]],
        left_on='Ativo',
        right_on=col_comum_df_col,
        how='left'
    ).drop(columns=col_comum_df_col)

    # Caso tenha valor vazio, que seja 0
    df_principal[col_incluir_df_col] = df_principal[col_incluir_df_col].fillna(0)

    return df_principal



# -------------------------------------------------------------------------------------------------------- Fx principal
def criar_df_pos_atual(df_mov_financeiras):

    # Start - Colunas: 'Ativo', 'Tipo de Ativo', 'Qtd Acumulada', 'Custo Médio'
    df_pos_atual = criar_df_pos_atual_col_consolidadas_inicio(df_mov_financeiras)

    # Cria e inclui cotação
    df_cotacao_tvb3 = criar_df_cotacao_tvb3(df_mov_financeiras)
    df_pos_atual = incluir_df_col(df_pos_atual, df_cotacao_tvb3, 'Ticker', 'Preço')

    # Cria e inclui remunerações
    df_pos_atual_col_consolidadas_rem =  criar_df_pos_atual_col_consolidadas_rem(df_mov_financeiras, df_pos_atual)
    df_pos_atual = incluir_df_col(
        df_pos_atual, df_pos_atual_col_consolidadas_rem,
        'Ticker', 'Remunerações $')

    # Cria e inclui resultado de vendas
    df_pos_atual_col_consolidadas_res_vendas = criar_df_pos_atual_col_consolidadas_res_vendas(df_mov_financeiras)
    df_pos_atual = incluir_df_col(df_pos_atual, df_pos_atual_col_consolidadas_res_vendas,
                                  'Ticker','Resultado de Vendas $')


    # Cria no próprio df_pos_atual colunas calculadas com medidas já existentes nele.
    # Não se está criando um df_col, por isso não precisa ser inserido como foram as colunas anteriores
    df_pos_atual = criar_col_calculadas(df_pos_atual)


    # Renomeando colunas:
    df_pos_atual.rename(columns={'Preço': 'Preço Atual'}, inplace=True)


    # Escolhendo a ordem das colunas.
    ordem_colunas = [
        'Ativo', 'Tipo',
        'Qtd',
        'Preço Médio', 'Custo Médio',
        'Preço Atual', 'Patrimônio Atual',
        'Variação de Cota %', 'Variação de Cota $',
        'Yield %', 'Remunerações $',
        'Resultado de Vendas $',
        'Performance %', 'Performance $'
    ]

    df_pos_atual = df_pos_atual[ordem_colunas]



    return df_pos_atual