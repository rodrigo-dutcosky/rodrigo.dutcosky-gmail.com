

def definir_cores(amostras, marca_mdias):

    colors = ['rgb(245, 200, 70)', 'rgb(150, 45, 35)', 'rgb(179, 150, 84)']

    N = 0
    color_dict = {}
    for A in amostras:
        if A in marca_mdias.keys():
            color_dict[A] = 'rgb(10, 35, 100)'
        else:
            color_dict[A] = colors[N]
            N += 1

    return color_dict


def exec_pizza_atributos_usuario(df, height, width):

    colors = [
        'rgb(103,0,31)', 
        'rgb(178,24,43)', 
        'rgb(214,96,77)', 
        'rgb(244,165,130)', 
        'rgb(253,219,199)',
        'rgb(245,210,195)'
    ]
    
    attb = list(df.columns)[0]

    if attb == 'SEXO':
        text_template = "| <b>%{percent:%,s}</b> <br> %{label}"

    elif attb == 'FAIXA_ETARIA':
        text_template = "| <b>%{percent:%,s}</b> <br> %{label}"

    elif attb == 'CLASSE_SOCIAL':
        text_template = "<b>%{percent:%,s}</b> | %{label}"

    elif attb == 'ESCOLARIDADE':
        text_template = "| <b>%{percent:%,s}</b> <br> %{label}"
        
    else:
        pass
        

    plot = go.Figure()

    plot.add_trace(go.Pie(

        labels = df[attb],
        values = df['ID_USUARIO'],

        showlegend = False,
        textposition = 'outside', 
        textinfo = 'percent+label',
        texttemplate = text_template,
        textfont = dict(size = 20, family = "Gilroy", color = 'black'), 

        opacity = 0.8,
        marker_line_color = 'white', 
        marker_line_width = 2, 
        marker = dict(colors = colors)
    ))

    plot.update_layout(

        paper_bgcolor = "white", 
        plot_bgcolor = "white", 
        height = height, 
        width = width, 
        margin = dict(t = 0, r = 0, b = 0, l = 0), 
    )

    return plot


def exec_nota_escala_hedonica(df, height, width):
    
    color_dict = {

        '7 ou Mais'  : 'rgb(170, 204, 161)',
        '5 ou 6'     : 'rgb(232, 213, 137)',
        '4 ou Menos' : 'rgb(232, 143, 137)'
    }

    plot = go.Figure()

    for K in color_dict.keys():

        plot.add_trace(go.Bar(

            y = df[df.NOTA == K].AMOSTRA,
            x = df[df.NOTA == K].FREQ_PERC,
            name = K,

#             text = df[df.NOTA == K].FREQ_PERC.apply(lambda x: round(x * 100, 0)),
#             textfont = dict(size = 22, family = "Gilroy", color = 'black'), 
#             textposition = 'auto', 

            marker_color = color_dict[K],
            orientation = 'h',
            marker_line_color = 'black', 
            marker_line_width = 0.5, 
            opacity = 0.9,
            width = 0.6
        ))

    plot.update_layout(

        yaxis  = dict(

            showline = False, 
            mirror = False, 
            linewidth = 1.4, 
            linecolor = 'black',  

            showgrid = True, 
            gridcolor = 'rgb(225,225,225)', 
            zerolinecolor = 'rgb(225,225,225)',

            nticks = 5, 
            dtick = 0.05, 
            ticklen = 8, 
            ticks = "outside", 
            tickcolor = 'white',

            showticklabels = True, 
            tickfont = dict(size = 18, family = "Gilroy", color = 'black')
        ),

        xaxis  = dict(

            range = [0, 1],
            showgrid = True, 
            gridcolor = 'rgb(200,200,200)', 
            showticklabels = True, 

            showline = False,
            mirror = False, 
            linecolor = 'black',
            linewidth = 1.4, 

            tickson = "boundaries", 
            ticks = "outside", 
            ticklen = 3,  
            tickwidth = 1, 
            tickcolor = 'rgb(225,225,225)',
            tickformat = '%', 
            tickfont = dict(size = 18, family = "Gilroy", color = 'black')
        ),

        legend = dict(

            y = 1.02, 
            x = 0.75, 
            yanchor = "bottom", 
            xanchor = "right",

            bgcolor = "white", 
            bordercolor = "white",
            borderwidth = 0.5,

            orientation = "h", 
            font = dict(size = 19, color = 'black', family = "Gilroy")
        ),

        height = height, 
        width = width, 
        margin = dict(t = 0, r = 20, b = 40, l = 0), 

        paper_bgcolor = "white", 
        plot_bgcolor = "white", 
        barmode = "stack"
    )

    return plot


