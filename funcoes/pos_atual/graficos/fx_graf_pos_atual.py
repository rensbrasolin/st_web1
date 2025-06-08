import plotly.graph_objects as go
import plotly.express as px


# ------------------------------------------------------------------------------------------------------------ GRÁFICO 1
def criar_grafico_cm_pa_rem(df_pos_atual):
    # Ordenar os ativos
    df_pos_atual = df_pos_atual.sort_values(by='Custo Médio', ascending=False)

    fig = go.Figure()

    # Adicionar a barra de 'Custo Médio' (barra individual)
    fig.add_trace(go.Bar(
        x=df_pos_atual['Ativo'],
        y=df_pos_atual['Custo Médio'],
        name='Custo Médio',
        offsetgroup=1,  # Grupo de barras composto
        marker={"color": "#ef476f"} #d1495b 219ebc
    ))

    # Adicionar a barra de 'Patrimônio Atual' (base da barra composta)
    fig.add_trace(go.Bar(
        x=df_pos_atual['Ativo'],
        y=df_pos_atual['Patrimônio Atual'],
        name='Patrimônio Atual',
        offsetgroup=2,
        marker={"color": "#26547c"}, # 00798c 023047
        # Rótulo
        text=df_pos_atual['Variação %'].apply(lambda x: f'{x:.0f}%'),
        textposition='inside',  # Dentro da barra
        insidetextanchor='end',  # start middle end
        textangle=0,  # Mantém o texto na horizontal
        textfont={
            "family": "Segoe UI",  # Acrescentar 'Black' na 'Segoe UI' caso queira negrito
            "size": 9,
            "color": df_pos_atual['Variação %'].apply(lambda x: "#ffb3c1" if x < 0 else "#b7e4c7").tolist()
            # 52b788
        }
    ))

    # Adicionar a barra de 'Remunerações' (empilhada sobre 'Patrimônio Atual')
    fig.add_trace(go.Bar(
        x=df_pos_atual['Ativo'],
        y=df_pos_atual['Remunerações $'],
        name='Remunerações',
        base=df_pos_atual['Patrimônio Atual'],  # Começa no topo de 'Patrimônio Atual'
        offsetgroup=2,  # Mesmo grupo que 'Patrimônio Atual'
        marker={"color": "#ffd166"}, # edae49 ffb703
        visible='legendonly'  # Começa oculta no gráfico, mas visível na legenda
    ))

    # Ajustar layout
    fig.update_layout(
        barmode='group',  # Barras lado a lado
        plot_bgcolor='#0a0908',  # Fundo da área do gráfico #202020 #1d1e18 0a0908
        paper_bgcolor='#0a0908',  # Fundo geral (inclusive margens)
        margin={"l": 40, "r": 40, "t": 40, "b": 40},

        yaxis={  # Eixo Y (valores)
            "showgrid": True,
            "gridcolor": '#161a1d',
            "gridwidth": 1,
            "zeroline": False,
            'tickprefix': 'R$ ',
            'tickformat': ',.0f',  # separador de milhar e duas casas decimais
            'separatethousands': True,
            "tickfont": {  # Cor dos valores do eixo Y
                "color": "#adb5bd"
            }
        },
        xaxis={  # Eixo X (ativos)
            "tickfont": {  # Cor dos rótulos no eixo X
                "color": "#adb5bd",
                "size": 11,
            },
            "tickangle": 0 # <- ROTACAO DO LABEL DO EIXO X (ajuste aqui: positivo ou negativo em graus)
        },

        title={  # Título do gráfico
            "text": 'Investimento x Retorno',
            "x": 0.5,
            "y": 0.97,
            "xanchor": 'center',
            "yanchor": 'top',
            "font": {  # Cor e estilo do título
                "color": "#adb5bd",
                "size": 16,
                "family": "Segoe UI"
            }
        },
        xaxis_title='',  # Remove o título do eixo X
        yaxis_title='',  # Remove o título do eixo Y

        showlegend=True,  # Exibe a legenda
        legend={  # Estilo da legenda
            "orientation": "h",
            "yanchor": "bottom",
            "y": 0.93,
            "xanchor": "center",
            "x": 0.5,
            "font": {
                "color": "#adb5bd",  # Cor da legenda
                "size": 12,
                "family": "Segoe UI"
            }
        }
    )

    # Texto com quebras de linha manuais para o hover
    hover_msg = (
        'Clicando em "Remunerações" na legenda abaixo, é possível incluí-la na análise de retorno. <br>'
        'No entanto, ao vender parte ou a totalidade de um ativo, a análise das remunerações neste <br>'
        'gráfico pode se tornar imprecisa. Isso ocorre porque os valores de “Custo Médio” e        <br>'
        '“Patrimônio Atual” são reduzidos conforme as vendas, enquanto as “Remunerações” continuam <br>'
        'acumuladas. Assim, o rendimento visual pode parecer maior do que foi de fato.'
    )

    # Inserir uma anotação no gráfico
    fig.add_annotation(
        text="⚠️",  # Texto que será exibido (ícone de ajuda)
        xref="paper",
        yref="paper",
        x=0.59,
        y=1.09,
        showarrow=False,
        font={"size": 14, "color": "#f6fff8"},  # Cor do ícone/emoji
        align="center",
        hovertext=hover_msg,
        hoverlabel={  # Estilo do tooltip (ajuda)
            "bgcolor": "#333",  # Cor de fundo do tooltip
            "bordercolor": "#555",  # Cor da borda
            "font": {
                "family": "Segoe UI",
                "size": 13,
                "color": "#ffffff"
            }
        }
    )

    return fig


