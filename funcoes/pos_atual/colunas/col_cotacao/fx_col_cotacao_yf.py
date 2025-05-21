# Sempre funcionou localmente. Assim que implementei na nuvem ela funcionou, mas depois de alguns dias testando,
# começou a travar na nuvem e depois travou local também, tanto no projeto web quanto no local.


import yfinance as yf

def criar_df_cotacao_yf(df_mov_financeiras):

    lista_tickers = df_mov_financeiras['Ativo'].unique().tolist()

    # Acrescentando ".SA" a cada elemento da lista e ordenando para que fique na sequência padrão.
    lista_tickers_yf = [ativo + ".SA" for ativo in sorted(lista_tickers)]

    data_api = '2025-05-15' # Se for usar, precisa deixar isso dinâmico.

    df_cotacao_yf = yf.download( # yf.download não precisa de tratamento caso não encontre um ticker, pois ele preenche None e cotinua funcionando.
        lista_tickers_yf,
        start=data_api,
        auto_adjust=False, # Se for cruzar dados c/ div em separado, deixar auto_adjust=False é melhor, senão conta o div duas vezes.
        progress=False, # barra de progresso
    )['Close']  # Escolhe coluna

    return df_cotacao_yf


# --------------------------------------------------------------- Mesma estrutura da fx acima, mas pega 1 cotação por vez
# import yfinance as yf
# import pandas as pd
# import time
#
# def criar_df_cotacao_yf(df_mov_financeiras):
#     lista_tickers = df_mov_financeiras['Ativo'].unique().tolist()
#
#     # Acrescentando ".SA" a cada elemento da lista e ordenando para que fique na sequência padrão.
#     lista_tickers_yf = [ativo + ".SA" for ativo in sorted(lista_tickers)]
#
#     data_api = '2025-05-15'  # Se for usar, precisa deixar isso dinâmico.
#
#     # DataFrame vazio para armazenar os dados
#     df_cotacao_yf = pd.DataFrame()
#
#     for ticker in lista_tickers_yf:
#         try:
#             df_ticker = yf.download(
#                 ticker,
#                 start=data_api,
#                 auto_adjust=False,
#                 progress=False,
#             )['Close']
#
#             df_cotacao_yf[ticker] = df_ticker  # adiciona como nova coluna
#
#         except Exception as e:
#             print(f"Erro ao baixar {ticker}: {e}")
#
#         time.sleep(2)  # pausa de 2 segundos entre os downloads
#
#     return df_cotacao_yf
