# # lista_manual_tickers = ['BBAS3', 'TAEE11', 'BRBI11', 'CSMG3', 'PETR4', 'VALE3', 'BBSE3', 'ISAE4', 'HASH11', 'IVVB11',
# #                         'MXRF11', 'HGLG11', 'MXRF11', 'BTLG11', 'GARE11', 'GGRC11', 'RECR11', 'CPTS11', 'HSLG11',
# #                         'XPLG11', 'XPML11', 'GTWR11', 'TAEE3', 'SAPR4', 'ITSA4']
#
# # ----------------------------------------------------------------------------------------------------------------------
# Status Invest tem tabelas separadas para cada tipo de ativo, sendo assim cada tipo de ativo tem uma url diferente
# Eu poderia colocar um if tornando a variável url dinâmica respondendo conforme a clasificação de tipo de ativo que fiz.
# Porém se o ativo for classificado como 'Indefinido' daria erro. Então vou procurar todos os ativos em todas as urls

import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep


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





def criar_df_cotacao_statusinvest(df_mov_financeiras):

    # Obtendo os valores únicos da coluna 'ATIVO' e convertendo em uma lista
    lista_tickers = df_mov_financeiras['Ativo'].unique().tolist()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": "https://statusinvest.com.br"
    }

    dados = []

    for ticker in lista_tickers:
        urls = [
            f"https://statusinvest.com.br/acoes/{ticker.lower()}",
            f"https://statusinvest.com.br/fundos-imobiliarios/{ticker.lower()}",
            f"https://statusinvest.com.br/etfs/{ticker.lower()}"
        ]

        valor = None

        for url in urls:
            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, "html.parser")

                # Procurar o primeiro elemento com classe que contém a cotação
                cotacao_elemento = soup.find("strong", {"class": "value"})

                if cotacao_elemento:
                    texto = cotacao_elemento.get_text(strip=True)
                    valor = float(texto.replace("R$", "").replace(".", "").replace(",", "."))
                    break  # se achou, não tenta as próximas URLs
            except Exception as e:
                print(f"Tentativa falhou para {ticker} na URL: {url} | Erro: {e}")
                continue

        # Adicionando à lista de dados para o DataFrame
        dados.append({
            "Ticker": ticker,
            "Preço": valor
        })

        sleep(0.5)  # pausa para evitar bloqueio

    return pd.DataFrame(dados)
