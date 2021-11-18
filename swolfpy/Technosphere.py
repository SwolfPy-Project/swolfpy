# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 11:18:40 2020

@author: msmsa
"""
from brightway2 import Database, projects, bw2setup, databases
import bw2io
import pandas as pd
from .Required_keys import biosphere_keys
from .swolfpy_method import import_methods
from swolfpy_inputdata import Technosphere_Input
import warnings


class Technosphere:
    """
    :param project_name: Name for the project
    :type project_name: str
    :param LCI_path: Patht to the technosphere LIC csv file
    :type LCI_path: str
    :param LCI_Reference_path: Path to the csv file for the technosphere refrences
    :type LCI_Reference_path: str
    :param Ecospold2_Path: Path to the user defined technosphere LCI with ecospold2 format.
    :type Ecospold2_Path: str
    """
    def __init__(self, project_name, LCI_path=None, LCI_Reference_path=None, Ecospold2_Path=None):
        self.project_name = project_name
        self.technosphere_db_name = 'Technosphere'
        self.user_tech_name = 'User_Technosphere'

        self.InputData = Technosphere_Input(LCI_path, LCI_Reference_path, Ecospold2_Path)
        self.LCI_swolfpy_data = self.InputData.LCI_swolfpy_data
        self.LCI_reference = self.InputData.LCI_reference
        self.Ecospold2_Path = self.InputData.Ecospold2_Path

    def Create_Technosphere(self):
        """
        .. _Create_Technosphere:

        Initialize a `project` in Brightway2 by calling the ``bw2setup()`` function which creates the `biosphere3`
        database and imports the impact assesment methods. \n
        It also addes 7 new biosphere flows for cost calculations swoflpy. \n
        New impact methods are imported by calling the  ``import_methods()`` from swolfpy_method_ module. \n

        Note: If the `project` already exists, it will delete all the databases except 'biosphere3'. `Technosphere` database is written from the
        `SWOLF_AccountMode_LCI DATA.csv` in the `Data` folder unless user select new file with it's `path`.
        """
        projects.set_current(self.project_name)
        bw2setup()
        db = Database('biosphere3')
        if len(db.search('capital cost')) == 0:
            db.new_activity(code='Capital_Cost', name="Capital Cost", unit='USD', categories=('economic', ),
                            type='economic', location='US').save()
            db.new_activity(code='Operational_Cost', name="Operational Cost", unit='USD', categories=('economic', ),
                            type='economic', location='US').save()
            db.new_activity(code='Utility_Cost', name="Utility Cost", unit='USD', categories=('economic', ),
                            type='economic', location='US').save()
            db.new_activity(code='Fuel_Cost', name="Fuel Cost", unit='USD', categories=('economic', ),
                            type='economic', location='US').save()
            db.new_activity(code='Electricity_Cost', name="Electricity Cost", unit='USD', categories=('economic', ),
                            type='economic', location='US').save()
            db.new_activity(code='Transportation_Cost', name="Transportation Cost", unit='USD', categories=('economic', ),
                            type='economic', location='US').save()
            db.new_activity(code='Material_Cost', name="Material Cost", unit='USD', categories=('economic',),
                            type='economic', location='US').save()

        # adding swolf methods
        import_methods()

        # Deleting the old (expired) databases (if exist)
        xx = [x for x in databases]
        for x in xx:
            if x not in ['biosphere3']:
                del databases[x]
        if self.LCI_reference['Reference_activity_id'].count() > 0:
            self._Write_user_technospher()
            db = Database(self.user_tech_name)
            self.user_tech_keys = {}
            for x in db:
                self.user_tech_keys[x.as_dict()['activity']] = x.key
        self._write_technosphere()

    def _Write_user_technospher(self):
        """
        Creates the user technosphere database from Ecospold2 files. \n
        Interface with Brightway2: Calls the ``bw2io.importers.SingleOutputEcospold2Importer`` function.
        """
        self.user_tech = bw2io.importers.SingleOutputEcospold2Importer(dirpath=self.Ecospold2_Path, db_name=self.user_tech_name)
        self.user_tech.apply_strategies()
        stats = self.user_tech.statistics()
        if stats[2] > 0:
            warnings.warn('There is {} unlink flows in the user defined technosphere (ecospold files). Make sure you are using the LCI ecosplod'
                          .format(stats[2]))
            print('\nUnique unlinked exchanges:\n')
            for x in self.user_tech.unlinked:
                print(x['type'], x['name'], x['amount'])

            print('\nAdd unlinked flows to biosphere database:\n')
            self.user_tech.add_unlinked_flows_to_biosphere_database()

        print("""
                ####
                ++++++  Writing the {}
                """.format(self.user_tech_name))
        self.user_tech.write_database()

    def _write_technosphere(self):
        """
        Creates the swolfpy technosphere database.\n
        """
        self.technosphere_data = {}
        # activities
        names = [x for x in self.LCI_swolfpy_data.columns][3:]
        for x in names:
            # add activity to database
            self.technosphere_data[(self.technosphere_db_name, x)] = {
                'name': x,
                'reference product': x,
                'unit': (lambda y: 'NA' if pd.isnull(y) else y)(self.LCI_swolfpy_data[x][0]),
                'exchanges': []}
            # Reference flow
            ex = {}
            ex['amount'] = 1
            ex['input'] = (self.technosphere_db_name, x)
            ex['type'] = 'production'
            ex['unit'] = self.technosphere_data[(self.technosphere_db_name, x)]['unit']
            self.technosphere_data[(self.technosphere_db_name, x)]['exchanges'].append(ex)

            if pd.isnull(self.LCI_reference['Reference_activity_id'][x]):
                i = 0
                for val in self.LCI_swolfpy_data[x][2:]:
                    if float(self._check_nan(val)) != 0:
                        ex = {}  # add exchange to activities
                        ex['amount'] = float(self._check_nan(val))
                        ex['input'] = biosphere_keys[i][0]
                        ex['type'] = 'biosphere'
                        ex['unit'] = 'kg'
                        self.technosphere_data[(self.technosphere_db_name, x)]['exchanges'].append(ex)
                    i += 1
            else:
                ex = {}  # add exchange to activities
                ex['amount'] = 1
                ex['input'] = self.user_tech_keys[self.LCI_reference['Reference_activity_id'][x]]
                ex['type'] = 'technosphere'
                ex['unit'] = self.LCI_reference['Unit'][x]
                self.technosphere_data[(self.technosphere_db_name, x)]['exchanges'].append(ex)

            if not pd.isnull(self.LCI_reference['Cost_key'][x]):  # adding the cost to technosphere
                ex = {}  # add exchange to activities
                ex['amount'] = self._check_nan(self.LCI_reference['Cost'][x])
                ex['input'] = ('biosphere3', self.LCI_reference['Cost_key'][x])
                ex['type'] = 'biosphere'
                ex['unit'] = self.LCI_reference['Cost_Unit'][x]
                self.technosphere_data[(self.technosphere_db_name, x)]['exchanges'].append(ex)

        print("""
                ####
                ++++++  Writing the {}
                """.format(self.technosphere_db_name))
        self.technosphere_db = Database(self.technosphere_db_name)
        self.technosphere_db.write(self.technosphere_data)
        # replace zeros when there is no data ("nan")

    def _check_nan(self, x):
        """
        Check the `x` and return 0 if `x` is `nan`.

        """
        if str(x) == "nan":
            return 0
        return x
