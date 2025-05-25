# A ideia é constituir o df_pos_atual aqui e só exibi-lo lá na pagina

import streamlit as st

from funcoes.pos_atual.colunas.col_consolidadas.fx_col_consolidadas_inicio import criar_df_pos_atual_col_consolidadas_inicio
from funcoes.pos_atual.colunas.col_cotacao.fx_col_cotacao_tvb3 import criar_df_cotacao_tvb3
from funcoes.pos_atual.colunas.col_consolidadas.fx_col_consolidadas_rem import criar_df_pos_atual_col_consolidadas_rem
from funcoes.pos_atual.colunas.col_consolidadas.fx_col_consolidadas_res_vendas import criar_df_pos_atual_col_consolidadas_res_vendas
from funcoes.pos_atual.colunas.col_calculadas.fx_col_calculadas import criar_col_calculadas
from funcoes.pos_atual.colunas.col_consolidadas.fx_col_consolidadas_tir import criar_df_pos_atual_col_consolidadas_tir



# --------------------------------------------------------------------------------------- Fx inclui df_col no principal
# OBRIGAÓRIO QUE ELA FIQUE ACIMA DA FX criar_df_pos_atual, POIS ELA É USADA LÁ
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

    # Start - Colunas: 'Ativo', 'Tipo de Ativo', 'Qtd Acumulada' (Qtd), 'Custo Médio'
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


    # Cria e inclui TIR. Tem que ser inserida por último pois usa a col calculada 'Patrimônio Atual'
    df_pos_atual_col_consolidadas_tir = criar_df_pos_atual_col_consolidadas_tir(df_mov_financeiras, df_pos_atual)
    df_pos_atual = incluir_df_col(df_pos_atual, df_pos_atual_col_consolidadas_tir,
                                  'Ticker','TIR %')


    # Renomeando colunas:
    df_pos_atual.rename(columns={'Preço': 'Preço Atual'}, inplace=True)


    # Escolhendo não apenas a ordem das colunas, mas quais irão aparecer.
    ordem_colunas = [
        'Ativo',
        'Tipo',
        'Qtd',
        'Preço Médio',
        'Custo Médio',
        'Preço Atual',
        'Patrimônio Atual',
        'Variação %',
        'Variação $',
        # 'Yield on Cost %',
        'Remunerações $',
        'Resultado de Vendas $',
        # 'Performance %',
        'Performance $',
        'TIR %'
    ]

    df_pos_atual = df_pos_atual[ordem_colunas]



    return df_pos_atual


# ----------------------------------------------------------------------------------------------------------- Fx filtros


def criar_filtro_tipo_df_pos_atual(df_pos_atual):
    # Criar um "radio button" para filtrar por Tipo de Ativo
    tipo_ativo_opcoes = ["Todos"] + df_pos_atual["Tipo"].unique().tolist()
    tipo_ativo_selecionado = st.radio(
        "Selecione o Tipo de Ativo",
        options=tipo_ativo_opcoes,
        index=0,  # Valor padrão: "Todos"
    )

    # Atualizar as opções de ativos com base na seleção anterior, 'Tipo de Ativo'


    if tipo_ativo_selecionado == "Todos":
        # Se "Todos" for selecionado, incluir todos os ativos
        ativo_opcoes = ["Todos"] + df_pos_atual["Ativo"].unique().tolist()
    else:
        # Filtrar os ativos com base no Tipo de Ativo selecionado
        ativo_opcoes = ["Todos"] + df_pos_atual.loc[
            df_pos_atual["Tipo"] == tipo_ativo_selecionado, "Ativo"
        ].unique().tolist()
        ###
        # Aplicar filtro por Tipo de Ativo no df
    if tipo_ativo_selecionado != "Todos":
        df_pos_atual = df_pos_atual[
            df_pos_atual["Tipo"] == tipo_ativo_selecionado
            ]

    return df_pos_atual



# ----------------------------------------------------------------------------------------------------------- Fx totais
# Medidas serão criadas na mesma ordem em que as colunas do df form criadas.
# Importante usar os titulos finais das colunas do df_pos_atual nesses cálculos. (olhar na lista acima)