# ------------------------------------------------------------------------------------------------------------ GRÁFICO 2

def criar_grafico_cm_pa_rem_total(
    custo_medio_total_df_pos_atual,
    patrimonio_atual_total_df_pos_atual,
    remuneracoes_total_df_pos_atual,
    variacao_percentual_total_df_pos_atual
):
    fig = go.Figure()

    # Adicionar a barra de 'Custo Médio' (barra individual)
    fig.add_trace(go.Bar(
        x=['TOTAL'],
        y=[custo_medio_total_df_pos_atual],
        name='CM',
        offsetgroup=1,
        marker={"color": "#ef476f"},
        showlegend=False
    ))

    # Adicionar a barra de 'Patrimônio Atual'
    fig.add_trace(go.Bar(
        x=['TOTAL'],
        y=[patrimonio_atual_total_df_pos_atual],
        name='PA',
        offsetgroup=2,
        marker={"color": "#26547c"},
        showlegend=False,
        text=[f'{variacao_percentual_total_df_pos_atual:.0f}%'],
        textposition='inside',
        insidetextanchor='end',
        textangle=0,
        textfont={
            "family": "Segoe UI",
            "size": 9,
            "color": "#ffb3c1" if variacao_percentual_total_df_pos_atual < 0 else "#b7e4c7"
        }
    ))

    # Adicionar a barra de 'Remunerações'
    fig.add_trace(go.Bar(
        x=['TOTAL'],
        y=[remuneracoes_total_df_pos_atual],
        name='Rem',
        base=[patrimonio_atual_total_df_pos_atual],
        offsetgroup=2,
        marker={"color": "#ffd166"},
        visible='legendonly'
    ))

    # Layout igual ao gráfico por ativo
    fig.update_layout(
        barmode='group',
        plot_bgcolor='#0a0908',
        paper_bgcolor='#0a0908',
        margin={"l": 40, "r": 40, "t": 40, "b": 40},
        yaxis={
            "showgrid": True,
            "gridcolor": '#161a1d',
            "gridwidth": 1,
            "zeroline": False,
            "tickfont": {
                "color": "#adb5bd"
            }
        },
        xaxis={
            "tickfont": {
                "color": "#adb5bd",
                "size": 11
            },
            "tickangle": 0
        },
        title={
            "text": '',
            "x": 0.5,
            "y": 0.97,
            "xanchor": 'center',
            "yanchor": 'top',
            "font": {
                "color": "#adb5bd",
                "size": 14,
                "family": "Segoe UI"
            }
        },
        xaxis_title='',
        yaxis_title='',
        legend={
            "orientation": "h",
            "yanchor": "top",
            "y": -0.1,
            "xanchor": "center",
            "x": 0.5,
            "font": {
                "color": "#adb5bd",
                "size": 12,
                "family": "Segoe UI"
            }
        }
    )

    return fig


# ------------------------------------------------------------------------------------------------------------ GRÁFICO 3

