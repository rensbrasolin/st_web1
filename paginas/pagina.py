# from idlelib.configdialog import font_sample_text

import streamlit as st
from st_aggrid import AgGrid

from funcoes.movimentacoes.fx_trat_movimentacoes import (
    unificar_extratos_em_df,
    tratar_coluna_data,
    tratar_colunas_numericas,
    negativar_valores_debito,
    criar_coluna_tipo_ativo,
    criar_coluna_ativo,
    atualizar_ticker,
    aplicar_desdobro,
)
from funcoes.movimentacoes.fx_exib_movimentacoes import (
    exibir_df_mov_filtrado,
    calcular_compras,
    calcular_vendas,
    calcular_remuneracoes,
)

from funcoes.pos_atual.fx_df_mov_financeiras import criar_df_mov_financeiras
from funcoes.pos_atual.fx_df_pos_atual import (
    criar_df_pos_atual,
    exibir_df_pos_atual_aggrid,
    aplicar_filtro_posicao_zerada_df_pos_atual,
    aplicar_filtro_tipo_df_pos_atual,
    criar_medidas_df_pos_atual,
    exibir_medidas_df_pos_atual
)

# Especialmente calculada aqui para sofrer influencia dos filtros
from funcoes.pos_atual.colunas.col_consolidadas.fx_col_consolidadas_tir import criar_tir_total_df_pos_atual



st.title("📊 Minha Carteira")
st.write('##### Análise da carteira de renda variável através do seu Extrato de Movimentações da B3 ')
st.markdown("---")

# --------------------------------------------------------------------------------------- INSTRUÇÕES E COMENTÁRIOS - 0
with st.expander("# 📘 Instruções e Comentários sobre a Aplicação", expanded=False):

    # st.markdown("---")

    with st.container(border=True):
        st.markdown("""
        Esta aplicação tem como objetivo **analisar automaticamente carteiras de investimentos** compostas por ativos
         listados na B3 — atualmente, são suportados **Ações, ETFs e Fundos Imobiliários (FIIs)**. Para isso, basta que
          você carregue seu **arquivo Excel do Extrato de Movimentações** da corretora.
    
        🔒 **Seus dados são processados localmente.** Nenhuma informação do extrato é armazenada, garantindo
         **total privacidade e segurança**.
    
        📉 O extrato não informa taxas e impostos (Clearing, Bolsa, Corretagem/Despesas), portanto, os cálculos são
         realizados com base apenas nos **valores líquidos** das operações.
    
        ⚙️ A aplicação foi construída com o objetivo de ser adaptável a diferentes situações. Atualmente, ela já trata
         eventos como **desdobramentos e atualizações de ticker**. No entanto, por enquanto, ela foi testada apenas
          com o meu próprio extrato, que inclui operações simples (compras, vendas e recebimento de proventos).
    
        🚧 Por isso, **certas movimentações ainda não são reconhecidas**, como:
        - Bonificações em ativos;
        - Direitos de subscrição;
        - Operações com opções;
        - Aluguel de ações.
    
        Se a aplicação apresentar erros, uma boa alternativa é **filtrar seu extrato apenas por FIIs** no momento
         do download. Isso costuma evitar falhas.
    
        📌 A classificação de cada ativo é feita com base em critérios lógicos. Caso algum ativo não seja identificado
         corretamente, ele será marcado como **“Indefinido”**.  
    
        🎯 Cada **seção da aplicação é independente**, e seus **filtros afetam apenas os dados visíveis naquela seção**.
        """)

# ------------------------------------------------------------------------------------------------- CARREGANDO ARQ - 1


