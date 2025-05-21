import streamlit as st


# Configurar o layout da página para ocupar toda a largura
st.set_page_config(layout="wide") # Fiz isso pra tabela não ficar pequena e com scroll horizontal.


# Menu
# Inicialmente terá uma página só devido a base ser carregado pelo usuario em tempo real.
# Mas dequalquer forma vou deixar um modelo de multipaginss comentado
menu = st.navigation(
    {
        '# Título do Menu': [st.Page('paginas/pagina.py', title='- Consolidação Carteira B3')],

        # '# 1. Consolidação do Extrato de Movimentações B3': [
        #     st.Page('paginas/movimentacoes/pg_mov_completo.py', title='- Extrato Completo (a+b)'),
        #     st.Page('paginas/movimentacoes/pg_mov_financeiras.py', title='- Movimentações Financeiras (a)'),
        #     st.Page('paginas/movimentacoes/pg_mov_eventos.py', title='- Outros Eventos (b)')
        # ],
        #
        # '# 2. Consolidações': [
        #     st.Page('paginas/pos_atual/pg_consolidacao_carteira.py', title='- Posição Atual'),
        #     st.Page('paginas/pos_atual/pg_rem.py', title='- Remunerações')
        # ],
    }
)

menu.run()