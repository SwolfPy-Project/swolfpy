# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 16:36:48 2019

@author: msmsa
"""

import brightway2 as bw
bw.projects.set_current("default")
Directory = "C:\\Users\\msmsa\\Documents\\Ecoinvent database\\ecoinvent 3.4_cutoff_ecoSpold02\\datasets"
ecoinvent = bw.SingleOutputEcospold2Importer(Directory,'ecoinvent 3.4_cutoffe')
ecoinvent.apply_strategies()
ecoinvent.statistics()
ecoinvent.write_database()