def exec_histograma_escala_hedonica(df, marca_mdias):

    atributo = df.columns[0]
    amostras = list(df.iloc[:, 1:].columns)
    color_dict = definir_cores(amostras, marca_mdias)

    plot = go.Figure()
    
    for A in amostras:

        plot.add_trace(go.Bar(
            x = df[atributo], 
            y = df[A], 
            name = A,
            marker_color = color_dict[A], 
            marker_line_color = 'black', 
            marker_line_width = 0.5, 
            opacity = 0.7
        ))

    plot.update_layout(

            yaxis  = dict(

                tickformat = '%', 
                nticks = 4, 
                dtick = 0.1,
                ticklen = 5,  
                tickson = "boundaries", 
                ticks = "outside",
                tickcolor = 'white',
                showticklabels = True, 
                tickfont = dict(size = 18, family = "Gilroy", color = 'black'), 

                showgrid = True, 
                gridcolor = 'rgb(215,215,215)', 

                showline = True, 
                linewidth = 1.4, 
                linecolor = 'black', 
                mirror = False, 
                zerolinecolor = 'white'
            ),

            xaxis  = dict(
                type = 'category',
                ticklen = 3,  
                tickson = "boundaries", 
                ticks = "outside", 
                tickwidth = 1,
                tickfont = dict(size = 18, family = "Gilroy", color = 'black'),

                showgrid = False, 
                gridcolor = 'rgb(225,225,225)', 

                showline = True,
                linewidth = 1.4, 
                linecolor = 'black', 
                mirror = False
            ),

            legend = dict(
                orientation = "h", 
                y = 1.02, 
                x = 0.7, 
                yanchor = "bottom", 
                xanchor = "right",
                font = dict(size = 16, color = 'black', family = "Gilroy"), 
                bgcolor = "white", bordercolor = "white", borderwidth = 0.5),

        height =  400, 
        width = 600, 
        paper_bgcolor = "white", 
        plot_bgcolor = "white", 
        margin = dict(t = 0, r = 0, b = 40, l = 0)
    )
    
    return plot


