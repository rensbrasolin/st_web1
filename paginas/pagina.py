import time

import streamlit as st
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

st.title("📊 Invest View")
st.write(" #### 🔎 Consolidação do Extrato de Movimentações da B3")

# -----------------------------------------------------------------------------------------------------------------


with st.expander("📂 Carregamento dos dados", expanded=True): # Comentar e manter apenas para manutenção
    with st.container(border=True):
        # Usuário carregará 1 ou mais arquivos de extrato de movimentação
        arquivos = st.file_uploader("Carregue seus extratos de movimentação aqui, sendo 1 arquivo para cada ano:",
                                    type=["xlsx", "xls"], accept_multiple_files=True)


if arquivos: # If para não aparecer um df vazio de início

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

# -----------------------------------------------------------------------------------------------------------------
#     Expanded para Inicar aberto para carregar aggrid corretamente
    with st.expander("📃 Extrato de Movimentações B3", expanded=True):
        st.text("Info", help="Aplique filtros na tabela para que os indicadores abaixo se ajustem.")  # ℹ️
        # Nesse caso, ao chamar a fx, já é criado e exibido o df
        with st.container(border=True):
            # st.write('Aplique filtros na tabela para que os indicadores abaixo se ajustem')
            df_mov_filtrado = exibir_df_mov_filtrado(df_movimentacoes)#, tema="balham-dark")

        # Criando colunas dentro do expander ------ Indicadores:
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







# ===============================================================================================

    # -----------------------------------------------------TESTES:-------------------------------------------
    # Obtendo os valores únicos da coluna 'ATIVO' e convertendo em uma lista
    lista_principal_tickers = df_movimentacoes['Ativo'].unique().tolist()

    # ---------------------

    with st.expander("Teste de cotação YF", expanded=True):  # ExpTeste
        import yfinance as yf  # cotação

        # Acrescentando ".SA" a cada elemento da lista e ordenando para que fique na sequência padrão.
        lista_tickers_yf = [ativo + ".SA" for ativo in sorted(lista_principal_tickers)]

        # lista_ativos = ['BBAS3.SA', 'TAEE11.SA', 'BRBI11.SA', 'CSMG3.SA', 'PETR4.SA', 'VALE3.SA', 'BBSE3.SA',
        #                 'ISAE4.SA', 'HASH11.SA', 'IVVB11.SA', 'MXRF11.SA', 'HGLG11.SA']

        data_api = '2025-05-02'

        df_cotacao_yf = yf.download(
            lista_tickers_yf,
            start=data_api,
            auto_adjust=False, # Se for cruzar dados c/ div em separado, deixar auto_adjust=False é melhor, senão conta o div duas vezes.
            progress=False, # barra de progresso
        )['Close']  # Escolhe coluna
        df_cotacao_yf













      # ------------------------------------------------------teste 2 tradingview com requests

    with st.expander("Teste de cotação Trading View", expanded=True):  # ExpTeste2

        import requests
        import json
        import pandas as pd
        from time import sleep

        url = "https://scanner.tradingview.com/brazil/scan"

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/json",
            "Referer": "https://br.tradingview.com/"
        }

        lista_tickers_tv = ['BBAS3', 'TAEE11', 'BRBI11', 'CSMG3', 'PETR4', 'VALE3', 'BBSE3', 'ISAE4', 'HASH11', 'IVVB11', 'MXRF11', 'HGLG11', 'MXRF11', 'BTLG11', 'GARE11',
                            'GGRC11', 'RECR11', 'CPTS11', 'HSLG11', 'XPLG11', 'XPML11', 'GTWR11', 'TAEE3', 'SAPR4', 'ITSA4']



        # Lista para armazenar os dados de todos os tickers
        dados = []

        for ticker in lista_tickers_tv:
            payload = {
                "symbols": {
                    "tickers": [f"BMFBOVESPA:{ticker}"],  # Pode colocar BBAS3, PETR4, etc
                    "query": {"types": []}
                },
                "columns": ["close", "name"]  # Aqui consigo pegar mais dados, preenchendo o nome dele aqui conforme doc API
            }

            response = requests.post(url, headers=headers, data=json.dumps(payload))
            data = response.json()

            # Atribuindo os dados pegos a variáveis
            resultados = data['data'][0]['d']
            preco_atual = resultados[0]
            # nome = resultados[1]

            # Adicionando à lista de dados para o DataFrame
            dados.append({
                "Ticker": ticker,
                "Preço": preco_atual
                # "Nome": nome  # Caso queira incluir, é só descomentar
            })

            sleep(0.5)

        # Criando o DataFrame final
        df_resultados = pd.DataFrame(dados)
        st.dataframe(df_resultados)

    # ------------------------------------------------------






# próximos passos:
# a versão publica está só com teste 2 YF que deu errado

# provavelmente consigo com fundamentus, mas lá não tem ETF´s
# tenho que pensar melhor como fazer isso.




# -----------------------------
# Quando for criar o df_mov_financeiras, talvez seja melhor usar a mesma fx que cria o df_mov, mas já com o nome df_mov_fin,
# pois assim é um jeito de o df_mov_fin ser totalmente independente do df_mov. Se for mesmo fazer isso, depois por obs na fx:
# informando que ela é usada como ponto de partida dos dfs mov e mov_fin. Mas antes tentar pegar o df_mov pronto mesmo pois
# acho que dá


# Informar que dados estão seguros


