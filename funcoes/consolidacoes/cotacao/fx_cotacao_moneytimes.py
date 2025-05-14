



# -------------------------------------------------------------------------------------------------------------------
import requests
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep


def criar_df_cotacao_moneytimes(df_mov_financeiras):

    # Obtendo os valores únicos da coluna 'ATIVO' e convertendo em uma lista
    lista_tickers = df_mov_financeiras['Ativo'].unique().tolist()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Referer": "https://www.moneytimes.com.br/"
    }

    dados = []

    for ticker in lista_tickers:

        url = f"https://www.moneytimes.com.br/cotacao/{ticker.lower()}/"

        valor = None

        if url:
            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, "html.parser")

                cotacao_elemento = soup.find("div", class_="valor")

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