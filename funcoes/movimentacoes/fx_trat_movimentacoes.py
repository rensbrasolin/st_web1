import streamlit as st
import pandas as pd
from funcoes.movimentacoes.listas_tipo_ativo import ( # Listas usadas na fx criar coluna tipo ativo
    lista_filtros_fiis, lista_filtros_acoes, lista_filtros_etfs,
    lista_exclusao_fiis, lista_exclusao_acoes, lista_exclusao_etfs
)

# Usuário carregará 1 ou mais relaórios de movimentação
@st.cache_data
def unificar_extratos_em_df(arquivos):
    if arquivos:
        # Lê cada arquivo Excel e armazena os DataFrames numa lista com list comprehension.
        lista_dfs = [pd.read_excel(arquivo) for arquivo in arquivos]

        # Concatena todos os DataFrames em um único DataFrame. A ordem do carregamento não importa agora.
        df_movimentacoes = pd.concat(lista_dfs, ignore_index=True)

        return df_movimentacoes


# ______________________________________________________________________________________________________________________
def tratar_coluna_data(df_movimentacoes, coluna_data):
    df_movimentacoes[coluna_data] = pd.to_datetime(df_movimentacoes[coluna_data], dayfirst=True)

    return df_movimentacoes

# ______________________________________________________________________________________________________________________
# Converter as colunas numéricas corretamente para substituir o "-" por 0.
# Comentei o fillna pois ele transforma NaN em 0. Ir vendo com o tempo se é melhor que fique Nan ou 0.
def tratar_colunas_numericas(df_movimentacoes, lista_colunas_numericas):
    for coluna in lista_colunas_numericas:
        df_movimentacoes[coluna] = pd.to_numeric(df_movimentacoes[coluna], errors='coerce')#.fillna(0)

    return df_movimentacoes

# ______________________________________________________________________________________________________________________
# Aplica a transformação para valores negativos quando 'Entrada/Saída' for 'Debito'
def negativar_valores_debito(df_movimentacoes, lista_colunas_numericas):
    df_movimentacoes.loc[df_movimentacoes['Entrada/Saída'] == 'Debito', lista_colunas_numericas] *= -1

    return df_movimentacoes

# ______________________________________________________________________________________________________________________
def criar_coluna_ativo(df_movimentacoes):
    # Extrair o código do ativo da coluna 'Produto' e criar uma nova coluna 'Ativo'
    df_movimentacoes['Ativo'] = df_movimentacoes['Produto'].str.split(' ').str[0]

    # Reorganizar as colunas para que 'Ativo' seja a primeira
    df_movimentacoes = df_movimentacoes[['Ativo'] + list(df_movimentacoes.columns.difference(['Ativo']))]

    return df_movimentacoes

# ______________________________________________________________________________________________________________________
# Importa 6 listas de outro arquivo
def criar_coluna_tipo_ativo(df_movimentacoes):
    # Função interna para definir o tipo de ativo
    def definir_tipo_ativo(produto):
        if (
            any(filtro in produto for filtro in lista_filtros_fiis) and
            not any(excluir in produto for excluir in lista_exclusao_fiis)
        ):
            return 'FII'
        elif (
            any(filtro in produto for filtro in lista_filtros_acoes) and
            not any(excluir in produto for excluir in lista_exclusao_acoes)
        ):
            return 'Ação'
        elif (
            any(filtro in produto for filtro in lista_filtros_etfs) and
            not any(excluir in produto for excluir in lista_exclusao_etfs)
        ):
            return 'ETF'
        else:
            return 'Indefinido'  # Caso não se encaixe em nenhuma categoria

    # Criar a nova coluna usando a função interna
    df_movimentacoes['Tipo de Ativo'] = df_movimentacoes['Produto'].apply(definir_tipo_ativo)

    # Reorganizar as colunas para que 'Tipo de Ativo' seja a primeira
    df_movimentacoes = df_movimentacoes[['Tipo de Ativo'] + list(df_movimentacoes.columns.difference(['Tipo de Ativo']))]

    return df_movimentacoes

