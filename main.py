from flask import Flask, request, make_response, redirect, render_template
from dash_application.candidatura_barrera import *
import pandas as pd
import plotly.graph_objects as go

c1 = pd.read_excel(r'C:\Users\Jorge\Documents\tesis\static\archivos\candidatura_Barrera.xlsx')
app =Flask(__name__)
create_dash_application(app)

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

    context={
        'c1b':c1b,
        'num_P_percent_str':num_P_percent_str,
        'num_N_percent_str':num_N_percent_str
    }

    return render_template('home.html', **context)
