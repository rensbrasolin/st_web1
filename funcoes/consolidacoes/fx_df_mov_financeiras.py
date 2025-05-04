# É o df_mov sem os "outros eventos". Esse df precisa ser criado para excluir todos os tickers de outros eventos.

def criar_df_mov_financeiras(df_movimentacoes):

    lista_outros_eventos = [
        "Direitos de Subscrição - Não Exercido",
        "Cessão de Direitos - Solicitada",
        "Cessão de Direitos",
        "Direito de Subscrição",
        "Atualização",
        "Desdobro"
    ]

    df_mov_financeiras = df_movimentacoes[~df_movimentacoes['Movimentação'].isin(lista_outros_eventos)]

    return df_mov_financeiras