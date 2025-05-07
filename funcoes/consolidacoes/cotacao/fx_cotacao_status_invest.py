# # lista_manual_tickers = ['BBAS3', 'TAEE11', 'BRBI11', 'CSMG3', 'PETR4', 'VALE3', 'BBSE3', 'ISAE4', 'HASH11', 'IVVB11',
# #                         'MXRF11', 'HGLG11', 'MXRF11', 'BTLG11', 'GARE11', 'GGRC11', 'RECR11', 'CPTS11', 'HSLG11',
# #                         'XPLG11', 'XPML11', 'GTWR11', 'TAEE3', 'SAPR4', 'ITSA4']
#
# # -------------------------------------------------------------------------------------------------------------------
# Status Invest tem tabelas separadas para cada tipo de ativo, sendo assim cada tipo de ativo tem uma url diferente
# Todas funcionam no ambiente local mas dão erro na nuvem
# A última funçao desse aqruivo é a melhor adaptada
# # -------------------------------------------------------------------------------------------------------------------
import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

# # ------------------------------------------------------------------------------------------- fx busca em 1 url só
# def criar_df_cotacao_statusinvest(df_mov_financeiras):
#
#     # Obtendo os valores únicos da coluna 'ATIVO' e convertendo em uma lista
#     lista_tickers = df_mov_financeiras['Ativo'].unique().tolist()
#
#     url_base = "https://statusinvest.com.br/acoes/"
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
#         "Referer": "https://statusinvest.com.br"
#     }
#
#     dados = []
#
#     for ticker in lista_tickers:
#         url = f"{url_base}{ticker.lower()}"
#         try:
#             response = requests.get(url, headers=headers, timeout=10)
#             response.raise_for_status()
#
#             soup = BeautifulSoup(response.text, "html.parser")
#
#             # Procurar o primeiro elemento com classe que contém a cotação
#             cotacao_elemento = soup.find("strong", {"class": "value"})
#
#             if cotacao_elemento:
#                 texto = cotacao_elemento.get_text(strip=True)
#                 valor = float(texto.replace("R$", "").replace(".", "").replace(",", "."))
#             else:
#                 valor = None
#
#         except Exception as e:
#             print(f"Erro ao obter {ticker}: {e}")
#             valor = None
#
#         dados.append({
#             "Ticker": ticker,
#             "Preço": valor
#         })
#
#         sleep(0.5)  # pausa para evitar bloqueio
#
#     return pd.DataFrame(dados)


# # ----------------------------------------------------------------------fx busca todos os 3 tipos de ativos em 3 urls

# def criar_df_cotacao_statusinvest(df_mov_financeiras):
#
#     # Obtendo os valores únicos da coluna 'ATIVO' e convertendo em uma lista
#     lista_tickers = df_mov_financeiras['Ativo'].unique().tolist()
#
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
#         "Referer": "https://statusinvest.com.br"
#     }
#
#     dados = []
#
#     for ticker in lista_tickers:
#         urls = [
#             f"https://statusinvest.com.br/acoes/{ticker.lower()}",
#             f"https://statusinvest.com.br/fundos-imobiliarios/{ticker.lower()}",
#             f"https://statusinvest.com.br/etfs/{ticker.lower()}"
#         ]
#
#         valor = None
#
#         for url in urls:
#             try:
#                 response = requests.get(url, headers=headers, timeout=10)
#                 response.raise_for_status()
#
#                 soup = BeautifulSoup(response.text, "html.parser")
#
#                 # Procurar o primeiro elemento com classe que contém a cotação
#                 cotacao_elemento = soup.find("strong", {"class": "value"})
#
#                 if cotacao_elemento:
#                     texto = cotacao_elemento.get_text(strip=True)
#                     valor = float(texto.replace("R$", "").replace(".", "").replace(",", "."))
#                     break  # se achou, não tenta as próximas URLs
#             except Exception as e:
#                 print(f"Tentativa falhou para {ticker} na URL: {url} | Erro: {e}")
#                 continue
#
#         # Adicionando à lista de dados para o DataFrame
#         dados.append({
#             "Ticker": ticker,
#             "Preço": valor
#         })
#
#         sleep(0.5)  # pausa para evitar bloqueio
#
#     return pd.DataFrame(dados)


# # ------------------------------------------------------------- fx acha tipo de ativo antes e procura na url corresp.


def criar_df_cotacao_statusinvest(df_mov_financeiras):

    # Obtendo os valores únicos da coluna 'ATIVO' e convertendo em uma lista de tuplas (ticker, tipo)
    lista_tickers = df_mov_financeiras[['Ativo', 'Tipo de Ativo']].drop_duplicates().values.tolist()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": "https://statusinvest.com.br"
    }

    dados = []

    for ticker, tipo in lista_tickers:

        # Definindo a URL com base no tipo de ativo
        if tipo == 'Ação':
            url = f"https://statusinvest.com.br/acoes/{ticker.lower()}"
        elif tipo == 'FII':
            url = f"https://statusinvest.com.br/fundos-imobiliarios/{ticker.lower()}"
        elif tipo == 'ETF':
            url = f"https://statusinvest.com.br/etfs/{ticker.lower()}"
        else:
            url = None  # Tipo indefinido, pode ser tratado conforme necessário

        valor = None

        if url:
            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, "html.parser")

                # Procurar o primeiro elemento com classe que contém a cotação
                cotacao_elemento = soup.find("strong", {"class": "value"})

                if cotacao_elemento:
                    texto = cotacao_elemento.get_text(strip=True)
                    valor = float(texto.replace("R$", "").replace(".", "").replace(",", "."))

            except Exception as e:
                print(f"Tentativa falhou para {ticker} na URL: {url} | Erro: {e}")

        # Adicionando à lista de dados para o DataFrame
        dados.append({
            "Ticker": ticker,
            "Preço": valor
        })

        sleep(2)  # pausa para evitar bloqueio

    return pd.DataFrame(dados)