def criar_grafico_distrib_cm(df_pos_atual):
    # Ordenar valores decrescentes para consistência visual
    df = df_pos_atual.copy()
    df = df.sort_values(by='Custo Médio', ascending=False)

    # Criar gráfico Sunburst com hierarquia: Tipo > Ativo
    fig = px.sunburst(
        df,
        path=['Tipo', 'Ativo'],  # Hierarquia: primeiro o Tipo, depois o Ativo
        values='Custo Médio',
        color='Tipo',  # Cores por Tipo (você pode personalizar mais abaixo)
        color_discrete_sequence=["#e63946", "#ec9a9a", "#f1faee"]  # Mesmo esquema da pizza cores=gr1 ["#23362b", "#1bb28c", "#e86a58"]
    )

    # Atualizar o layout do gráfico
    fig.update_layout(
        plot_bgcolor='#0a0908',     # Fundo da área do gráfico
        paper_bgcolor='#0a0908',    # Fundo geral
        margin={"l": 40, "r": 40, "t": 5, "b": 5},  # Margens internas

        title={
            'text': 'Distribuição da Carteira pelo Custo Médio',
            'x': 0.5,
            'y': 0.95,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'family': 'Segoe UI',
                'size': 16,
                'color': '#adb5bd'
            }
        },

        font={
            'family': 'Segoe UI',
            'color': '#adb5bd',
            'size': 12
        }
    )

    # Exibir valores em formato brasileiro no hover
    fig.update_traces(
        textinfo='label+percent entry',  # 'entry' mostra o rótulo do nó, mesmo nos níveis superiores
        hovertemplate='<b>%{label}</b><br>Custo Médio: R$ %{value:,.0f}<br>Porcentagem: %{percentRoot:.1%}',
        maxdepth=2,  # Limita o número de níveis visíveis (0 = raiz, 1 = 1º nível, 2 = até o 2º nível)
        insidetextorientation="radial",  # Orientação do texto dentro das fatias (melhor visual em círculos)
        domain={
        "x": [0.1, 0.9],  # Ocupa de 10% a 90% da largura disponível (horizontal)
        "y": [0.05, 0.875]  # Ocupa de 10% a 90% da altura disponível (vertical)
    }
    )

    return fig


# ------------------------------------------------------------------------------------------------------------ GRÁFICO 4

def criar_grafico_distrib_pa(df_pos_atual):
    # Ordenar valores decrescentes para consistência visual
    df = df_pos_atual.copy()
    df = df.sort_values(by='Patrimônio Atual', ascending=False)

    # Criar gráfico Sunburst com hierarquia: Tipo > Ativo
    fig = px.sunburst(
        df,
        path=['Tipo', 'Ativo'],  # Hierarquia: primeiro o Tipo, depois o Ativo
        values='Patrimônio Atual',
        color='Tipo',  # Cores por Tipo (você pode personalizar mais abaixo)
        color_discrete_sequence=["#457b9d", "#a8dadc", "#1d3557"]  # Mesmo esquema da pizza
    )

    # Atualizar o layout do gráfico
    fig.update_layout(
        plot_bgcolor='#0a0908',     # Fundo da área do gráfico
        paper_bgcolor='#0a0908',    # Fundo geral
        margin={"l": 40, "r": 40, "t": 5, "b": 5},  # Margens internas

        title={
            'text': 'Distribuição da Carteira pelo Patrimônio Atual',
            'x': 0.5,
            'y': 0.95,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'family': 'Segoe UI',
                'size': 16,
                'color': '#adb5bd'
            }
        },

        font={
            'family':'Segoe UI',
            'color':'#adb5bd',
            'size':12
    }
    )

    # Exibir valores em formato brasileiro no hover
    fig.update_traces(
        textinfo='label+percent entry',  # 'entry' mostra o rótulo do nó, mesmo nos níveis superiores
        hovertemplate='<b>%{label}</b><br>Patrimônio Atual: R$ %{value:,.0f}<br>Porcentagem: %{percentRoot:.1%}',
        maxdepth=2,  # Limita o número de níveis visíveis (0 = raiz, 1 = 1º nível, 2 = até o 2º nível)
        insidetextorientation="radial",  # Orientação do texto dentro das fatias (melhor visual em círculos)
        domain={
        "x": [0.1, 0.9],  # Ocupa de 10% a 90% da largura disponível (horizontal)
        "y": [0.05, 0.875]  # Ocupa de 10% a 90% da altura disponível (vertical)
    }
    )

    return fig

# ------------------------------------------------------------------------------------------------------------ GRÁFICO 5