with st.expander("📂 Carregamento dos dados", expanded=False):

    st.metric(label="ℹ️", value="", help="""
    # Carregamento dos dados\n
    Baixe seu Extrato de Movimentações:
    - Acesse o site da B3: https://www.b3.com.br/pt_br/para-voce
    - No site da B3, clique em 'Área do Investidor', ou acesse direto: https://www.investidor.b3.com.br/
        - Faça login ou crie seu acesso
    - Dentro da 'Área do Investidor', no menu principal, clique em "Extratos"
    - Em "Extratos", clique em "Movimentação"
    - Em "Movimentação", clique e abra o filtro
    - No filtro:
        - Escolha Data Inicial e Data Final para selecionar o período desejado
            - Para o correto funcionamento da aplicação, é obrigatório que o extrato contemple todo o período da carteira
        - Na seção "Tipo de Investimento", selecione apenas Ações, ETFs e FIIs
        - Clique em 'Filtrar'
    - E por fim, clique em 'Baixar' e salve o arquivo em seu PC
        """)

    # st.markdown("---")

    with st.container(border=True):
        # Usuário carregará 1 ou mais arquivos de extrato de movimentação
        arquivos = st.file_uploader("Carregue aqui o seu Extrato de Movimentações",
                                    type=["xlsx", "xls"], accept_multiple_files=True)

# ------------------------------------------------------------------------------------------------- CRIANDO DF MOV - 2a

# If para não aparecer um df vazio de início.
# Todu o resto do cód tem que estar dentro desse if, obrigatoriamente. Sem df_mov não há app.
if arquivos:

    # Cria o df_mov
    df_movimentacoes = unificar_extratos_em_df(arquivos)
    # with st.expander("Dados carregados"): # Comentar e manter apenas para manutenção
    #     st.dataframe(df_movimentacoes)


    df_movimentacoes = tratar_coluna_data(df_movimentacoes,'Data')
    # st.dataframe(df_movimentacoes)

    df_movimentacoes = tratar_colunas_numericas(df_movimentacoes, ['Preço unitário', 'Quantidade', 'Valor da Operação'])
    # st.dataframe(df_movimentacoes)

    df_movimentacoes = negativar_valores_debito(df_movimentacoes, ['Preço unitário', 'Quantidade', 'Valor da Operação'])
    # st.dataframe(df_movimentacoes)

    df_movimentacoes = criar_coluna_ativo(df_movimentacoes)
    # st.dataframe(df_movimentacoes)

    df_movimentacoes = criar_coluna_tipo_ativo(df_movimentacoes)
    # st.dataframe(df_movimentacoes)

    df_movimentacoes = atualizar_ticker(df_movimentacoes)
    # st.dataframe(df_movimentacoes)

    df_movimentacoes = aplicar_desdobro(df_movimentacoes)
    # st.dataframe(df_movimentacoes)

# ------------------------------------------------------------------------------------------------- EXIBINDO DF MOV - 2b
#     Expanded para Inicar aberto para carregar aggrid corretamente
    with st.expander("📃 Extrato de Movimentações", expanded=True):
        st.metric(label="ℹ️", value="", help="""
        # Extrato de Movimentações
        Clique nos botões ao lado dos títulos de cada coluna e customize a tabela interativa:
        - Arraste colunas
        - Reordene os dados conforme a coluna desejada
        - Aplique filtros em linhas e colunas que os indicares abaixo se ajustarão
        """)

        # st.markdown("---")

        # Nesse caso, ao chamar a fx, já é criado e exibido o df aggrid
        # with st.container(border=True):
        df_mov_filtrado = exibir_df_mov_filtrado(df_movimentacoes)#, tema="balham-dark")

        # st.markdown("---")

        # Criando colunas dentro do expander ------ Indicadores do df_mov:
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            with st.container(border=True):
                calcular_compras(df_mov_filtrado)

        with col2:
            with st.container(border=True):
                calcular_vendas(df_mov_filtrado)

        with col3:
            with st.container(border=True):
                calcular_remuneracoes(df_mov_filtrado)

# -------------------------------------------------------------------------------------- CRIANDO DF MOV_FINANCEIRAS - 3

    # Não pôr expander pois df não será exibido para usuário
    df_mov_financeiras = criar_df_mov_financeiras(df_movimentacoes)
    # st.write('Tabela de Movimentações Financeiras') # Comentar e manter apenas para manutenção
    # st.dataframe(df_mov_financeiras)