def criar_medidas_df_pos_atual(df_pos_atual):

    # Estas medidas não necessariamente precisam ser mostradas
    qtd_ativos_total_df_pos_atual = df_pos_atual['Qtd'].count() # Essa até faz sentido mostrar.
    qtd_tipos_total_df_pos_atual = df_pos_atual['Tipo'].nunique() # Não faz sentido, já que df pode ser filtrado.
    qtd_total_df_pos_atual = df_pos_atual['Qtd'].sum() # Não tenho certeza se esa medida é necessária.

    custo_medio_total_df_pos_atual = df_pos_atual['Custo Médio'].sum()

    remuneracoes_total_df_pos_atual = df_pos_atual['Remunerações $'].sum()

    res_vendas_total_df_pos_atual = df_pos_atual['Resultado de Vendas $'].sum()

    patrimonio_atual_total_df_pos_atual = df_pos_atual['Patrimônio Atual'].sum()

    variacao_percentual_total_df_pos_atual = (patrimonio_atual_total_df_pos_atual / custo_medio_total_df_pos_atual - 1) * 100

    variacao_absoluta_total_df_pos_atual = df_pos_atual['Variação $'].sum()

    # Não faz mais sentido. Deixar um pouco e depois excluir
    yieldoncost_total_df_pos_atual = remuneracoes_total_df_pos_atual / custo_medio_total_df_pos_atual * 100

    performance_absoluta_total_df_pos_atual = df_pos_atual['Performance $'].sum()

    # Não faz mais sentido. Deixar um pouco e depois excluir
    # No cálculo da coluna, essa medida ficará zerada se a posição for zerada. Já que compara o desempenho com o 'Custo Médio', que estará zerado.
    # Já aqui no total, não, pois só utiliza valores absolutos. E sim, as posições zeradas terão tbm a coluna 'Variação $' zeradas,
    # porém, nesse cálculo não há problema, pois quando a posição é zerada, o que era 'Variação $' vira 'Resultado com Vendas'. acho
    performance_percentual_total_df_pos_atual = ((remuneracoes_total_df_pos_atual + res_vendas_total_df_pos_atual + variacao_absoluta_total_df_pos_atual)
                                                 / custo_medio_total_df_pos_atual * 100)

    # tir_total_df_pos_atual = essa fx é criada separada. Lá no fx_df_pos_atual.py


    return (qtd_ativos_total_df_pos_atual, qtd_tipos_total_df_pos_atual, qtd_total_df_pos_atual, custo_medio_total_df_pos_atual,
            remuneracoes_total_df_pos_atual, res_vendas_total_df_pos_atual,patrimonio_atual_total_df_pos_atual,
            variacao_percentual_total_df_pos_atual, variacao_absoluta_total_df_pos_atual, yieldoncost_total_df_pos_atual,
            performance_absoluta_total_df_pos_atual, performance_percentual_total_df_pos_atual)


# ------------------------ Exibindo indicadores totais
# Por enquanto está cabendo na página, mas uma carteira com 3 dígitos já geraria abreviação do metric.
# Solução mais fácil: Fazer 3 linhas com 4 cada e/ou exibir emoji no título e não no valor.
# Solução difícil: Fazer sem metric, talvrz criar uma fx quer cria metric manualmente com wrtite/title sei lá.

def exibir_medidas_df_pos_atual(
            qtd_ativos_total_df_pos_atual, # Essa até faz sentido mostrar.
            qtd_tipos_total_df_pos_atual, # Não faz muito sentido, já que df pode ser filtrado.
            qtd_total_df_pos_atual,  # Não será usada provavelmente

            custo_medio_total_df_pos_atual,
            remuneracoes_total_df_pos_atual,
            res_vendas_total_df_pos_atual,
            patrimonio_atual_total_df_pos_atual,
            variacao_percentual_total_df_pos_atual,
            variacao_absoluta_total_df_pos_atual,
            yield_total_df_pos_atual, # Não faz mais sentido. Deixar um pouco e depois excluir
            performance_absoluta_total_df_pos_atual,
            performance_percentual_total_df_pos_atual, # Não faz mais sentido. Deixar um pouco e depois excluir
            tir_total_df_pos_atual,
        ):