def criar_grafico_rank_variacao(df_pos_atual):
    # Ordenar os ativos por Variação %
    df_pos_atual = df_pos_atual.sort_values(by='Variação %', ascending=True)

    # Criar gráfico de barras horizontal com cores por valor
    fig = go.Figure(go.Bar(
        x=df_pos_atual['Variação %']/100,  # Valores no eixo X
        y=df_pos_atual['Ativo'],       # Ativos no eixo Y
        orientation='h',               # Barras horizontais
        # text=df_pos_atual['Variação %'].apply(lambda x: f'{x:.2f}%'),  # Texto formatado em %
        textposition='outside',        # Texto fora da barra
        marker={  # Estilo das barras
            'color': df_pos_atual['Variação %'],  # Cor com base no valor
            'colorscale': 'Burg',  # Escala de cores divergente PuBu
            'line': {'width': 0}  # Remove contorno
        }
    ))

    # Layout no estilo escuro com tipografia clara
    fig.update_layout(
        plot_bgcolor='#0a0908',  # Cor de fundo do gráfico
        paper_bgcolor='#0a0908',  # Cor de fundo do papel
        font={
            'family': 'Segoe UI',  # Fonte consistente
            'size': 12,
            'color': '#adb5bd'  # Cor do texto clara
        },
        margin={'l': 60, 'r': 40, 't': 60, 'b': 40},  # Margens internas

        title={  # Título centralizado com estilo
            'text': 'Ranking de Ativos pela Variação de Preço',
            'x': 0.5,
            'y': 0.95,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'family': 'Segoe UI',
                'size': 16,
                'color': '#adb5bd'
            }
        },

        xaxis_title='',  # Eixos sem título
        yaxis_title='',
        showlegend=False,  # Sem legenda

        yaxis={  # Estilo do eixo Y (Ativos)
            'showgrid': True,
            'gridcolor': 'rgba(200, 200, 200, 0.075)',  # Linhas discretas
            'gridwidth': 0.5,
            "tickfont": {  # Cor dos rótulos no eixo X
                "color": "#adb5bd",
                "size": 10,
            },
        },

        xaxis={  # Estilo do eixo X (valores %)
            'zeroline': True,
            'zerolinecolor': 'rgba(255, 255, 255, 0.15)',  # Linha no zero
            'showgrid': False,
            'tickformat': '.0%',
            "tickfont": {  # Cor dos rótulos no eixo X
                "color": "#adb5bd",
                "size": 10,
            },
        }
    )

    return fig

# ------------------------------------------------------------------------------------------------------------ GRÁFICO 6

def criar_grafico_rank_tir(df_pos_atual):
    # Ordenar os ativos por Variação %
    df_pos_atual = df_pos_atual.sort_values(by='TIR %', ascending=True)

    # Criar gráfico de barras horizontal com cores por valor
    fig = go.Figure(go.Bar(
        x=df_pos_atual['TIR %']/100,  # Valores no eixo X
        y=df_pos_atual['Ativo'],       # Ativos no eixo Y
        orientation='h',               # Barras horizontais
        # text=df_pos_atual['TIR %'].apply(lambda x: f'{x:.2f}%'),  # Texto formatado em %
        textposition='outside',        # Texto fora da barra
        marker={  # Estilo das barras
            'color': df_pos_atual['TIR %'],  # Cor com base no valor
            'colorscale': 'deep',  # Escala de cores divergente PuRd
            'line': {'width': 0}  # Remove contorno
        }
    ))

    # Layout no estilo escuro com tipografia clara
    fig.update_layout(
        plot_bgcolor='#0a0908',  # Cor de fundo do gráfico
        paper_bgcolor='#0a0908',  # Cor de fundo do papel
        font={
            'family': 'Segoe UI',  # Fonte consistente
            'size': 12,
            'color': '#adb5bd'  # Cor do texto clara
        },
        margin={'l': 60, 'r': 40, 't': 60, 'b': 40},  # Margens internas

        title={  # Título centralizado com estilo
            'text': 'Ranking de Ativos pela Taxa Interna de Retorno',
            'x': 0.5,
            'y': 0.95,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'family': 'Segoe UI',
                'size': 16,
                'color': '#adb5bd'
            }
        },

        xaxis_title='',  # Eixos sem título
        yaxis_title='',
        showlegend=False,  # Sem legenda

        yaxis={  # Estilo do eixo Y (Ativos)
            'showgrid': True,
            'gridcolor': 'rgba(200, 200, 200, 0.075)',  # Linhas discretas
            'gridwidth': 0.5,
            "tickfont": {  # Cor dos rótulos no eixo X
                "color": "#adb5bd",
                "size": 10,
            },
        },

        xaxis={  # Estilo do eixo X (valores %)
            'zeroline': True,
            'zerolinecolor': 'rgba(255, 255, 255, 0.15)',  # Linha no zero
            'showgrid': False,
            'tickformat': '.0%',
            "tickfont": {  # Cor dos rótulos no eixo X
                "color": "#adb5bd",
                "size": 10,
            },
        }
    )

    return fig