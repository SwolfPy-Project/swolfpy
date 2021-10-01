# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 21:42:51 2019

@author: msmsa
"""
import numpy as np
from brightway2 import Database


class ProcessDB():
    def __init__(self, process_name, waste_treatment, CommonData, process_types, Distance=None):
        self.Report = {}
        self.P_Name = process_name
        self.P_Pr_Name = self.P_Name + '_product'
        self.Distance = Distance
        self.CommonData = CommonData
        self._process_types = process_types

        self.waste_treatment = waste_treatment

        # Databases
        self.database_biosphere = Database("biosphere3")
        self.database_Product = Database(self.P_Pr_Name)
        self.database_Waste_technosphere = Database("Technosphere")

    def check_nan(self, x):  # replace zeros when there is no data ("nan")
        if str(x) == "nan":
            return 0
        return x

    @staticmethod
    def init_DB(DB_name, waste_flows):
        db_data = {}
        for x in waste_flows:
            # add activity to database
            db_data[(DB_name, x)] = {
                'name': DB_name + "_" + x,
                'reference product': DB_name + "_" + x,
                'unit': 'Mg/year',
                'exchanges': []}

        print("""
              ####
              ++++++ Initializing the {}
              """.format(DB_name))

        db = Database(DB_name)
        db.write(db_data)

    def Write_DB(self, waste_flows, parameters, Process_Type):
        """
        .. _Write_DB:

        """
        create_static_parameters = True
        self.db_data = {}
        self.db_Pr_data = {}
        self.parameters = []  # List of dictionaries ({'name':Formula ,'amount':0})
        self.list_of_params = []  # List of parameters name
        self.list_of_static_params = []
        self.act_in_group = set()
        self.params_dict = dict()  # Dictionary that has set() include the key (input,act) for all the exchanges with parameters.
        self.uncertain_parameters = parameters

        for x in waste_flows:    # x is waste fraction
            # add activity to database
            self.db_data[(self.P_Name, x)] = {
                'name': self.P_Name + "_" + x,
                'reference product': self.P_Name + "_" + x,
                'unit': 'Mg/year',
                'exchanges': []}
            if Process_Type == 'Collection':
                self.db_data[(self.P_Name, x)]['unit'] = '{} Mg/year'.format(np.round(sum(self.Report["Waste"][x].values()), decimals=2))
            # Reference flow
            ex = self.exchange(Input=(self.P_Name, x),
                               Type='production',
                               Unit=self.db_data[(self.P_Name, x)]['unit'],
                               Amount=1)
            self.db_data[(self.P_Name, x)]['exchanges'].append(ex)

            if Process_Type == 'Transfer_Station':
                xx = ProcessDB._helper_wasteflow_name(x)
            else:
                xx = x

            for key in self.Report["Waste"][x]:
                ex = self.exchange((self.P_Pr_Name, xx + '_' + key), 'technosphere', 'Mg/year', self.Report["Waste"][x][key])
                self.db_data[(self.P_Name, x)]['exchanges'].append(ex)

                # add activity to Waste_database
                self.db_Pr_data[(self.P_Pr_Name, xx + '_' + key)] = {
                    'name': self.P_Pr_Name + "_" + xx + '_' + key,
                    'reference product': self.P_Pr_Name + "_" + xx + '_' + key,
                    'unit': 'Mg/year',
                    'exchanges': []}
                # Reference flow
                ex = self.exchange(Input=(self.P_Pr_Name, xx + '_' + key),
                                   Type='production',
                                   Unit=self.db_Pr_data[(self.P_Pr_Name, xx + '_' + key)]['unit'],
                                   Amount=1)
                self.db_Pr_data[(self.P_Pr_Name, xx + '_' + key)]['exchanges'].append(ex)
                self.act_in_group.add((self.P_Pr_Name, xx + '_' + key))

                # Streams that are not the same with their source.
                if key in ['Bottom_Ash', 'Fly_Ash', 'RDF'] + self.CommonData.Reprocessing_Index:
                    # finding the destination
                    for p in self.waste_treatment[key]:
                        # adding exchange to waste processing
                        if len(self.waste_treatment[key]) > 1 or not create_static_parameters:
                            Formula = "frac_of_" + key + '_from_' + self.P_Name + '_to_' + p
                        else:
                            Formula = None
                            if "frac_of_" + key + '_from_' + self.P_Name + '_to_' + p not in self.list_of_static_params:
                                self.list_of_static_params.append("frac_of_" + key + '_from_' + self.P_Name + '_to_' + p)
                                self.uncertain_parameters.add_parameter(key, self.P_Name, p, 1, dynamic_param=False)

                        ex = self.exchange((p, key), 'technosphere', 'Mg/year', 0 if Formula else 1, Formula=Formula,
                                           Act=(self.P_Pr_Name, xx + '_' + key), product=key)
                        self.db_Pr_data[(self.P_Pr_Name, xx + '_' + key)]['exchanges'].append(ex)

                        # addin exchange for transportation between the process models
                        ex_trnp = self.exchange((self.P_Pr_Name, self.P_Name + '_' + 'to' + '_' + p), 'technosphere', 'Mg/year',
                                                0 if Formula else 1, Formula=Formula,
                                                Act=(self.P_Pr_Name, xx + '_' + key), product=key)
                        self.db_Pr_data[(self.P_Pr_Name, xx + '_' + key)]['exchanges'].append(ex_trnp)

                # Streams that are same with the source.
                elif key in ['Separated_Organics', 'Other_Residual', 'Separated_Recyclables', 'Unreacted_Ash']:
                    # finding the destination
                    for p in self.waste_treatment[key]:
                        # adding exchange to waste processing
                        if len(self.waste_treatment[key]) > 1 or not create_static_parameters:
                            Formula = "frac_of_" + key + '_from_' + self.P_Name + '_to_' + p
                        else:
                            Formula = None
                            if "frac_of_" + key + '_from_' + self.P_Name + '_to_' + p not in self.list_of_static_params:
                                self.list_of_static_params.append("frac_of_" + key + '_from_' + self.P_Name + '_to_' + p)
                                self.uncertain_parameters.add_parameter(key, self.P_Name, p, 1, dynamic_param=False)

                        # adding exchange to waste processing
                        ex = self.exchange((p, xx), 'technosphere', 'Mg/year', 0 if Formula else 1, Formula=Formula,
                                           Act=(self.P_Pr_Name, xx + '_' + key), product=key)
                        self.db_Pr_data[(self.P_Pr_Name, xx + '_' + key)]['exchanges'].append(ex)

                        # addin exchange for transportation between the process models
                        ex_trnp = self.exchange((self.P_Pr_Name, self.P_Name + '_' + 'to' + '_' + p), 'technosphere', 'Mg/year',
                                                0 if Formula else 1, Formula=Formula,
                                                Act=(self.P_Pr_Name, xx + '_' + key), product=key)
                        self.db_Pr_data[(self.P_Pr_Name, xx + '_' + key)]['exchanges'].append(ex_trnp)

                ### Collection streams.
                # Transportation between the collection and treatment processes are calculate inside collection model.
                elif key in self.CommonData.Collection_Index:
                    # finding the destination
                    for p in self.waste_treatment[key]:
                        # adding exchange to waste processing
                        if len(self.waste_treatment[key]) > 1 or not create_static_parameters:
                            Formula = "frac_of_" + key + '_from_' + self.P_Name + '_to_' + p
                        else:
                            Formula = None
                            if "frac_of_" + key + '_from_' + self.P_Name + '_to_' + p not in self.list_of_static_params:
                                self.list_of_static_params.append("frac_of_" + key + '_from_' + self.P_Name + '_to_' + p)
                                self.uncertain_parameters.add_parameter(key, self.P_Name, p, 1, dynamic_param=False)
                        if self._process_types[p] == 'Transfer_Station':
                            ex = self.exchange(Input=(p, key + '_' + x),
                                               Type='technosphere',
                                               Unit='Mg/year',
                                               Amount=0 if Formula else 1,
                                               Formula=Formula,
                                               Act=(self.P_Pr_Name, xx + '_' + key),
                                               product=key)
                        else:
                            ex = self.exchange(Input=(p, x),
                                               Type='technosphere',
                                               Unit='Mg/year',
                                               Amount=0 if Formula else 1,
                                               Formula=Formula,
                                               Act=(self.P_Pr_Name, xx + '_' + key),
                                               product=key)

                        self.db_Pr_data[(self.P_Pr_Name, xx + '_' + key)]['exchanges'].append(ex)

                        # addin exchange for transportation between the collection sector and treatment processs
                        if p in self.Report['LCI'][key].keys():
                            ex_trnp = self.exchange((self.P_Pr_Name, key + '_' + 'to' + '_' + p), 'technosphere', 'Mg/year',
                                                    0 if Formula else 1, Formula=Formula,
                                                    Act=(self.P_Pr_Name, x + '_' + key), product=key)
                            self.db_Pr_data[(self.P_Pr_Name, xx + '_' + key)]['exchanges'].append(ex_trnp)
                        else:
                            raise ValueError('Inconsistent treatment processes in model and collection')
                else:
                    raise Exception(f'Unknown waste proudct! {key} is not defined in PrcessDB class')

            ### Adding the technosphere exchnages to activities
            for key in self.Report["Technosphere"][x]:
                # if self.Report["Technosphere"][x][key] != 0:
                if True:
                    ex = self.exchange(key, 'technosphere', 'Mg/year', self.Report["Technosphere"][x][key])
                    self.db_data[(self.P_Name, x)]['exchanges'].append(ex)

            ### Adding the biosphere exchnages
            for key in self.Report["Biosphere"][x]:
                # if self.Report["Biosphere"][x][key] != 0:
                if True:
                    ex = self.exchange(key, 'biosphere', 'kg', self.Report["Biosphere"][x][key])
                    self.db_data[(self.P_Name, x)]['exchanges'].append(ex)

            if Process_Type == 'Collection':
                ### Adding activity for transport between the collection and treatment processes
                self._add_transport_from_collection()
            else:
                ### Adding activity for transport between the treatment processes
                self._add_transport_between_processes()

        ### writing the databases
        self._writre_DB_from_dict()

        return(self.parameters, self.act_in_group)

    def _add_transport_from_collection(self):
        """
        Adding activity for transport between the collection and treatment processes
        """
        for y in self.Report["LCI"].keys():
            for m in self.Report["LCI"][y].keys():
                self.db_Pr_data[(self.P_Pr_Name, y + '_' + 'to' + '_' + m)] = {
                    'name': 'LCI' + '_' + y + '_to' + '_' + m,
                    'reference product': 'LCI' + '_' + y + '_to' + '_' + m,
                    'unit': 'Mg/year',
                    'exchanges': []}
                # Reference flow
                ex = self.exchange(Input=(self.P_Pr_Name, y + '_' + 'to' + '_' + m),
                                   Type='production',
                                   Unit=self.db_Pr_data[(self.P_Pr_Name, y + '_' + 'to' + '_' + m)]['unit'],
                                   Amount=1)
                self.db_Pr_data[(self.P_Pr_Name, y + '_' + 'to' + '_' + m)]['exchanges'].append(ex)
                ### Adding exchage to transport activity between the collection and treatment processes
                for n in self.Report["LCI"][y][m].keys():
                    ex = self.exchange(n, 'technosphere' if 'biosphere3' not in n else 'biosphere', '_', self.Report["LCI"][y][m][n])
                    self.db_Pr_data[(self.P_Pr_Name, y + '_' + 'to' + '_' + m)]['exchanges'].append(ex)

    def _add_transport_between_processes(self):
        """
        Adding activity for transport between the treatment processes
        """
        # check whether transportation is needed or not (if no waste is proudced, then no transportation is needed)
        if len(self.db_Pr_data) > 0:
            for p, q in self.Distance.Distance.keys():
                if p == self.P_Name and p != q:
                    self.db_Pr_data[(self.P_Pr_Name, p + '_' + 'to' + '_' + q)] = {
                        'name': 'LCI' + '_' + p + '_' + 'to' + '_' + q,
                        'reference product': 'LCI' + '_' + p + '_' + 'to' + '_' + q,
                        'unit': 'Mg/year',
                        'exchanges': []}
                    # Reference flow
                    ex = self.exchange(Input=(self.P_Pr_Name, p + '_' + 'to' + '_' + q),
                                       Type='production',
                                       Unit=self.db_Pr_data[(self.P_Pr_Name, p + '_' + 'to' + '_' + q)]['unit'],
                                       Amount=1)
                    self.db_Pr_data[(self.P_Pr_Name, p + '_' + 'to' + '_' + q)]['exchanges'].append(ex)
                    ### Adding exchage to transport activity between the treatment processes
                    for mode in self.Distance.Distance[(p, q)].keys():
                        if mode == 'Heavy Duty Truck':
                            ex = self.exchange(('Technosphere', 'Internal_Process_Transportation_Heavy_Duty_Diesel_Truck'),
                                               'technosphere', 'Mg/year', 1000 * self.Distance.Distance[(p, q)][mode], Formula=None,
                                               Act=None, product=None)  # unit converion Mg to kg
                        elif mode == 'Medium Duty Truck':
                            ex = self.exchange(('Technosphere', 'Internal_Process_Transportation_Medium_Duty_Diesel_Truck'),
                                               'technosphere', 'Mg/year', 1000 * self.Distance.Distance[(p, q)][mode], Formula=None,
                                               Act=None, product=None)  # unit converion Mg to kg
                        elif mode == 'Rail':
                            ex = self.exchange(('Technosphere', 'Internal_Process_Transportation_Rail'),
                                               'technosphere', 'Mg/year', 1000 * self.Distance.Distance[(p, q)][mode], Formula=None,
                                               Act=None, product=None)  # unit converion Mg to kg
                        elif mode == 'Barge':
                            ex = self.exchange(('Technosphere', 'Internal_Process_Transportation_Barge'),
                                               'technosphere', 'Mg/year', 1000 * self.Distance.Distance[(p, q)][mode], Formula=None,
                                               Act=None, product=None)  # unit converion Mg to kg
                        elif mode == 'Cargo Ship':
                            ex = self.exchange(('Technosphere', 'Internal_Process_Transportation_Cargo_Ship'),
                                               'technosphere', 'Mg/year', 1000 * self.Distance.Distance[(p, q)][mode], Formula=None,
                                               Act=None, product=None)  # unit converion Mg to kg
                        else:
                            raise ValueError(f'Transport mode {mode} is incorrect!')
                        self.db_Pr_data[(self.P_Pr_Name, p + '_' + 'to' + '_' + q)]['exchanges'].append(ex)

    def _writre_DB_from_dict(self):
        if len(self.db_Pr_data) > 0:
            print("""
                  ####
                  ++++++ Writing the {}
                  """.format(self.P_Pr_Name))

            self.database_Product.write(self.db_Pr_data)

        print("""
              ####
              ++++++ Writing the {}
              """.format(self.P_Name))
        db = Database(self.P_Name)
        db.write(self.db_data)
        self.uncertain_parameters.params_dict.update(self.params_dict)

    def exchange(self, Input, Type, Unit, Amount, Formula=None, Act=None, product=None):
        """
        return exchange in a dictionary format
        """
        exchange = {}
        exchange['amount'] = Amount
        exchange['input'] = Input
        exchange['type'] = Type
        exchange['unit'] = Unit

        if Formula:
            exchange['formula'] = Formula
            if Act is None or product is None:
                raise TypeError('swolfpy error: Act and product are not defined for formula(parameter): {}'.format(Formula))
            if Formula not in self.list_of_params:
                self.parameters.append({'name': Formula, 'amount': 0})
                self.list_of_params.append(Formula)
                self.params_dict[Formula] = set()
                self.params_dict[Formula].add((Input, Act))
                self.uncertain_parameters.add_parameter(product, self.P_Name, Input[0], 0)
            else:
                self.params_dict[Formula].add((Input, Act))

        return(exchange)

    @staticmethod
    def _helper_wasteflow_name(name):
        if 'DryRes' == name[0:6] or 'WetRes' == name[0:6]:
            return(name[7:])
        elif 'ORG' == name[0:3] or 'REC' == name[0:3]:
            return(name[4:])
        else:
            return(None)