# Poderia até usar um for mas como cada caso é um caso, vou deixar 'manual' mesmo.

    col1, col2, col3, col4, col5 = st.columns([0.53, 1, 1, 1, 1])

    with col1:
        with st.container(border=True):
            st.metric('🧾 Ativos', f' {qtd_ativos_total_df_pos_atual:,.0f}')

        with st.container(border=True):
            st.metric('🗂️ Tipos de Ativos', f'{qtd_tipos_total_df_pos_atual:,.0f}')


    with col2:
        with st.container(border=True):
            st.metric('💰 Custo Médio', f'R$ {custo_medio_total_df_pos_atual:,.2f}'.replace(
                ",", "X").replace(".", ",").replace("X", "."),
                      help="""
                        - Soma do valor de todas as compras
                        - Quando há venda, subtrai-se o valor de 'Preço Médio * Qtd Vendida'
                        """
                      )

        with st.container(border=True):
            st.metric('🏦 Patrimônio Atual', f'R$ {patrimonio_atual_total_df_pos_atual:,.2f}'.replace(
                ",", "X").replace(".", ",").replace("X", "."),
                      help = "'Quantidade de Ativos * Cotação Atual'"
                      )


    with col3:
        with st.container(border=True):
            st.metric('📈 Variação Percentual', f'{variacao_percentual_total_df_pos_atual:,.2f}%',
                      help='Diferença entre Cotação Atual e Preço Médio'
                      )

        with st.container(border=True):
            st.metric('📈 Variação Absoluta', f' R$ {variacao_absoluta_total_df_pos_atual:,.2f}'.replace(
                ",", "X").replace(".", ",").replace("X", "."),
                      help='Diferença absoluta entre Patrimônio Atual e Custo Médio'
                      )


    with col4:
        with st.container(border=True):
            st.metric('🪙 Remunerações', f'R$ {remuneracoes_total_df_pos_atual:,.2f}'.replace(
                ",", "X").replace(".", ",").replace("X", "."),
                      help="""
            Soma dos recebimentos de:
            - Dividendo
            - Juros Sobre Capital Próprio
            - Rendimento"""
                      )

        with st.container(border=True):
            st.metric('💵 Resultado de Vendas', f'R$ {res_vendas_total_df_pos_atual:,.2f}'.replace(
                ",", "X").replace(".", ",").replace("X", "."),
                      help='Saldo dos resultados (lucro ou prejuízo) de todas as operações de vendas'
                      )


    with col5:
        with st.container(border=True):
            st.metric('🚀 Performance Absoluta', f'R$ {performance_absoluta_total_df_pos_atual:,.2f}'.replace(
                ",", "X").replace(".", ",").replace("X", "."),
                      help='''
                           Saldo dos resultados de:
                           - Variação Absoluta
                           - Remunerações
                           - Resultado de Vendas
                           '''
                      )

        with st.container(border=True):
            st.metric('💹 Taxa Interna de Retorno', f'{tir_total_df_pos_atual:,.2f}% a.a.',
                      help='''
                 Calcula a taxa de retorno anual, considerando todas as movimentações do fluxo de caixa da carteira:
                 - Compras [ - ]
                 - Vendas [ + ]
                 - Remunerações [ + ]
                 '''
                      )  # 🧮📉














    # col1b, col2b, col3b, col4b = st.columns([0.8, 1, 1, 1])
    #
    # with col1b:
    #     with st.container(border=True):
    #         st.metric('Ativos', f'🧾 {qtd_ativos_total_df_pos_atual:,.0f}')
    #
    #     with st.container(border=True):
    #         st.metric('Variação Percentual', f'📈 {variacao_percentual_total_df_pos_atual:,.2f}%')
    #
    #     # with st.container(border=True):
    #     #     st.metric('Performance Percentual', f'🚀 {performance_percentual_total_df_pos_atual:,.2f}%')
    #
    # with col2b:
    #     with st.container(border=True):
    #         st.metric('Tipos de Ativos', f'🗂️ {qtd_tipos_total_df_pos_atual:,.0f}')
    #
    #     with st.container(border=True):
    #         st.metric('Variação Absoluta', f'📈 R$ {variacao_absoluta_total_df_pos_atual:,.2f}'.replace(
    #             ",", "X").replace(".", ",").replace("X", "."))
    #
    #     with st.container(border=True):
    #         st.metric('Performance Absoluta', f'🚀 R$ {performance_absoluta_total_df_pos_atual:,.2f}'.replace(
    #             ",", "X").replace(".", ",").replace("X", "."))
    #
    # with col3b:
    #     with st.container(border=True):
    #         st.metric('Custo Médio', f'💰 R$ {custo_medio_total_df_pos_atual:,.2f}'.replace(
    #             ",", "X").replace(".", ",").replace("X", "."),
    #                   help="""
    #                     - Soma de todas as compras.
    #                     - Quando há venda, se subtrai o valor de 'Preço Médio * Qtd Vendida'.
    #                     """
    #                   )
    #
    #     # with st.container(border=True):
    #     #     st.metric('Yield on Cost', f'🪙 {yield_total_df_pos_atual:,.2f}%')
    #
    #     with st.container(border=True):
    #         st.metric('Resultado de Vendas', f'💵 R$ {res_vendas_total_df_pos_atual:,.2f}'.replace(
    #             ",", "X").replace(".", ",").replace("X", "."))
    #
    # with col4b:
    #     with st.container(border=True):
    #         st.metric('Patrimônio Atual', f'🏦 R$ {patrimonio_atual_total_df_pos_atual:,.2f}'.replace(
    #             ",", "X").replace(".", ",").replace("X", "."))
    #
    #     with st.container(border=True):
    #         st.metric('Remunerações', f'🪙 R$ {remuneracoes_total_df_pos_atual:,.2f}'.replace(
    #             ",", "X").replace(".", ",").replace("X", "."))
    #
    #     with st.container(border=True):
    #         st.metric('Taxa Interna de Retorno', f'💹 {tir_total_df_pos_atual:,.2f}%')  # 🧮📉
