# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 14:41:00 2019

@author: msardar2
"""
import pandas as pd
from brightway2 import methods, Method
import os
import swolfpy_inputdata.Data.LCIA_Methods as m


def import_methods(path_to_methods=None):
    """
    Imports the user defined LCIA methods from the csv files in the path.
    """
    if not path_to_methods:
        path_to_methods = m.__path__[0]
    files = os.listdir(path_to_methods)
    for f in files:
        if '.csv' in f:
            df = pd.read_csv(path_to_methods + '/' + f)
            CF = []
            for i in df.index:
                CF.append((eval(df['key'][i]), df['value'][i]))
            name = eval(f[:-4])
            Method(name).register(**{'unit': df['unit'][0],
                                     'num_cfs': len(df),
                                     'filename': f,
                                     'path_source_file': path_to_methods})
            Method(name).write(CF)
    methods.flush()
