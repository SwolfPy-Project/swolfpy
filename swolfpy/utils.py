# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 16:07:33 2020

@author: msmsa
"""
import json
import plotly.graph_objects as go
from plotly.offline import plot


def plot_sankey(data_json, fileName=None):
    with open(data_json) as json_file:
        data = json.load(json_file)

    layout = go.Layout(title_text=data['title_text'],
                       font_size=data['font_size'],
                       hoverlabel=data['hoverlabel'])
    data_ = go.Sankey(valueformat=data['valueformat'],
                      valuesuffix=data['valuesuffix'],
                      node=data['node'],
                      link=data['link'])
    fig = go.Figure(data=[data_], layout=layout)
    plot(fig, filename=fileName if fileName else 'plot.html', auto_open=True)