# ------------------------------------------------------------------------------------------- CRIANDO DF_POS_ATUAL - 4a

    with st.expander("🔎 Posição Atual", expanded=True):
        st.metric(label="ℹ️", value="", help="""
        # Posição Atual
        - Visualize a Posição Atual da Carteira como um todo, ou filtre por ativo
        - Indicadores, tabela, e gráficos serão ajustados pelo filtro
        """)

        st.markdown("---")

        # Criado logo antes do filtro e exibido só após os indicadores
        df_pos_atual = criar_df_pos_atual(df_mov_financeiras)

# ---------------------------------------------------------------------------------- APLICANDO FILTROS DF_POS_ATUAL - 4b

        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            with st.container(border=True):
                df_pos_atual = aplicar_filtro_posicao_zerada_df_pos_atual(df_pos_atual)
                st.markdown("---")
                df_pos_atual = aplicar_filtro_tipo_df_pos_atual(df_pos_atual)



        with col2:
            pass



        with col3:
            pass

        # st.markdown("---")

        # -------------------------------------------------------------------------------- INDICADORES/TOTAIS DF_POS_ATUAL - 4c

        (  # FX retorna todas as variáveis de totais, menor TIR
            qtd_ativos_total_df_pos_atual, # Essa até faz sentido mostrar.
            qtd_tipos_total_df_pos_atual, # # Não faz sentido, já que df pode ser filtrado.
            qtd_total_df_pos_atual,  # Não será usada provavelmente

            custo_medio_total_df_pos_atual,
            remuneracoes_total_df_pos_atual,
            res_vendas_total_df_pos_atual,
            patrimonio_atual_total_df_pos_atual,
            variacao_percentual_total_df_pos_atual,
            variacao_absoluta_total_df_pos_atual,
            yield_total_df_pos_atual,
            performance_absoluta_total_df_pos_atual,
            performance_percentual_total_df_pos_atual
        ) = criar_medidas_df_pos_atual(df_pos_atual)

        # Especialmente calculada aqui para sofrer influencia dos filtros do df_pos_atual
        tir_total_df_pos_atual = criar_tir_total_df_pos_atual(
            df_pos_atual, df_mov_financeiras, patrimonio_atual_total_df_pos_atual)


# ---------------------------------------- EXIBINDO INDICADORES/TOTAIS DF_POS_ATUAL
#         with st.container(border=True):  # Tirei o container para ter espaço
        exibir_medidas_df_pos_atual(
            qtd_ativos_total_df_pos_atual, # Essa até faz sentido mostrar.
            qtd_tipos_total_df_pos_atual, # Não faz muito sentido, já que df pode ser filtrado.
            qtd_total_df_pos_atual,  # Não será usada provavelmente

            custo_medio_total_df_pos_atual,
            remuneracoes_total_df_pos_atual,
            res_vendas_total_df_pos_atual,
            patrimonio_atual_total_df_pos_atual,
            variacao_percentual_total_df_pos_atual,
            variacao_absoluta_total_df_pos_atual,
            yield_total_df_pos_atual,
            performance_absoluta_total_df_pos_atual,
            performance_percentual_total_df_pos_atual,
            tir_total_df_pos_atual,
        )

        st.markdown("---")
# ------------------------------------------------------------------------------------------- EXIBINDO DF_POS_ATUAL - 4d

        # with st.container(border=True):
        # st.dataframe(df_pos_atual.round(2))

        exibir_df_pos_atual_aggrid(df_pos_atual)



# -------------------------------------------------------------------------------- EXIBINDO GRÁFICOS DODF_POS_ATUAL - 5

    st.markdown("---")



# ==========================================================================================================================================================================

    # -----------------------------------------------------TESTES:------------------------------------------











# ************************************************************************************************************
# próximos passos:


# imagem do ativo, provavelmnete só com aggrid, nessa hora ja decidir se será dataframe ou agrid
# "https://s3-symbol-logo.tradingview.com/vale--big.svg",
# "https://s3-symbol-logo.tradingview.com/brasileiro-petrobras--big.svg",
# "https://s3-symbol-logo.tradingview.com/banco-do-brasil--big.svg",
# "https://s3-symbol-logo.tradingview.com/hashdex--big.svg",








# -----------------------------