def exec_marca_preferencia(df):
    
    if len(df.columns) == 5:
        color_dict = {
            '1' : 'rgb(245, 70, 40)',   '2' : 'rgb(240, 160, 110)', 
            '3' : 'rgb(250, 230, 150)', '4' : 'rgb(260, 200, 90)'
        }
    if len(df.columns) == 4:
        color_dict = {'1' : 'rgb(245, 70, 40)', '2' : 'rgb(240, 160, 110)','3' : 'rgb(250, 230, 150)'}

    elif len(df.columns) == 3:
        color_dict = {'1' : 'rgb(245, 70, 40)', '2' : 'rgb(250, 230, 150)'}
    else:
        pass

    plot = go.Figure()

    for K in color_dict.keys():

        plot.add_trace(go.Bar(
            x = df['AMOSTRA'], 
            y = df[K], 
            name = K,
            marker_color = color_dict[K], 
            marker_line_color = 'black',
            marker_line_width = 0.6, 
            opacity = 0.75,
            width = 0.65
        ))

    plot.update_layout(

        yaxis  = dict(

            showline = True, 
            mirror = False, 
            linewidth = 1.25, 
            linecolor = 'black', 

            showgrid = True, 
            gridcolor = 'rgb(210,210,210)', 
            zerolinecolor = 'black',

            tickson = "boundaries", 
            ticks = "outside", 
            ticklen = 3,  
            tickwidth = 1, 
            tickcolor = 'rgb(225,225,225)',
            tickformat = '%', 

            showticklabels = True, 
            tickfont = dict(size = 18, family = "Gilroy", color = 'black')
        ),

        xaxis  = dict(

            showgrid = False, 
            gridcolor = 'rgb(225,225,225)', 

            showline = True,
            mirror = False, 
            linecolor = 'white', 
            linewidth = 1.5, 

            ticklen = 8, 
            ticks = "outside", 
            tickcolor = 'white',
            tickfont = dict(size = 18, family = "Gilroy", color = 'black')
        ),

        legend = dict(

            y = - .2, 
            x = 0.7, 
            yanchor = "bottom", 
            xanchor = "right",

            bgcolor = "white", 
            bordercolor = "white",
            borderwidth = 0.75,

            orientation = "h", 
            font = dict(size = 20, color = 'black', family = "Gilroy")
        ),

        height = 500, 
        width = 525, 
        margin = dict(t = 0, r = 0, b = 30, l = 0), 

        paper_bgcolor = "white", 
        plot_bgcolor = "white", 
        barmode = "stack"
    )

    return plot


def exec_medias_hedonicas_entre_marcas(df, marca_mdias):
    
    amostras = []
    for C in df.columns:
        if C.find('OL') == -1 and C != 'HEDONICA':
            amostras.append(C)

    color_dict = definir_cores(amostras, marca_mdias)
    
    plot = go.Figure()

    for A in amostras:

        plot.add_trace(go.Scatter(
            y = df.HEDONICA.apply(lambda x: x.replace('PROPORCAO_RECHEIO_CASQUINHA', 'Recheio casquinha'
                                ).replace('_', ' ').capitalize()), 
            x = df[A],
            name = A, 
            mode = 'lines+markers', 
            showlegend = True,
            line = dict(color = color_dict[A], width = 2.5), 
            marker = dict(color = color_dict[A], size = 20, line = dict(color = 'white', width = 2))
        ))

        plot.add_trace(go.Scatter(
            y = df.HEDONICA.apply(lambda x: x.replace('PROPORCAO_RECHEIO_CASQUINHA', 'Recheio casquinha'
                                ).replace('_', ' ').capitalize()), 
            x = df[A + 'OL'],
            mode = 'lines', 
            name = 'Overall Liking',
            line = dict(color = color_dict[A], width = 4, dash = 'dash')
        ))

    plot.update_layout(

        yaxis  = dict(

            showgrid = True,
            gridcolor = 'rgb(210,210,210)', 

            showline = True, 
            mirror = False, 
            linewidth = 2, 
            linecolor = 'rgb(87,87,87)', 
            zerolinecolor = 'white',

            ticks = "outside", 
            ticklen = 9,
            tickcolor = 'rgb(225,225,225)',
            tickfont = dict(size = 20, family = "Gilroy", color = 'black'),
            showticklabels = True
        ),

        xaxis  = dict(

            showgrid = True, 
            gridcolor = 'rgb(210,210,210)', 

            showline = True, 
            mirror = False, 
            linewidth = 2, 
            linecolor = 'rgb(87,87,87)',


            ticks = "outside", 
            ticklen = 9, 
            dtick = 0.25, 
            tickcolor = 'rgb(225,225,225)',
            tickfont = dict(size = 22, family = "Gilroy", color = 'black'),

            title_text = 'Media', titlefont = dict(size = 18, family = "Gilroy", color = 'black'), 
            # range = [np.array(df.iloc[: , 1:]).min() - 0.5, np.array(df.iloc[: , 1:]).max() + 0.5]
            range = [5, 8]
        ),

        legend = dict(

            y = 0.7, 
            x = 1.05, 
            yanchor = "bottom", 
            xanchor = "right",
            font = dict(size = 18, color = 'black', family = "Gilroy"), 
            bgcolor = "white", 
            bordercolor = "black", 
            borderwidth = 0.5
        ),

        height = 525, 
        width = 1300, 
        paper_bgcolor = "white", 
        plot_bgcolor = "white", 
        margin = dict(t = 5, r = 15, b = 5, l = 0) 
    )
    
    return plot

