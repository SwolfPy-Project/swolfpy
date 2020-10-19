# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 14:41:00 2019

@author: msardar2
"""
import pandas as pd
from brightway2 import methods, Method, Database
from .Required_keys import biosphere_keys
from pathlib import Path


def import_methods():
    """
    doc
    """
    keys = biosphere_keys

    bd = Database("biosphere3")

    bio_flows = []
    for i in keys:
        bio_flows.append([keys[i][0], bd.get(keys[i][0][1])])

    jj = pd.DataFrame(bio_flows)

    ### jj.to_csv("SWOLF _ IPPC.csv")
    ### Add the Characterization factors to the SWOLF_IPPC.csv file from the SWOLF and read it again to have characterization factors

    Data = pd.read_csv(Path(__file__).parent / 'SWOLF_LCIA_Methods.csv')

    SWOLF_IPCC = []
    SWOLF_Acidification = []
    SWOLF_Eutrophication = []
    SWOLF_PhotochemicalSmog = []
    SWOLF_CED = []
    SWOLF_Ecotoxicity = []
    SWOLF_HumanToxicity = []

    for i in range(len(Data.key)):
        if Data.CF1[i] != 0:
            SWOLF_IPCC.append((jj[0][i], Data.CF1[i]))
        if Data.CF2[i] != 0:
            SWOLF_Acidification.append((jj[0][i], Data.CF2[i]))
        if Data.CF3[i] != 0:
            SWOLF_Eutrophication.append((jj[0][i], Data.CF3[i]))
        if Data.CF4[i] != 0:
            SWOLF_PhotochemicalSmog.append((jj[0][i], Data.CF4[i]))
        if Data.CF5[i] != 0:
            SWOLF_CED.append((jj[0][i], Data.CF5[i]))
        if Data.CF6[i] != 0:
            SWOLF_Ecotoxicity.append((jj[0][i], Data.CF6[i]))
        if Data.CF7[i] != 0:
            SWOLF_HumanToxicity.append((jj[0][i], Data.CF7[i]))

    SWOLF_Capital_Cost = [(('biosphere3', 'Capital_Cost'), 1)]

    SWOLF_Operational_Cost = [(('biosphere3', 'Operational_Cost'), 1), (('biosphere3', 'Utility Cost'), 1),
                              (('biosphere3', 'Fuel_Cost'), 1), (('biosphere3', 'Electricity_Cost'), 1),
                              (('biosphere3', 'Transportation_Cost'), 1), (('biosphere3', 'Material_Cost'), 1)]

    SWOLF_Total_Cost = [(('biosphere3', 'Capital_Cost'), 1), (('biosphere3', 'Operational_Cost'), 1),
                        (('biosphere3', 'Utility Cost'), 1), (('biosphere3', 'Fuel_Cost'), 1),
                        (('biosphere3', 'Electricity_Cost'), 1), (('biosphere3', 'Transportation_Cost'), 1),
                        (('biosphere3', 'Material_Cost'), 1)]

    Method(('SWOLF_Capital_Cost', 'SWOLF')).register(**{'unit': 'USD',
                                                        'num_cfs': 1,
                                                        'abbreviation': '',
                                                        'description': 'Capital cost',
                                                        'filename': ''})

    Method(('SWOLF_Capital_Cost', 'SWOLF')).write(SWOLF_Capital_Cost)

    Method(('SWOLF_Operational_Cost', 'SWOLF')).register(**{'unit': 'USD',
                                                            'num_cfs': 1,
                                                            'abbreviation': '',
                                                            'description': 'Operational cost',
                                                            'filename': ''})
    Method(('SWOLF_Operational_Cost', 'SWOLF')).write(SWOLF_Operational_Cost)

    Method(('SWOLF_Total_Cost', 'SWOLF')).register(**{'unit': 'USD',
                                                      'num_cfs': 2,
                                                      'abbreviation': '',
                                                      'description': 'Total cost',
                                                      'filename': ''})
    Method(('SWOLF_Total_Cost', 'SWOLF')).write(SWOLF_Total_Cost)

    Method(('SWOLF_IPCC', 'SWOLF')).register(**{'unit': 'kg CO2eq',
                                                'num_cfs': '',
                                                'abbreviation': '',
                                                'description': 'based on IPCC 2007 method',
                                                'filename': ''})
    Method(('SWOLF_IPCC', 'SWOLF')).write(SWOLF_IPCC)

    Method(('SWOLF_Acidification', 'SWOLF')).register(**{'unit': 'NAN',
                                                         'num_cfs': '',
                                                         'abbreviation': '',
                                                         'description': 'based on --- mehtod',
                                                         'filename': ''})
    Method(('SWOLF_Acidification', 'SWOLF')).write(SWOLF_Acidification)

    Method(('SWOLF_Eutrophication', 'SWOLF')).register(**{'unit': 'NAN',
                                                          'num_cfs': '',
                                                          'abbreviation': '',
                                                          'description': 'based on --- mehtod',
                                                          'filename': ''})
    Method(('SWOLF_Eutrophication', 'SWOLF')).write(SWOLF_Eutrophication)

    Method(('SWOLF_PhotochemicalSmog', 'SWOLF')).register(**{'unit': 'NAN',
                                                             'num_cfs': '',
                                                             'abbreviation': '',
                                                             'description': 'based on --- mehtod',
                                                             'filename': ''})
    Method(('SWOLF_PhotochemicalSmog', 'SWOLF')).write(SWOLF_PhotochemicalSmog)

    Method(('SWOLF_CED', 'SWOLF')).register(**{'unit': 'NAN',
                                               'num_cfs': '',
                                               'abbreviation': '',
                                               'description': 'based on --- mehtod',
                                               'filename': ''})
    Method(('SWOLF_CED', 'SWOLF')).write(SWOLF_CED)

    Method(('SWOLF_Ecotoxicity', 'SWOLF')).register(**{'unit': 'NAN',
                                                       'num_cfs': '',
                                                       'abbreviation': '',
                                                       'description': 'based on --- mehtod',
                                                       'filename': ''})
    Method(('SWOLF_Ecotoxicity', 'SWOLF')).write(SWOLF_Ecotoxicity)

    Method(('SWOLF_HumanToxicity', 'SWOLF')).register(**{'unit': 'NAN',
                                                         'num_cfs': '',
                                                         'abbreviation': '',
                                                         'description': 'based on --- mehtod',
                                                         'filename': ''})
    Method(('SWOLF_HumanToxicity', 'SWOLF')).write(SWOLF_HumanToxicity)

    methods.flush()
