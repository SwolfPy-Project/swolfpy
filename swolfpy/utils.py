# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 16:07:33 2020

@author: msmsa
"""
import json
import plotly.graph_objects as go
from plotly.offline import plot
import brightway2 as bw2
import pandas as pd


def plot_sankey(data_json, fileName=None):
    """
    Plot sankey diagram from the JSON file created by SwolfPy.
    """
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


def dump_method(methodName, path=None):
    """
    Dump the LCIA method to a `csv` file in `path` directory.
    """
    method = bw2.Method(methodName)
    data = method.load()
    key = []
    value = []
    unit = []
    name = []
    categories = []
    for i in data:
        key.append(i[0])
        value.append(i[1])
        unit.append(method.metadata['unit'])
        act = bw2.get_activity(i[0])
        name.append(act.as_dict()['name'])
        categories.append(act.as_dict()['categories'])
    DF = pd.DataFrame({'key': key,
                       'name': name,
                       'categories': categories,
                       'value': value,
                       'unit': unit})
    if path:
        DF.to_csv(path + "/" + str(methodName) + ".csv", index=False)
    else:
        DF.to_csv(str(methodName) + '.csv', index=False)
    return(DF)
