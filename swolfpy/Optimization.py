# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 19:35:26 2020

@author: msmsa
"""
from .LCA_matrix import LCA_matrix
import numpy as np
import pandas as pd
from scipy.optimize import minimize
import plotly.graph_objects as go
from plotly.offline import plot
from copy import deepcopy
import json
from multiprocessing import Pool, cpu_count, TimeoutError
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial
import os
import pyDOE
from time import time
from brightway2 import projects


class Optimization(LCA_matrix):
    """

    :param functional_unit:
    :type functional_unit: dict
    :param method:
    :type method: lsit
    :param project:
    :type project: ``swolfpy.Project.Project``

    """
    def __init__(self, functional_unit, method, project):
        super().__init__(functional_unit, method)
        self.project = project
        self.Treatment_processes = deepcopy(self.project.Treatment_processes)
        self.Collection_processes = deepcopy(self.project.Collection_processes)
        self.N_param = len(self.project.parameters_list)

        self.n_scheme_vars = 0

    @staticmethod
    def config(project):
        columns = []
        schemes = {}
        for col in project.Collection_processes:
            columns.append(col)
            columns.append(col + ' mode')
            schemes[col] = project.Collection_processes[col]['model'].col_schm

        index = [('RWC', 'N/A', 'N/A'),
                 ('RWC', 'N/A', 'SSR'),
                 ('RWC', 'SSYW', 'N/A'),
                 ('RWC', 'SSYW', 'SSR'),
                 ('RWC', 'SSO', 'N/A'),
                 ('RWC', 'SSO', 'SSR'),
                 ('RWC', 'SSO_AnF', 'N/A'),
                 ('RWC', 'SSO_AnF', 'SSR'),
                 ('REC_WetRes', 'N/A', 'REC_WetRes'),
                 ('REC_WetRes', 'SSYW', 'REC_WetRes'),
                 ('REC_WetRes', 'SSO', 'REC_WetRes'),
                 ('REC_WetRes', 'SSO_AnF', 'REC_WetRes'),
                 ('ORG_DryRes', 'ORG_DryRes', 'N/A'),
                 ('ORG_DryRes', 'ORG_DryRes', 'SSR')]

        config_pd = pd.DataFrame(index=index, columns=columns)
        if len(config_pd.columns) > 0:
            for c in columns[1::2]:
                config_pd[c] = ['Optimize', 'Optimize',
                                'Optimize', 'Optimize',
                                'Optimize', 'Optimize',
                                'Fix', 'Fix',
                                'Fix', 'Fix', 'Fix',
                                'Fix', 'Fix', 'Fix']

            for col, sch in schemes.items():
                for k, v in sch.items():
                    if k in index:
                        config_pd[col][k] = v
        return config_pd.fillna(0.0)

    def set_config(self, config):
        self.config = config
        self.scheme_vars_index = self.N_param
        self.scheme_vars_dict = {}
        self.x0_col = []

        for c in self.config.columns[1::2]:
            for i in self.config.index:
                if self.config[c][i] == 'Optimize':
                    self.scheme_vars_dict[self.scheme_vars_index] = (c.split(' mode')[0], i)
                    self.x0_col.append(self.config[c.split(' mode')[0]][i])
                    self.scheme_vars_index += 1
                    self.n_scheme_vars += 1

        for process in self.config.columns[0::2]:
            for schm in self.config.index:
                if schm in self.Treatment_processes[process]['model'].col_schm:
                    self.Treatment_processes[process]['model'].col_schm[schm] = self.config.loc[[schm], process].values[0]

    def update_col_scheme(self, x):
        process_set = set()
        if self.n_scheme_vars:
            for k, v in self.scheme_vars_dict.items():
                process = v[0]
                process_set.add(process)
                self.Treatment_processes[process]['model'].col_schm[v[1]] = x[k]
            for process in process_set:
                self.Treatment_processes[process]['model']._normalize_scheme(DropOff=False, warn=False)

    ### Objective function
    def _objective_function(self, x):
        """
        Use the new parameters (Waste fractions) to update the ``tech_matrix`` (``tech_param``)
        and reculate the LCA score.
        """
        if self.oldx != list(x):  # Calculations are done only when the function get new x.
            if self.oldx[0:self.N_param] != list(x)[0:self.N_param]:
                param_exchanges = self.project.parameters.Param_exchanges(x[0:self.N_param])
                for key, value in param_exchanges.items():
                    if key in self.tech_matrix:
                        self.tech_matrix[key] = value

            if self.collection and self.oldx[self.N_param:] != list(x)[self.N_param:]:
                self.update_col_scheme(x)
                for col in self.Collection_processes:
                    model = self.Treatment_processes[col]['model']
                    model.calc()
                    report_dict = model.report()
                    process_name = model.process_name
                    LCA_matrix.update_techmatrix(process_name, report_dict, self.tech_matrix)
                    LCA_matrix.update_biomatrix(process_name, report_dict, self.bio_matrix)

            tech = np.array(list(self.tech_matrix.values()), dtype=float)
            bio = np.array(list(self.bio_matrix.values()), dtype=float)

            self.rebuild_technosphere_matrix(tech)
            self.rebuild_biosphere_matrix(bio)
            self.lci_calculation()
            if self.lcia:
                self.lcia_calculation()

            self.oldx = list(x)
        return(self.score / 10**self.magnitude)

    ### Mass to process
    def get_mass_flow(self, key, KeyType, x):
        """
        calculate the mass to the process from the `supply_array` matrix.
        """
        self._objective_function(x)

        mass_flow = 0
        if KeyType == 'WasteToProcess':
            for i in range(len(self.supply_array)):
                if key == self.activities_dict[i]:
                    mass_flow += self.supply_array[i]

        elif KeyType == 'Process':
            for i in range(len(self.supply_array)):
                if key == self.activities_dict[i][0]:
                    mass_flow += self.supply_array[i]
        else:
            raise ValueError(""" KeyType for the get_mass_flow function is not defined correct.""")
        return mass_flow

    ### Emission flow in LCI
    def get_emission_amount(self, emission, x):
        """
        calculate the mass of the `emission` to biosphere from the `inventory`.
        """
        self._objective_function(x)
        inventory = self.biosphere_matrix * self.supply_array
        emission_amount = 0
        for i in range(len(inventory)):
            if emission == self.biosphere_dict[i]:
                emission_amount += inventory[i]
        return emission_amount

    ### Calculates impacts other than objective
    def get_impact_amount(self, impact, x):
        """
        Calculates impacts other than objective.
        """
        self._objective_function(x)
        self.switch_method(impact)
        self.lcia()
        score = self.score
        self.switch_method(self._base_method)
        self.lcia()
        return score

    def _create_equality(self, N_param_Ingroup):
        """
        Check that the sum of parameters in each group should be one.
        """
        local_index = self.Param_index
        f = (lambda x: sum([x[i] for i in range(local_index, local_index + N_param_Ingroup)]) - 1)
        self.Param_index += N_param_Ingroup
        return f

    def _create_inequality(self, key, limit, KeyType, ConstType):
        """

        :param key: process name, key for activtity in process or key for activity in biosphere
        :type key: str or tuple
        :param limit:
        :type limit: float
        :param KeyType: ``"Process"``, ``"WasteToProcess"``, ``"Emission"``
        :type KeyType: str
        :param ConstType: ``"<="`` , ``">="``
        :type ConstType: str

        """
        if ConstType not in ['<=', '>=']:
            raise ValueError(" Constraint Type is not defined correct ")

        if KeyType == 'Process':
            if ConstType == '<=':
                f = (lambda x: limit - self.get_mass_flow(key, KeyType, x))
            else:
                f = (lambda x: self.get_mass_flow(key, KeyType, x) - limit)
            return f

        elif KeyType == 'WasteToProcess':
            if ConstType == '<=':
                f = (lambda x: limit - self.get_mass_flow(key, KeyType, x))
            else:
                f = (lambda x: self.get_mass_flow(key, KeyType, x) - limit)
            return f

        elif KeyType == 'Emission':
            if ConstType == '<=':
                f = (lambda x: limit - self.get_emission_amount(key, x))
            else:
                f = (lambda x: self.get_emission_amount(key, x) - limit)
            return f

        elif KeyType == 'Impact':
            if ConstType == '<=':
                f = (lambda x: limit - self.get_impact_amount(key, x))
            else:
                f = (lambda x: self.get_impact_amount(key, x) - limit)
            return f

    def _create_collection_constraints(self, cons):
        const_dict = {}
        if self.n_scheme_vars:
            for k in self.scheme_vars_dict:
                process = self.scheme_vars_dict[k][0]
                if process not in const_dict:
                    const_dict[process] = []
                const_dict[process].append(k)
        print("\n\n collection constraints dict: \n", const_dict, '\n\n')

        for k in const_dict:
            self._col_const_helper(const_dict, k, cons)

    def _col_const_helper(self, const_dict, k, cons):
        def helper_sum(x, index):
            return(sum([x[i] for i in index]))

        fix = 0
        for i in self.config.index:
            if self.config[k + ' mode'][i] == 'Fix':
                fix += self.config[k][i]
        cons.append({'type': 'eq',
                     'fun': (lambda x: helper_sum(x, const_dict[k]) + fix - 1),
                     'Name': '{} main const'.format(k)})

    def _create_constraints(self):
        cons = list()
        group = dict()

        # Index for the parameters
        self.Param_index = 0

        # Number of parameters in each group (from one source to different denstinations)
        for key in self.project.parameters.param_uncertainty_dict.keys():
            group[key] = len(self.project.parameters.param_uncertainty_dict[key])

        # Equal constraint (sum of the parameters in each group should be one)
        for vals in group.values():
            cons.append({'type': 'eq',
                         'fun': self._create_equality(N_param_Ingroup=vals)})

        if self.collection and self.n_scheme_vars:
            self._create_collection_constraints(cons)

        if self.constraints:
            for key in self.constraints.keys():
                cons.append({'type': 'ineq',
                             'fun': self._create_inequality(key, self.constraints[key]['limit'], self.constraints[key]['KeyType'],
                                                            self.constraints[key]['ConstType'])})
        return cons

    @staticmethod
    def multi_start_optimization(optObject, constraints=None, collection=False, n_iter=30,
                                 nproc=None, timeout=None, initialize_guess='random'):
        """
        Call the ``scipy.optimize.minimize()`` to minimize the LCA score. \n
        ``constraints`` is python dictionary. \n
        Constraint type can be ``'<='`` or ``'>='``. \n
        Three kind of constraints are defined as below: \n
        * **Process:** Constraint on the total mass to the processs. The ``'KeyType'`` should be ``'Process'``
          (e.g., The capacity of the WTE). Examaple:

        >>> constraints = {}
        >>> # Use name the the process as key in dict
        >>> constraints['WTE'] = {'limit':100, 'KeyType':'Process','ConstType':"<="}

        * **WasteToProcess:** Constraint on the total mass of waste fraction to the processs. The ``'KeyType'`` should
          be ``'WasteToProcess'`` (e.g., Ban food waste from landfill). Examaple:

        >>> constraints = {}
        >>> # Use database key as key in dict
        >>> constraints[('LF','Food_Waste_Vegetable')] = {'limit':0, 'KeyType':'WasteToProcess','ConstType':"<="}

        * **Emission:** Constraint on the emissions. The ``'KeyType'`` should be ``'Emission'`` (e.g., CO2 emissions Cap). Examaple:

        >>> constraints = {}
        >>> # Use database key as key in dict
        >>> constraints[('biosphere3', 'eba59fd6-f37e-41dc-9ca3-c7ea22d602c7')] = {'limit':100,'KeyType':'Emission','ConstType':"<="}

        """
        optObject.constraints = constraints
        optObject.collection = collection

        optObject.magnitude = len(str(int(abs(optObject.score))))

        global_min = 1E100

        if optObject.collection:
            n_dec_vars = len(optObject.project.parameters_list) + optObject.n_scheme_vars
        else:
            n_dec_vars = len(optObject.project.parameters_list)

        bnds = tuple([(0, 1) for _ in range(n_dec_vars)])

        args = []
        if initialize_guess == 'LHS':
            all_x0 = pyDOE.lhs(n_dec_vars, samples=n_iter)
        elif initialize_guess == 'random':
            all_x0 = np.random.rand(n_iter, n_dec_vars)
        elif initialize_guess == 'binary':
            all_x0 = np.random.randint(low=0,
                                       high=2,
                                       size=(n_iter, n_dec_vars))
        else:
            raise ValueError(f'The {initialize_guess} method for generating the initial guess is not correct!')

        for j in range(n_iter):
            args.append((optObject, bnds, all_x0[j], j))

        if not nproc:
            nproc = cpu_count()

        all_results = []
        pool = Pool(processes=nproc, maxtasksperchild=1)
        for arg in args:
            abortable_func = partial(Optimization.abortable_worker, Optimization.worker, timeout=timeout)
            all_results.append(pool.apply_async(abortable_func, args=arg))
        results = [res.get() for res in all_results]
        pool.close()
        pool.join()
        optObject.all_results = results

        optObject.res_global = False
        for i, res in enumerate(optObject.all_results):
            if res:
                if res.success:
                    if res.fun < global_min:
                        optObject.res_global = res
                        global_min = res.fun
                print("""\n
                      Iteration: {}
                      Status: {}, Message: {}
                      Objective function: {}
                      Global min: {} \n
                      """.format(i,
                                 res.success, res.message,
                                 res.fun * 10**optObject.magnitude,
                                 global_min * 10**optObject.magnitude))
            else:
                print("""\n
                      Iteration: {}
                      Status: {}, Message: {}
                      Objective function: {}
                      Global min: {} \n
                      """.format(i,
                                 False, 'Aborting due to timeout!',
                                 'NAN',
                                 global_min * 10**optObject.magnitude))

        if not optObject.res_global:
            optObject.success = False
            print('None of the iterations were successful!')
            return None

        if optObject.res_global.success:
            optObject.oldx = [0 for i in range(n_dec_vars)]
            optObject.success = True
            optObject.optimized_x = list()
            optObject.res_global.x = optObject.res_global.x.round(decimals=4)
            optObject._objective_function(optObject.res_global.x)

            for i in range(len(optObject.project.parameters_list)):
                optObject.optimized_x.append({'name': optObject.project.parameters_list[i]['name'],
                                              'amount': optObject.res_global.x[i]})

            if optObject.collection:
                for k, v in optObject.scheme_vars_dict.items():
                    optObject.optimized_x.append({'name': v,
                                                  'amount': optObject.res_global.x[k]})

            return optObject.res_global
        else:
            optObject.success = False
            print(optObject.res_global.message)
            return optObject.res_global

    @staticmethod
    def abortable_worker(func, *args, **kwargs):
        iteration = args[3]
        timeout = kwargs.get('timeout', None)
        p = ThreadPool(1)
        res = p.apply_async(func, args)
        try:
            return(res.get(timeout))  # Wait timeout seconds for func to complete.
        except TimeoutError:
            print("(Iteration:{}, PID:{}): Aborting due to timeout!".format(iteration, os.getpid()))
            return None

    @staticmethod
    def worker(optObject, bnds, x0, iteration):
        start = time()
        projects.set_current(optObject.project.project_name, writable=False)
        print("Iteration: {} PID: {}\n".format(iteration, os.getpid()))
        optObject.oldx = [0 for i in range(len(x0))]
        optObject.cons = optObject._create_constraints()
        res = minimize(optObject._objective_function, x0, method='SLSQP', bounds=bnds, constraints=optObject.cons)

        time_ = round(time() - start)
        print("Iteration: {} PID: {} time:{} sec, Success:{} \n".format(iteration,
                                                                        os.getpid(),
                                                                        time_,
                                                                        res.success))
        res['time'] = time_
        res['PID'] = os.getpid()
        return(res)

    def set_optimized_parameters_to_project(self):
        assert hasattr(self, "project"), "Must run optimize_parameters first"
        assert self.success, "Optimization has to be sucessful first"

        self.project.update_parameters(self.optimized_x)

    def plot_sankey(self, optimized_flow=True, show=True, fileName=None, params=None):
        """Plots a sankey diagram for the waste mass flows. \n
        Calls the ``plotly.graph_objs.Sankey`` to plot sankey. \n
        Calculates the mass flows by calling ``self.get_mass_flow()``. \n

        :param optimized_flow: If ``True``, it plots the sankey based on the optimized waste fractions.
                                If ``False``, it plost the sankey based on the current waste fractions by calling ``self.project.parameters_list``.
        :type optimized_flow: bool

        :param show: If ``True``, it will show the figure
        :type show: bool

        """
        if optimized_flow:
            params = [i['amount'] for i in self.optimized_x]
        else:
            if params:
                params = params
            else:
                params = [i['amount'] for i in self.project.parameters_list]

            self.oldx = [0 for i in range(len(params))]
            self.magnitude = len(str(int(abs(self.score))))
            self.N_param = len(self.project.parameters_list)
            self.col_model = []

        product = []
        index = 0
        for _, i in self.project.parameters.param_uncertainty_dict.items():
            for j in i:
                product.append((j[3], params[index]))
                index += 1
        for _, i in self.project.parameters.static_param_dict.items():
            for j in i:
                product.append((j[3], 1))

        label = self.project.parameters.nodes
        source = []
        target = []
        value = []
        label_link = []
        color = []

        # Color & shape for plotting the SWM Network
        # https://www.rapidtables.com/web/color/RGB_Color.html
        edge_color = {'RWC': (160, 82, 45),  # sienna	#A0522D
                      'SSR': (0, 0, 255),  # blue	#0000FF
                      'DSR': (0, 0, 205),  # medium blue	#0000CD
                      'MSR': (65, 105, 225),  # royal blue	#4169E1
                      'LV': (0, 255, 0),  # lime	#00FF00
                      'SSYW': (0, 100, 0),  # dark green	#006400
                      'SSO': (0, 255, 127),  # spring green	#00FF7F
                      'SSO_HC': (128, 128, 0),  # olive #808000
                      'SSO_AnF': (127, 255, 0),  # chartreuse #7FFF00
                      'ORG': (46, 139, 87),  # sea green	#2E8B57
                      'DryRes': (222, 184, 135),  # burly wood	#DEB887
                      'REC': (0, 191, 255),  # deep sky blue	#00BFFF
                      'WetRes': (210, 105, 30),  # chocolate	#D2691E
                      'MRDO': (205, 133, 63),  # peru	#CD853F
                      'SSYWDO': (107, 142, 35),  # olive drab	#6B8E23
                      'MSRDO': (106, 90, 205),  # slate blue	#6A5ACD
                      'Bottom_Ash': (128, 128, 128),  # Gray	#808080
                      'Fly_Ash': (0, 0, 0),  # black	#000000
                      'Unreacted_Ash': (128, 128, 128),  # Gray	#808080
                      'Separated_Organics': (50, 205, 50),  # lime green	#32CD32
                      'Separated_Recyclables': (0, 128, 128),  # teal	#008080
                      'Other_Residual': (139, 69, 19),  # saddle brown	#8B4513
                      'RDF': (255, 0, 0)}  # Red	#FF0000
        for i in self.project.CommonData.Reprocessing_Index:
            edge_color[i] = (0, 0, 139)  # dark blue	#00008B

        for x in product:
            key, frac = x
            source.append(label.index(key[0]))
            target.append(label.index(key[1]))
            label_link.append(key[2])
            # color.append('rgba({},{},{}, 0.8)'.format(*np.random.randint(256, size=3)))
            color.append('rgba({}, {}, {}, 0.8)'.format(*edge_color[key[2]]))
            mass = 0.0
            for m in self.project.CommonData.Index + ['RDF']:
                mass += self.get_mass_flow((key[0] + '_product', m + '_' + key[2]), 'WasteToProcess', params)
                mass += self.get_mass_flow((key[0] + '_product', key[2]), 'WasteToProcess', params)

            value.append(np.round(mass * frac, 3))

        print("""
              # Sankey Mass flows
              label = {}
              source = {}
              target = {}
              label_link = {}
              value = {}""".format(label, source, target, label_link, value))

        node = dict(pad=20,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=label,
                    color='rgba({}, {}, {}, 0.8)'.format(*(176, 196, 222)))  # light steel blue	#B0C4DE

        link = dict(source=source,
                    target=target,
                    value=value,
                    label=label_link,
                    color=color)

        # The other good option for the valueformat is ".3f". Yes
        score = self._objective_function(params) * 10**self.magnitude
        if score >= 1000 or score <= -1000:
            score = "{:,.0f}".format(score)
        elif score <= 0.1 and score >= -0.1:
            score = "{:,.4f}".format(score)
        elif score <= 1 and score >= -1:
            score = "{:,.3f}".format(score)
        else:
            score = "{:,.2f}".format(score)

        layout = go.Layout(title_text="LCIA: " + str(self.method[0]) + f"= {score}",
                           font_size=16,
                           hoverlabel=dict(font_size=14))
        data = go.Sankey(valueformat=".3s",
                         valuesuffix="Mg",
                         node=node,
                         link=link)
        fig = go.Figure(data=[data], layout=layout)
        plot(fig, filename=fileName if fileName else 'plot.html', auto_open=show)

        # Store data for ploting the sankey
        store_data = {}
        store_data['title_text'] = "Impact " + str(self.method[0]) + f": {score}"
        store_data['font_size'] = 16
        store_data['hoverlabel'] = dict(font_size=14)
        store_data['valueformat'] = ".3s"
        store_data['valuesuffix'] = "Mg"
        store_data['node'] = node
        store_data['link'] = link

        filename = fileName.split('.')[0] + '.JSON' if fileName else 'Sankey_Data.JSON'
        with open(filename, 'w') as outfile:
            json.dump(store_data, outfile, indent=4)
