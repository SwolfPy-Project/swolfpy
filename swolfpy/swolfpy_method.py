# -*- coding: utf-8 -*-
import os

import pandas as pd
import swolfpy_inputdata.data.lcia_methods as m
from brightway2 import Method, methods


def import_methods(path_to_methods=None):
    """
    Imports the user defined LCIA methods from the csv files in the path.
    """
    if not path_to_methods:
        path_to_methods = m.__path__[0]
    files = os.listdir(path_to_methods)
    for f in files:
        if ".csv" in f:
            df = pd.read_csv(path_to_methods + "/" + f)
            CF = []
            for i in df.index:
                CF.append((eval(df["key"][i]), df["value"][i]))
            name = eval(f[:-4])
            Method(name).register(
                **{
                    "unit": df["unit"][0],
                    "num_cfs": len(df),
                    "filename": f,
                    "path_source_file": path_to_methods,
                }
            )
            Method(name).write(CF)
    methods.flush()