def exec_tabela_escala_jar(html):

    table = go.Figure()
    table.add_trace(go.Table(

        header = dict(

            values = ['<b>Amostra</b>','<b>Mais Fraco</b>','<b>Ideal</b>','<b>Mais Forte</b>'],
            line_color = 'white',
            fill_color = 'rgb(180, 85, 80)',

            align = ['center','center'],
            font = dict(color = 'white', size = 16)
        ),
        cells = dict(
            values = [
                list(map(lambda x: '<b>' + x + '</b>', list(html['AMOSTRA']))), 
                list(map(lambda x: '<b>' + x + '</b>', list(html['Mais Fraco']))), 
                list(map(lambda x: '<b>' + x + '</b>', list(html['Ideal']))), 
                list(map(lambda x: '<b>' + x + '</b>', list(html['Mais Forte'])))
            ],

            height = 40,
            line_color = 'white',
            fill_color = [['rgb(180, 85, 80)'] * (len(html) - 1), ['rgb(240, 190, 190)'] * (len(html) - 1)],
            align = ['center', 'center'],
            font = dict(color = 'white', size = 16)
        )
    ))

    table.update_layout(
        height = 150, 
        width = 500, 
        margin = dict(t = 0, r = 0, b = 0, l = 0)
    )
    
    return table


def exec_histograma_escala_jar(df, marca_mdias):

    atributo = df.columns[0]
    amostras = list(df.iloc[:, 1:].columns)
    color_dict = definir_cores(amostras, marca_mdias)

    plot = go.Figure()
    
    for A in amostras:

        plot.add_trace(go.Bar(
            x = df[atributo], 
            y = df[A], 
            name = A,
            marker_color = color_dict[A], 
            marker_line_color = 'black', 
            marker_line_width = 0.5, 
            opacity = 0.7
        ))

    plot.update_layout(

            yaxis  = dict(

                tickformat = '%', 
                nticks = 4, 
                dtick = 0.1,
                ticklen = 5,  
                tickson = "boundaries", 
                ticks = "outside",
                tickcolor = 'white',
                showticklabels = True, 
                tickfont = dict(size = 18, family = "Gilroy", color = 'black'), 

                showgrid = True, 
                gridcolor = 'rgb(215,215,215)', 

                showline = True, 
                linewidth = 1.4, 
                linecolor = 'black', 
                mirror = False, 
                zerolinecolor = 'white'
            ),

            xaxis  = dict(
                type = 'category',
                ticklen = 3,  
                tickson = "boundaries", 
                ticks = "outside", 
                tickwidth = 1,
                tickfont = dict(size = 18, family = "Gilroy", color = 'black'),

                showgrid = False, 
                gridcolor = 'rgb(225,225,225)', 

                showline = True,
                linewidth = 1.4, 
                linecolor = 'black', 
                mirror = False
            ),

            legend = dict(
                orientation = "h", 
                y = - 0.15, 
                x = 0.65,
                yanchor = "bottom", 
                xanchor = "right",
                font = dict(size = 16, color = 'black', family = "Gilroy"), 
                bgcolor = "white", bordercolor = "white", borderwidth = 0.5),

        height =  450, 
        width = 600, 
        paper_bgcolor = "white", 
        plot_bgcolor = "white", 
        margin = dict(t = 0, r = 0, b = 40, l = 0)
    )
    
    return plot

