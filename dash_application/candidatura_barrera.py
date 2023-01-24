import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go



c1 = pd.read_excel(r'C:\Users\Jorge\Documents\tesis\static\archivos\candidatura_Barrera.xlsx')
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
'background-color': '#e7e7e7'
}
#distribución por sentimiento
value_counts = c1['Sentimental_Analysis'].value_counts()
num_P = value_counts['P']
num_N = value_counts['N']
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


def create_dash_application(flask_app):
    dash_app = dash.Dash(server=flask_app, name="Dashboard", url_base_pathname="/augustobarrera/",external_stylesheets=[dbc.themes.BOOTSTRAP])
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
                                        html.Img(src=('../static/images/Barrera.png')),
                                        html.P("Augusto Barrera",style=NAME_ALCALDE),
                                        html.P("31/07/2009 - 14/05/2014"),
                                    ], className='bg-white card'),

                                ],className='col-xs-12 col-sm-6 col-md-4 col-lg-4 ',style={'text-align': 'center'}),


                                html.Div([

                                    html.Div([
                                        html.Div([
                                            html.Div([
                                                html.Img(src=('../static/images/twitter.png')),
                                                html.P("Tweets Totales"),
                                                html.P(c1b),
                                            ],className='col-xs-12 col-sm-6 col-md-4 col-lg-4'),

                                            html.Div([
                                                html.Img(src=('../static/images/smile.png')),
                                                html.P("Positivos"),
                                                html.P(num_P),
                                            ],className='col-xs-12 col-sm-6 col-md-4 col-lg-4'),

                                            html.Div([
                                                html.Img(src=('../static/images/sad-face.png')),
                                                html.P("Negativos"),
                                                html.P(num_N),
                                            ],className='col-xs-12 col-sm-6 col-md-4 col-lg-4'),

                                        ],className='row d-flex'),
                                    ],className='container', style={'padding-top': '40%'}),

                                ],className='col-xs-12 col-sm-6 col-md-4 col-lg-4 card',style={'text-align': 'center'}),

                                html.Div([
                                    html.Div([
                                        dcc.Graph(figure=create_pie()),
                                    ], className='bg-white card'),
                                ],className='col-xs-12 col-sm-6 col-md-4 col-lg-4',style={'text-align': 'center'}),

                            ],className='row justify-content-between'),
                        ],className='container'),

                html.Br(),html.Br(),html.Br(),

                html.Div([

                    html.Div([
                        html.Div([
                            html.Div([
                                html.Img(src=('../static/images/Barrera.png')),
                                html.P("Augusto Barrera",style=NAME_ALCALDE),
                                html.P("31/07/2009 - 14/05/2014"),

                            ],className='card-body',style={'padding-top':'20%'})
                        ],className='col-xs-12 col-sm-6 col-md-4 col-lg-4 card',style={'text-align': 'center'}),

                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.Div([
                                            html.Img(src=('../static/images/twitter.png')),
                                            html.P("Tweets Totales"),
                                            html.P(c1b),
                                        ],className='col-xs-12 col-sm-6 col-md-4 col-lg-4'),

                                        html.Div([
                                            html.Img(src=('../static/images/smile.png')),
                                            html.P("Positivos"),
                                            html.P(num_P),
                                        ],className='col-xs-12 col-sm-6 col-md-4 col-lg-4'),

                                        html.Div([
                                            html.Img(src=('../static/images/sad-face.png')),
                                            html.P("Negativos"),
                                            html.P(num_N),
                                        ],className='col-xs-12 col-sm-6 col-md-4 col-lg-4'),

                                    ],className='row'),
                                ],className='container',style={'padding-top': '30%'}),

                            ],className='card-body')
                        ],className=' col-xs-12 col-sm-6 col-md-4 col-lg-4 card',style={'text-align': 'center'}),

                        html.Div([
                            html.Div([
                                dcc.Graph(figure=create_pie()),
                            ],className='card-body')
                        ],className='col-xs-12 col-sm-6 col-md-4 col-lg-4 card',style={'text-align': 'center'}),


                    ],className='row')
                ],className='container '),

                html.Br(),html.Br(),html.Br(),
        ],style=BG_CONTENT)


    return dash_app
