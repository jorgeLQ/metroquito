import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np
import io
import base64


c1 = pd.read_excel('static/archivos/candidatura_Guarderas.xlsx')
c1b= "{:,}".format(c1.shape[0])

#style
TEXT_STYLEP={
'text-align': 'left',
'height': '45px',
'padding-left': '10px',
'font-size': '25px'
}
TEXT_STYLEP2={
'text-align': 'left',
'height': '45px',
'padding-left': '10px',
'font-size': '25px',
'font-weight': 'bold'
}
BR_STYLE={
'background-color': 'red',
'height': '2px'
}
DIV_IZ={
'float':'left'
}
DIV_DR={
'text-align': 'right',
'background-color': 'white',
'border-bottom': '2px solid #C00'
}
IMG_LOGO={
'width': '72px',
'padding-top': '5px',
'padding-right': '10px'
}
NAME_ALCALDE={
'font-weight': 'bold',
'font-size': '19px'
}
BG_CONTENT={
'background-color': '#d2d2d2'
}
#distribución por sentimiento
value_counts2 = c1['Sentimental_Analysis'].value_counts()


value_counts = c1['Sentimental_Analysis'].value_counts()
num_P = value_counts['P']
num_N = value_counts['N']

num_Pc1= "{:,}".format(num_P)
num_Nc1= "{:,}".format(num_N)

num_P_percent = round(num_P / (num_P + num_N) * 100, 1)
num_N_percent = round(num_N / (num_P + num_N) * 100, 1)
num_P_percent_str = "{}%".format(num_P_percent)
num_N_percent_str = "{}%".format(num_N_percent)

def create_pie():
    data = [go.Pie(labels=['Positivo', 'Negativo'],
                    values=[num_P_percent, num_N_percent],
                    hole=.3,
                    marker=dict(colors=['#2bc58b', '#f44d4d']))]
    layout = go.Layout(title='Polaridad Sentimientos')
    fig = go.Figure(data=data, layout=layout)
    return fig


def create_hbar():
    tendencia = c1[['Id','hashtags']]
    tendencia = tendencia.dropna()
    tendencia['hashtags'] = tendencia['hashtags'].str.split(',', expand=True)[0]
    tendencia_count = tendencia['hashtags'].value_counts().head(5)
    tendencia_count.to_frame()
    tabla = pd.DataFrame(tendencia_count.to_frame())
    tabla = tabla.rename(columns ={'hashtags':'Count'})
    tendencia_count = tabla.sort_values(by='Count', ascending=True)
    tendencia_count = tendencia_count.reset_index()
    tendencia_count = tendencia_count.rename(columns ={'index':'hashtags'})
    fig = go.Figure(data=[
        go.Bar(
            name='Tendencia',
            y=tendencia_count['hashtags'],
            x=tendencia_count['Count'],
            orientation='h',
            text=tendencia_count['Count'],
            textposition='inside',
        )
    ])

    fig.update_layout(title='Top de Tendencias', title_x=0.5,font=dict(size=18))
    return fig





def create_bar_polarity():
    df_pivot = c1.pivot_table(index=[c1['Date'].dt.year, 'Id'], columns='Sentimental_Analysis', aggfunc='size', fill_value=0)
    df_grouped = df_pivot.groupby(level=0).sum()

    trace1 = go.Bar(x=df_grouped.index, y=df_grouped['P'], name='P', marker=dict(color='#2bc58b'),text=df_grouped['P'].astype(str))
    trace2 = go.Bar(x=df_grouped.index, y=df_grouped['N'], name='N', marker=dict(color='#f44d4d'),text=df_grouped['N'].astype(str))
    data = [trace1, trace2]
    layout = go.Layout(title='Análisis de Sentimiento por Año', title_x=0.5, font=dict(size=18),barmode='stack', xaxis=dict(title='Año'), yaxis=dict(title='Cantidad'))
    fig = go.Figure(data=data, layout=layout)
    return fig



def create_topics():
    df = c1
    df_grouped = df.groupby(['topic_name','Sentimental_Analysis']).size().reset_index(name='counts')
    df_grouped
    df_grouped = df.groupby(['topic_name','Sentimental_Analysis']).size().reset_index(name='counts')
    def add_percentage(val):
        return f"{val:.2f}%"
    df_grouped = df_grouped.pivot(index='topic_name', columns='Sentimental_Analysis', values='counts')
    df_grouped['Total'] = df_grouped.sum(axis=1)
    df_grouped['P_percent'] = round(df_grouped['P'] / df_grouped['Total'] * 100, 2)
    df_grouped['N_percent'] = round(df_grouped['N'] / df_grouped['Total'] * 100, 2)


    fig = go.Figure(data=[
        go.Bar(
            name='Positivo',
            y=df_grouped.index.tolist(),
            x=df_grouped['P_percent'],
            orientation='h',
            text=df_grouped['P_percent'].astype(str) + '%',
            textposition='outside',
            marker=dict(color='#2bc58b')
        ),
        go.Bar(
            name='Negativo',
            y=df_grouped.index.tolist(),
            x=df_grouped['N_percent'],
            orientation='h',
            text=df_grouped['N_percent'].astype(str) + '%',
            textposition='outside',
            marker=dict(color='#f44d4d')
        )
    ])

    fig.update_layout(
        title='Análisis de Sentimiento por tópico', title_x=0.5,font=dict(size=18), height=600,
        yaxis=dict(
            tickmode="array",
            tickvals=df_grouped.index.tolist(),
            ticktext=df_grouped.index.tolist(),
            side='left'
        )
    )

    return fig


