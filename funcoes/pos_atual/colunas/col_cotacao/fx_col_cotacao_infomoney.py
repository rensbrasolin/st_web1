# Algumas poucas urls de tickers não são encontradas. Entre elas GARE11 e ISAE4 que tiveram troca de ticker recentemente.
# Então acredito ser algum problema da base do próprio site.
# Funciona local e na nuvem.

# ---------------------------------------------------------------------------------------------------------------------
import requests
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep

def criar_df_cotacao_infomoney(df_mov_financeiras):

    # Obtendo os valores únicos da coluna 'Ativo' e 'Tipo de Ativo' e convertendo em uma lista de listas
    lista_tickers = df_mov_financeiras[['Ativo', 'Tipo de Ativo']].drop_duplicates().values.tolist()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Referer": "https://www.infomoney.com.br/"
    }

    dados = []

    for ticker, tipo in lista_tickers:

        # É estranho pois a url é assim: https://www.infomoney.com.br/cotacoes/b3/acao/banco-do-brasil-bbas3/
        # Mas eu requisitando a url assim, eu tbm chego no endereço acima: https://www.infomoney.com.br/bbas3/
        url = f"https://www.infomoney.com.br/{ticker.lower()}"

        valor = None

        if url:
            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")

                # Escolhendo a classe correta com base no tipo de ativo
                if tipo == 'Ação' or tipo == 'ETF':
                    cotacao_elemento = soup.find("div", class_="value")
                    texto_bruto = cotacao_elemento.get_text(strip=True)
                    texto = texto_bruto[0:5]
                    valor = float(texto.replace("R$", "").replace(".", "").replace(",", "."))
                elif tipo == 'FII':
                    cotacao_elemento = soup.find("span", class_="typography__display--2-noscale typography--numeric spacing--mr1")
                    texto = cotacao_elemento.get_text(strip=True)
                    valor = float(texto.replace("R$", "").replace(".", "").replace(",", "."))
                else:
                    cotacao_elemento = None  # Tipo indefinido, não procuramos
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

# ---------------------------------------------------------------------------------------------------------------------
## Código para investigar formas de obter o arquivo através de NAME e CLASS

# import requests
# import pandas as pd
# from bs4 import BeautifulSoup
# from time import sleep
#
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
#     "Referer": "https://www.infomoney.com.br/"
# }
#
# # É estranho pois a url é assim: https://www.infomoney.com.br/cotacoes/b3/acao/banco-do-brasil-bbas3/
# # Mas eu requisitando a url assim, eu tbm chego no endereço acima: https://www.infomoney.com.br/bbas3/
# url = "https://www.infomoney.com.br/vale3"
#
# response = requests.get(url, headers=headers, timeout=10)
#
# soup = BeautifulSoup(response.text, "html.parser")
#
# # Procurar o elemento que contém a cotação (div com classe "value")
# cotacao_elemento = soup.find("div", class_="value") # classe para fiis="cotacoes__header-price" , ações e etfs "value"
#
# # soup
#
# cotacao_elemento
#
# texto = cotacao_elemento.get_text(strip=True)
#
#
# texto