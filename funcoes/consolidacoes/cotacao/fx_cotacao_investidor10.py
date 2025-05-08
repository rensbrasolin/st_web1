# Fx só ta pegando ações. Sendo que o elemento html de fiis e etfs é o mesmo que para ações.
# Testar na nuvem e se funcionar, talvez valha a pena tentar fazer fii e etf dar certo.

# import requests
# import pandas as pd
# from bs4 import BeautifulSoup
# from time import sleep
#
# def criar_df_cotacao_investidor10(df_mov_financeiras):
#     """
#     Função para buscar a cotação atual de uma lista de ativos no site Investidor10.
#     A URL acessada depende do tipo de ativo: Ação, FII ou ETF.
#     Classes para puxar elemento:
#         Descobri a classe pelo cod fonte, dando CTRL+f e procurando classes onde aparecem a cotação = da página.
#             Ação value
#             FII compare-progress-bar primary
#             ETF etfCurrentQuotation
#     """
#
#     # Obtendo os valores únicos da coluna 'Ativo' e 'Tipo de Ativo' e convertendo em uma lista de listas
#     lista_tickers = df_mov_financeiras[['Ativo', 'Tipo de Ativo']].drop_duplicates().values.tolist()
#
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
#         "Referer": "https://investidor10.com.br"
#     }
#
#     dados = []
#
#     for ticker, tipo in lista_tickers:
#
#         # Definindo a URL com base no tipo de ativo
#         if tipo == 'Ação':
#             url = f"https://investidor10.com.br/acoes/{ticker.lower()}/"
#         elif tipo == 'FII':
#             url = f"https://investidor10.com.br/fiis/{ticker.lower()}/"
#         elif tipo == 'ETF':
#             url = f"https://investidor10.com.br/etfs/{ticker.lower()}/"
#         else:
#             url = None  # Tipo indefinido, pode ser tratado conforme necessário
#
#         valor = None
#
#         if url:
#             try:
#                 response = requests.get(url, headers=headers, timeout=10)
#                 response.raise_for_status()
#
#                 soup = BeautifulSoup(response.text, "html.parser")
#
#                 # Procurar o elemento que contém a cotação (div com classe "value")
#                 cotacao_elemento = soup.find("div", class_="value")
#
#
#                 if cotacao_elemento:
#                     texto = cotacao_elemento.get_text(strip=True)
#                     valor = float(texto.replace("R$", "").replace(".", "").replace(",", "."))
#                 else:
#                     print(f"Cotação não encontrada para {ticker} na URL: {url}")
#
#             except Exception as e:
#                 print(f"Erro ao obter {ticker} na URL: {url} | Erro: {e}")
#
#         # Adicionando à lista de dados para o DataFrame
#         dados.append({
#             "Ticker": ticker,
#             "Preço": valor
#         })
#
#         sleep(1)  # pausa para evitar bloqueio
#
#     return pd.DataFrame(dados)

# ------------------------------------------------------------------------------------------------- manutenção da fx
# Estrutura para achar ativo mais direto ao ponto. Vai serivir pra ajudar a procurar a classe correta quando mudar.

# import requests
# import pandas as pd
# from bs4 import BeautifulSoup
# from time import sleep
#
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
#     "Referer": "https://investidor10.com.br"
# }
#
# url = "https://investidor10.com.br/fiis/hglg11"
#
# response = requests.get(url, headers=headers, timeout=10)
#
# soup = BeautifulSoup(response.text, "html.parser")
#
# # Procurar o elemento que contém a cotação (div com classe "value")
# cotacao_elemento = soup.find("div", class_="compare-progress-bar primary")
#
# # soup
#
# cotacao_elemento
#
# texto = cotacao_elemento.get_text(strip=True)
#
# texto

# ------------------------------------------------------------------------------------ Nova fxadaptada para cada classe
import requests
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep

def criar_df_cotacao_investidor10(df_mov_financeiras):
    """
    Função para buscar a cotação atual de uma lista de ativos no site Investidor10.
    A URL e classe do html acessada dependem do tipo de ativo: Ação, FII ou ETF.
    Classes para puxar elemento:
        Descobri a classe pelo cod fonte, dando CTRL+f e pesquisando cotação = da página. Lá peguei a classe.
            Ação class_="_card-body"
            FII class_="compare-progress-bar primary"
            ETF class_="etfCurrentQuotation"
    """

    # Obtendo os valores únicos da coluna 'Ativo' e 'Tipo de Ativo' e convertendo em uma lista de listas
    lista_tickers = df_mov_financeiras[['Ativo', 'Tipo de Ativo']].drop_duplicates().values.tolist()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Referer": "https://investidor10.com.br"
    }

    dados = []

    for ticker, tipo in lista_tickers:

        # Definindo a URL com base no tipo de ativo
        if tipo == 'Ação':
            url = f"https://investidor10.com.br/acoes/{ticker.lower()}/"
        elif tipo == 'FII':
            url = f"https://investidor10.com.br/fiis/{ticker.lower()}/"
        elif tipo == 'ETF':
            url = f"https://investidor10.com.br/etfs/{ticker.lower()}/"
        else:
            url = None  # Tipo indefinido, pode ser tratado conforme necessário

        valor = None

        if url:
            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, "html.parser")

                # Escolhendo a classe correta com base no tipo de ativo
                if tipo == 'Ação':
                    # Procurar o elemento que contém a cotação (div com classe "value")
                    cotacao_elemento = soup.find("div", class_="_card-body")
                elif tipo == 'FII':
                    # Procurar o elemento que contém a cotação (div com classe "compare-progress-bar primary")
                    cotacao_elemento = soup.find("div", class_="compare-progress-bar primary")
                elif tipo == 'ETF':
                    # Procurar o elemento que contém a cotação (div com classe "etfCurrentQuotation")
                    cotacao_elemento = soup.find("div", class_="etfCurrentQuotation")
                else:
                    cotacao_elemento = None  # Tipo indefinido, não procuramos

                # Se encontrou o elemento, extrair e converter o valor
                if cotacao_elemento:
                    texto = cotacao_elemento.get_text(strip=True)
                    valor = float(texto.replace("R$", "").replace(".", "").replace(",", "."))
                else:
                    print(f"Cotação não encontrada para {ticker} na URL: {url}")

            except Exception as e:
                print(f"Erro ao obter {ticker} na URL: {url} | Erro: {e}")

        # Adicionando à lista de dados para o DataFrame
        dados.append({
            "Ticker": ticker,
            "Preço": valor
        })

        sleep(1)  # pausa para evitar bloqueio

    return pd.DataFrame(dados)