# ______________________________________________________________________________________________________________________
# Usa o nome completo da empresa da coluna 'Produto' para alterar apenas as colunas 'Ativo' anteriores a data de atualização
def atualizar_ticker(df_movimentacoes):
    # Filtrar linhas onde a "Movimentação" é "Atualização"
    atualizacoes = df_movimentacoes[df_movimentacoes["Movimentação"] == "Atualização"]

    # Iterar sobre cada linha de atualização
    for index, row in atualizacoes.iterrows():
        # Extrair o nome completo do ativo da coluna "Produto"
        nome_completo = row["Produto"].split(" - ")[1]
        novo_ticker = row["Ativo"]
        data_atualizacao = row["Data"]

        # Filtrar linhas anteriores à data da atualização e que contenham o mesmo nome completo no "Produto"
        linhas_para_atualizar = (df_movimentacoes["Produto"].str.contains(nome_completo)) & \
                                (df_movimentacoes["Data"] < data_atualizacao)

        # Atualizar a coluna "Ativo" nas linhas filtradas
        df_movimentacoes.loc[linhas_para_atualizar, "Ativo"] = novo_ticker

    return df_movimentacoes

# ______________________________________________________________________________________________________________________
# O desdobramento é apenas a correção (ajuste) de quantidade (*2) e preço unitário (/2).
# Ele é aplicado partindo da data do desdobro e voltando até o início. Em todas as movimentações daquele ticker.
# Se tiver mais de 1 desdobro do mesmo ticker, o código vai "ajustar 2x" as movimentações anteriores ao primeiro desdobro. Mas na minha lógica, acredito ser isso mesmo o correto.
# Assim que acontecer o primeiro agrupamento da carteira, tenho que aplicar aqui da mesma forma. Acredito que seja só pegar esse código, aplicar o mesmo filtro e inverter o cálculo.
def aplicar_desdobro(df_movimentacoes):
    # Itera sobre as linhas onde a coluna 'Movimentação' tem 'Desdobro', para ter em mãos o ativo e a data do desdobro.
    for index, row in df_movimentacoes[df_movimentacoes['Movimentação'] == 'Desdobro'].iterrows():
        ativo = row['Ativo']
        data_desdobro = row['Data']

        # Aplica o filtro para pegar as linhas do mesmo ativo, com data anterior ao desdobro e mantendo só trasnf-liq.
        mask = (
            (df_movimentacoes['Ativo'] == ativo) &
            (df_movimentacoes['Data'] <= data_desdobro)
        )

        # Aplica o desdobramento
        df_movimentacoes.loc[mask, 'Preço unitário'] /= 2
        df_movimentacoes.loc[mask, 'Quantidade'] *= 2

    return df_movimentacoes




# apagar depois abaixo pois fxs foram para outro arquivo.

# _____________________________________________________________________________________________________________________
# _____________________________________________________________________________________________________________________
# # Não é obrigatório capturar a resposta de AgGrid como faço na variável grid_response. Mas nesse caso será feito
# # pois a tabela exibida precisará refletir os filtros.
# def exibir_df_mov_com_indicadores(df_movimentacoes, tema='streamlit', altura=400): # Tema 'streamlit' muda conforme tema da pagina light/dark.
#
#     # Configurar a tabela.
#     gb = GridOptionsBuilder.from_dataframe(df_movimentacoes)
#
#     # Ativar filtro em todas as colunas
#     gb.configure_default_column(filter=True)
#
#     # Identificar colunas float
#     colunas_numericas = df_movimentacoes.select_dtypes(include=['float']).columns
#     # Aplicar valueFormatter para colunas numéricas. Formato brasileiro.
#     for coluna in colunas_numericas:
#         gb.configure_column(
#             coluna,
#             valueFormatter="value.toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2})")
#
#     grid_options = gb.build()
#
#     # Exibir a tabela e capturar a resposta
#     grid_response = AgGrid(
#         df_movimentacoes,
#         gridOptions=grid_options,
#         theme=tema, # Há várias temas mas não estão fuincionando. por hora usar vazio ou streamlit.
#         enable_enterprise_modules=True,
#         fit_columns_on_grid_load=True, # Evita que a tabela fique com primeiras colunas curtas dentro do expander.
#         height=altura,  # Altura da tabela (ajuste na chamada da fx, conforme necessário)
#         reload_data=True
#     )
#
#     # Capturar o DataFrame filtrado. Criando um novo df para que o def_mov fique intacto, já que será usado na pagina.
#     df_mov_filtrado = grid_response['data']
#
#     return df_mov_filtrado
#
# # ==================================================================================== Indicadores
#
#     # # Calcular o total da coluna "Valor da Operação"
#     # total = df_mov_filtrado['Valor da Operação'].sum()
#     # # Mostrar o indicador no topo
#     # st.metric("Volume", f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
#
#
#
#     ######## Cartões:
#     # Tipos de Ativos: qtde linhas unicas.
#     # Ativos: qtde linhas unicas, só letras (indice 0a3).
#     # Compras: valor com condição
#     # Vendas: valor com condição
#     # Remunerações: valor com condição

