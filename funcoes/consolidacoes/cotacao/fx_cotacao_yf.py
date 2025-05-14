# Sempre funcionou localmente. Assim que implementei na nuvem ela funcionou, mas depois de alguns dias testando,
# começou a travar na nuvem e depois travou local também, tanto no projeto web quanto no local.


import yfinance as yf

def criar_df_cotacao_yf(df_mov_financeiras):

    lista_tickers = df_mov_financeiras['Ativo'].unique().tolist()

    # Acrescentando ".SA" a cada elemento da lista e ordenando para que fique na sequência padrão.
    lista_tickers_yf = [ativo + ".SA" for ativo in sorted(lista_tickers)]

    data_api = '2025-05-02' # Se for usar, precisa deixar isso dinâmico.

    df_cotacao_yf = yf.download( # yf.download não precisa de tratamento caso não encontre um ticker, pois ele preenche None e cotinua funcionando.
        lista_tickers_yf,
        start=data_api,
        auto_adjust=False, # Se for cruzar dados c/ div em separado, deixar auto_adjust=False é melhor, senão conta o div duas vezes.
        progress=False, # barra de progresso
    )['Close']  # Escolhe coluna

    return df_cotacao_yf

