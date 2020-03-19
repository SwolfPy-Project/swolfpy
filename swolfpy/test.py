# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 18:21:28 2020

@author: msmsa
"""

from pathlib import Path
import pandas as pd
class moj:
    def __init__(self):
        self.a = 1
    def test(self):
        print(str(Path(__file__).parent))
        x=str(Path(__file__).parent)+'/Data/SWOLF_AccountMode_LCI DATA.csv'
        self.Data = pd.read_csv(x)