def create_dash_application4(flask_app):
    dash_app = dash.Dash(server=flask_app, name="Dashboard", url_base_pathname="/santiagoguarderas/",external_stylesheets=[dbc.themes.BOOTSTRAP])

    dash_app.layout = html.Div(
        children=[
                html.Div([
                    html.Span('Análisis de Opiniones Basado en Tweets', style=TEXT_STYLEP),
                    html.Br(),
                    html.Span('Metro de Quito', style=TEXT_STYLEP2),
                ],style=DIV_IZ),
                html.Div([
                    html.Img(src=('../static/images/metro_logo.png'), style=IMG_LOGO),
                    html.Br(),
                    html.Span('FECHA DE CORTE: 15/01/2023'),
                ],style=DIV_DR),

                html.Br(),

                html.Div([

                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.Div([
                                            html.Img(src=('../static/images/Guarderas.png'),style={'width': '90px'}),

                                        ],className='col-xl-6 col-md-6 mb-6'),
                                        html.Div([
                                            html.Span(" Santiago Guarderas ",style=NAME_ALCALDE),
                                            html.Span("30/09/2021 - 15/01/2023"),

                                        ],className='col-xl-6 col-md-6 mb-6'),
                                    ],className='row no-gutters align-items-center text-center'),
                                ],className='card-body'),
                            ],className='card shadow h-100 py-2'),
                        ],className='col-xl-3 col-md-6 mb-3'),

                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.Div([
                                            html.Img(src=('../static/images/twitter.png')),
                                        ],className='col-xl-6 col-md-6 mb-6'),
                                        html.Div([
                                            html.Span(" Total Tweets ",style=NAME_ALCALDE),
                                            html.Span(c1b, style={'font-size': '30px'}),
                                        ],className='col-xl-6 col-md-6 mb-6'),

                                    ],className='row no-gutters text-center'),

                                ],className='card-body'),
                            ],className='card shadow h-100 py-2'),
                        ],className='col-xl-3 col-md-6 mb-3'),

                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.Div([
                                            html.Img(src=('../static/images/smile.png')),
                                        ],className='col-xl-6 col-md-6 mb-6'),
                                        html.Div([
                                            html.Span(" Total Positivos ",style=NAME_ALCALDE),

                                            html.Span(num_Pc1, style={'font-size': '30px'}),
                                            dbc.Progress(num_P_percent_str, value=num_P_percent, color="#2bc58b", style={'height': '35px','font-size': '20px'}),
                                        ],className='col-xl-6 col-md-6 mb-6'),
                                    ],className='row no-gutters text-center'),

                                ],className='card-body'),
                            ],className='card shadow h-100 py-2'),
                        ],className='col-xl-3 col-md-6 mb-3'),

                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.Div([
                                            html.Img(src=('../static/images/sad-face.png')),
                                        ],className='col-xl-6 col-md-6 mb-6'),
                                        html.Div([
                                            html.Span(" Total Negativos ",style=NAME_ALCALDE),
                                            html.Span(num_Nc1, style={'font-size': '30px'}),
                                            dbc.Progress(num_N_percent_str, value=num_N_percent, color="#f44d4d", style={'height': '35px','font-size': '20px'}),
                                        ],className='col-xl-6 col-md-6 mb-6'),
                                    ],className='row no-gutters text-center'),
                                ],className='card-body'),
                            ],className='card shadow h-100 py-2'),
                        ],className='col-xl-3 col-md-6 mb-3'),

                    ],className='row'),


                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Div([
                                        dcc.Graph(figure=create_topics(),style={'width': '100%'}),
                                    ],className='row no-gutters align-items-center text-center'),
                                ]),
                            ],className='card border-left-success shadow h-100 py-2'),
                        ],className='col-xl-12 col-md-12 mb-12'),

                    ],className='row'),
                    html.Br(),

                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Div([
                                        dcc.Graph(figure=create_hbar(),style={'width': '100%'}),

                                    ],className='row no-gutters text-center'),
                                ]),
                            ],className='card shadow py-2'),
                        ],className='col-xl-4 col-md-6 mb-4'),

                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Div([

                                        dcc.Graph(figure=create_bar_polarity(),style={'width': '100%'}),

                                    ],className='row no-gutters text-center'),
                                ]),
                            ],className='card  shadow py-2'),
                        ],className='col-xl-5 col-md-6 mb-5'),

                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.P('Nube de palabras',style={'font-size':'25px','color': '#304463','padding-left': '26%'}),
                                        html.Img(src=('../static/images/word_cloud_c4.png'),style={'width': '100%','height': '365px'}),
                                    ],className='row no-gutters text-center'),
                                ],className='card-body'),
                            ],className='card shadow py-2'),
                        ],className='col-xl-3 col-md-6 mb-3'),

                    ],className='row'),


                ],className='container-fluid'),

                html.Br(),html.Br(),html.Br(),



        ],style=BG_CONTENT)


    return dash_app
