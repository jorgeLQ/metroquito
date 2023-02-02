from flask import Flask, request, make_response, redirect, render_template
from dash_application.candidatura_barrera import *
from dash_application.candidatura_rodas import *
from dash_application.candidatura_yunda import *
from dash_application.candidatura_guarderas import *
import pandas as pd
import plotly.graph_objects as go

c1 = pd.read_excel('static/archivos/candidatura_Barrera.xlsx')
c2 = pd.read_excel('static/archivos/candidatura_Rodas.xlsx')
c3 = pd.read_excel('static/archivos/candidatura_Yunda.xlsx')
c4 = pd.read_excel('static/archivos/candidatura_Guarderas.xlsx')

app =Flask(__name__)
create_dash_application(app)
create_dash_application2(app)
create_dash_application3(app)
create_dash_application4(app)

@app.route('/')
def home():

    c1b= "{:,}".format(c1.shape[0])
    '''Sentimiento por candidatura'''
    value_counts = c1['Sentimental_Analysis'].value_counts()
    num_P = value_counts['P']
    num_N = value_counts['N']
    num_P_percent = round(num_P / (num_P + num_N) * 100, 1)
    num_N_percent = round(num_N / (num_P + num_N) * 100, 1)
    num_P_percent_str = "{}%".format(num_P_percent)
    num_N_percent_str = "{}%".format(num_N_percent)

    c2b= "{:,}".format(c2.shape[0])
    '''Sentimiento por candidatura'''
    value_counts2 = c2['Sentimental_Analysis'].value_counts()
    num_P2 = value_counts2['P']
    num_N2 = value_counts2['N']
    num_P_percent2 = round(num_P2 / (num_P2 + num_N2) * 100, 1)
    num_N_percent2 = round(num_N2 / (num_P2 + num_N2) * 100, 1)
    num_P_percent_str2 = "{}%".format(num_P_percent2)
    num_N_percent_str2 = "{}%".format(num_N_percent2)

    c3b= "{:,}".format(c3.shape[0])
    '''Sentimiento por candidatura'''
    value_counts3 = c3['Sentimental_Analysis'].value_counts()
    num_P3 = value_counts3['P']
    num_N3 = value_counts3['N']
    num_P_percent3 = round(num_P3 / (num_P3 + num_N3) * 100, 1)
    num_N_percent3 = round(num_N3 / (num_P3 + num_N3) * 100, 1)
    num_P_percent_str3 = "{}%".format(num_P_percent3)
    num_N_percent_str3 = "{}%".format(num_N_percent3)

    c4b= "{:,}".format(c4.shape[0])
    '''Sentimiento por candidatura'''
    value_counts4 = c4['Sentimental_Analysis'].value_counts()
    num_P4 = value_counts4['P']
    num_N4 = value_counts4['N']
    num_P_percent4 = round(num_P4 / (num_P4 + num_N4) * 100, 1)
    num_N_percent4 = round(num_N4 / (num_P4 + num_N4) * 100, 1)
    num_P_percent_str4 = "{}%".format(num_P_percent4)
    num_N_percent_str4 = "{}%".format(num_N_percent4)

    context={
        'c1b':c1b,
        'num_P_percent_str':num_P_percent_str,
        'num_N_percent_str':num_N_percent_str,

        'c2b':c2b,
        'num_P_percent_str2':num_P_percent_str2,
        'num_N_percent_str2':num_N_percent_str2,

        'c3b':c3b,
        'num_P_percent_str3':num_P_percent_str3,
        'num_N_percent_str3':num_N_percent_str3,

        'c4b':c4b,
        'num_P_percent_str4':num_P_percent_str4,
        'num_N_percent_str4':num_N_percent_str4
    }

    return render_template('home.html', **context)
