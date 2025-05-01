# Listas usadas na fx criar_coluna_tipo_ativo para categorizar cada ativo.
# Usado dados ("Razão social") da CVM. Teste no jupyter na pasta 'Carteira'. Mais info lá.


# Listas de inclusão
lista_filtros_fiis = [
    'IMOB', 'FII', 'FIAGRO', 'FUNDO DE INVESTIMENTO', 'REAL ESTATE', ' FI ', 'RETROFITS', 'OFFICE', 'FUNDO DE INVEST',
    'FUNDO INVESTIMENTO', 'FUNDO DE INV', 'SHOPPING', 'SPX'
]

lista_filtros_acoes = [
    ' CIA', 'CIA ', ' CIA.', 'CIA.', ' S/A', ' S.A.', ' SA', ' S.A', ' S. A.', 'S.A. ', 'SA ', 'S.A.', 'S/A',
    'IND COM',  'COMPANHIA', 'COMPANHIIA', 'SOCIEDADE ANÔNIMA', 'INDUSTRIA', 'COMERCIO', 'LIQUIDAÇÃO',
    'TRUST DE RECEBIVEIS', 'CONSULTORIA', 'PATICIPACOES', 'PARTICIPAÇÕES', 'FINANC', 'SIDERURGICA'
]

lista_filtros_etfs = [
    'FUNDO DE INDICE', 'FUNDO DE ÍNDICE', 'ETF', 'INDEX', 'ÍNDICE', 'FDO IND', 'FDO. IND.', 'FDO DE INDI',
    'FDO DE IND', 'DE IND', 'IBOV', 'F. DE Í.'
]


# -------------------------------------------------------------------------------- # Listas de exclusão
# Se conter essas strings, não serão categorizadas como tal.
# Formadas por 2 listas dos outros 2 ativos, que não aquele.
# Mas não podem simplesmente ser as listas de inclusão somadas. Editar com cuidado pois é bem sensível.

lista_exclusao_fiis = ( # exclusão ações
        [' CIA', 'CIA ', ' CIA.', 'CIA.', ' S/A', ' S.A.', ' S.A', ' S. A.', 'S.A. ', 'S.A.', 'S/A', ' SA ',
         'IMOBILIÁRIOS SA', 'SHOPPING SA', 'IMOBILIARIO SA', 'IMOBILIARIA SA', 'IMOB SA', 'IMOBILIARIO SA',
         'SHOPPING CENTER SA', 'IMOBILIARIOS SA', 'BENS SA', 'IMOB. LTDA', 'SHOPPING CENTERS SA', 'TACARUNA SA',
         'AFONSO SA', 'PARTS SA', 'IND COM', 'COMPANHIA', 'COMPANHIIA', 'SOCIEDADE ANÔNIMA', 'COMERCIO', 'LIQUIDAÇÃO',
         'TRUST DE RECEBIVEIS', 'CONSULTORIA', 'PATICIPACOES', 'PARTICIPAÇÕES', 'SIDERURGICA']
        + # exclusão etfs
        ['FUNDO DE INDICE', 'FUNDO DE ÍNDICE', 'ETF', 'INDEX', 'FDO IND', 'FDO. IND.', 'FDO DE INDI', 'FDO DE IND',
         'DE IND', 'IBOV', 'F. DE Í.']
)

# ---------------------------
lista_exclusao_acoes = (
        ['FUNDO', 'FII'] # exclusão fiis
        + # exclusão etfs
        ['FUNDO DE INDICE', 'FUNDO DE ÍNDICE', 'ETF', 'INDEX', 'ÍNDICE', 'FDO IND', 'FDO. IND.', 'FDO DE INDI',
         'FDO DE IND', 'IBOV', 'F. DE Í.']
)

# ---------------------------
lista_exclusao_etfs = ( # exclusão fiis
        ['IMOB', 'FII', 'FIAGRO', 'FUNDO DE INVESTIMENTO', ' FI ', 'RETROFITS', 'OFFICE', 'FUNDO INVESTIMENTO']
        + # exclusão ações
        ['INDUSTRIA']
)

