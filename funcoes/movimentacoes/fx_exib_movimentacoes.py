import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder


# Não é obrigatório capturar a resposta de AgGrid como faço na variável grid_response. Mas nesse caso será feito
# pois a tabela exibida precisará refletir os filtros.
def exibir_df_mov_filtrado(df_movimentacoes, tema='streamlit', altura=400): # Tema 'streamlit' muda conforme tema da pagina light/dark.

    # Configurar a tabela.
    gb = GridOptionsBuilder.from_dataframe(df_movimentacoes)

    # Ativar filtro em todas as colunas
    gb.configure_default_column(filter=True)

    # Identificar colunas float
    colunas_numericas = df_movimentacoes.select_dtypes(include=['float']).columns
    # Aplicar valueFormatter para colunas numéricas. Formato brasileiro.
    for coluna in colunas_numericas:
        gb.configure_column(
            coluna,
            valueFormatter="value.toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2})")

        # Formatar a coluna de data para exibir apenas a data
        gb.configure_column("Data", valueFormatter="new Date(value).toLocaleDateString('pt-BR')")

    grid_options = gb.build()

    # Exibir a tabela e capturar a resposta
    grid_response = AgGrid(
        df_movimentacoes,
        gridOptions=grid_options,
        theme=tema, # Há várias temas mas não estão fuincionando. por hora usar vazio ou streamlit.
        enable_enterprise_modules=True,
        fit_columns_on_grid_load=True, # Evita que a tabela fique com primeiras colunas curtas dentro do expander.
        height=altura,  # Altura da tabela (ajuste na chamada da fx, conforme necessário)
        reload_data=True,
    )

    # Capturar o DataFrame filtrado. Criando um novo df para que o def_mov fique intacto, já que será usado na pagina.
    df_mov_filtrado = grid_response['data']

    return df_mov_filtrado

# ==================================================================================== Indicadores
def calcular_compras(df_mov_filtrado):
    filtro = ((df_mov_filtrado['Entrada/Saída'] == 'Credito') &
              (df_mov_filtrado['Movimentação'] == 'Transferência - Liquidação'))

    total_compras = df_mov_filtrado.loc[filtro, 'Valor da Operação'].sum()

    st.metric('Compras', f"💸 R$ {total_compras:,.2f}"
              .replace(",", "X").replace(".", ",").replace("X", "."))

# ---------------------------------------------------------------------------------------------------------------------
def calcular_vendas(df_mov_filtrado):
    filtro = ((df_mov_filtrado['Entrada/Saída'] == 'Debito') &
              (df_mov_filtrado['Movimentação'] == 'Transferência - Liquidação'))

    total_vendas = df_mov_filtrado.loc[filtro, 'Valor da Operação'].sum() *-1 #*-1 pra não ficar (-)

    st.metric('Vendas', f"💵 R$ {total_vendas:,.2f}"
              .replace(",", "X").replace(".", ",").replace("X", "."))

# ---------------------------------------------------------------------------------------------------------------------
def calcular_remuneracoes(df_mov_filtrado):
    filtro = ((df_mov_filtrado['Movimentação'] == 'Dividendo') |
             (df_mov_filtrado['Movimentação'] == 'Juros Sobre Capital Próprio') |
             (df_mov_filtrado['Movimentação'] == 'Rendimento')
              ) # Se tiver mais, acrescentar conforme for descobrindo

    total_remuneracoes = df_mov_filtrado.loc[filtro, 'Valor da Operação'].sum()

    st.metric('Remunerações', f"🪙 R$ {total_remuneracoes:,.2f}" # 💰
              .replace(",", "X").replace(".", ",").replace("X", "."),
              help="""
              - Dividendo
              - Juros Sobre Capital Próprio
              - Rendimento"""
              )

