def exibir_df_aggrid(df, tema='streamlit', altura=400): # Tema 'streamlit' muda conforme tema da pagina light/dark.
    from st_aggrid import AgGrid, GridOptionsBuilder
    # from st_aggrid.grid_options_builder import GridOptionsBuilder


    # Configurar a tabela para permitir filtros nas colunas
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(filter=True)  # Ativar filtro em todas as colunas
    grid_options = gb.build()

    # Exibir a tabela com filtros
    AgGrid(
        df,
        gridOptions=grid_options,
        theme=tema, # Há várias temas mas não estão fuincionando. por hora usar vazio ou streamlit.
        enable_enterprise_modules=True,
        fit_columns_on_grid_load=True, # Evita que a tabela fique com primeiras colunas curtas dentro do expander.
        height=altura,  # Altura da tabela (ajuste conforme necessário)
    )