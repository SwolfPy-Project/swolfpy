# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 19:45:04 2020

@author: msmsa
"""
import numpy as np
import pandas as pd
import os
from .LCA_matrix import LCA_matrix
import multiprocessing as mp
from brightway2 import LCA, projects


class Monte_Carlo(LCA_matrix):
    """Setups the Monte Carlo simulation. This class is inherited from ``swolfpy.LCA_matrix``. \n
    The Monte Carlo simulation will be only done for  the process models, common data
    or parameters than the class gets by arguments.

    :param functional_unit: ``{flow:amount}``
    :type functional_unit: dict

    :param method: List of methods for MC.
    :type method: list

    :param project: Name of the project.
    :type project: str

    :param process_models: list of the process models.
    :type process_models: list, optional

    :param process_model_names: list of process models' names.
    :type process_model_names: list, optional

    :param common_data: ``CommonData`` object.
    :type common_data: ``swolfpy_inputdata.CommonData.CommonData`` , optional

    :param parameters: ``Parameters`` object
    :type parameters: ``swolfpy_inputdata.Parameters.Parameters``,optional

    :param seed: seed for ``stats_arrays.RandomNumberGenerator``
    :type seed: int, optional

    """
    def __init__(self, functional_unit, method, project, process_models=None, process_model_names=None,
                 common_data=None, parameters=None, seed=None):
        super().__init__(functional_unit, method)

        self.process_models = process_models
        self.process_model_names = process_model_names
        self.parameters = parameters
        self.common_data = common_data
        self.project = project
        if seed:
            self.seed = seed
        else:
            self.seed = 0

    def run(self, nproc, n):
        """ Runs the Monte Carlo ``n`` times with ``nproc`` processors. Calls and map the ``Monte_Carlo.worker()`` to the processors.

        :param nproc: Number of processors allocated to MC
        :type nproc: int
        :param n: Number of iterations in MC
        :type n: int

        """

        def pool_adapter(x):
            return(x)

        with pool_adapter(mp.Pool(processes=nproc)) as pool:
            res = pool.map(Monte_Carlo.worker,
                           [(self.project, self.functional_unit, self.method, self.parameters, self.process_models,
                             self.process_model_names, self.common_data, self.tech_matrix, self.bio_matrix, self.seed + i * 100, n // nproc)
                            for i in range(nproc)])
        self.results = [x for lst in res for x in lst]
# =============================================================================
#         res = Monte_Carlo.worker((self.project, self.functional_unit, self.method, self.parameters, self.process_models, self.process_model_names,
#                                   self.common_data, self.tech_matrix, self.bio_matrix, self.seed, n//nproc))
#         self.results = [x for lst in res for x in lst]
# =============================================================================

    @staticmethod
    def worker(args):
        """
        Setups the Monte Carlo for process models and input data and then creates the ``LCA`` object
        and Calls the ``Monte_Carlo.parallel_mc()`` for `n` times.
        """
        project, functional_unit, method, parameters, process_models, process_model_names, common_data, tech_matrix, bio_matrix, seed, n = args
        projects.set_current(project, writable=False)
        if common_data:
            common_data.setup_MC(seed + 100000)
        if process_models:
            for seed_, x in enumerate(process_models):
                x.setup_MC(seed + seed_)
        if parameters:
            parameters.setup_MC(seed + 200000)

        lca = LCA(functional_unit, method[0])
        lca.lci()
        lca.lcia()
        return [Monte_Carlo.parallel_mc(lca, project, functional_unit, method, tech_matrix, bio_matrix, process_models=process_models,
                process_model_names=process_model_names, parameters=parameters, common_data=common_data, index=x)
                for x in range(n)]

    @staticmethod
    def parallel_mc(lca, project, functional_unit, method, tech_matrix, bio_matrix, process_models=None, process_model_names=None,
                    parameters=None, common_data=None, index=None):
        """
        Calls the ``InputData.gen_MC()`` , ``ProcessModel.MC_calc()``  and ``parameters.MC_calc()`` and then gets the new LCI and updates
        the ``tech_matrix`` and ``bio_matrix``. Creates new ``bio_param`` and ``tech_param`` and then recalculate the LCA.

        """
        uncertain_inputs = list()
        if process_models:
            if common_data:
                uncertain_inputs += common_data.gen_MC()
                for process in process_models:
                    process.CommonData = common_data
                    uncertain_inputs += process.MC_calc()
            else:
                for process in process_models:
                    uncertain_inputs += process.MC_calc()

            i = 0
            for process_name in process_model_names:
                report_dict = process_models[i].report()
                LCA_matrix.update_techmatrix(process_name, report_dict, tech_matrix)
                LCA_matrix.update_biomatrix(process_name, report_dict, bio_matrix)
                i += 1

        if parameters:
            param_exchanges, params = parameters.MC_calc()
            uncertain_inputs += params
            for key, value in param_exchanges.items():
                if key in tech_matrix:
                    tech_matrix[key] = value

        tech = np.array(list(tech_matrix.values()), dtype=float)
        bio = np.array(list(bio_matrix.values()), dtype=float)

        lca.rebuild_technosphere_matrix(tech)
        lca.rebuild_biosphere_matrix(bio)
        lca.lci_calculation()
        if lca.lcia:
            lca.lcia_calculation()

        lca_results = dict()
        lca_results[method[0]] = lca.score

        if len(method) > 1:
            for i in range(1, len(method)):
                lca.switch_method(method[i])
                lca.lcia_calculation()
                lca_results[method[i]] = lca.score
            lca.switch_method(method[0])
        print(os.getpid(), index)
        return(os.getpid(), lca_results, uncertain_inputs)

    ### Export results
    def result_to_DF(self):
        """ Returns the results from the Monte Carlo in a ``pandas.DataFrame`` format.

        :return: Monte Carlo results
        :rtype: ``pandas.DataFrame``
        """
        output = pd.DataFrame()
        # Reporting the LCIA results; Create a column for each method
        for j in self.results[0][1].keys():
            output[j] = [self.results[i][1][j] for i in range(len(self.results))]
        # Reporting the input data
        for j in range(len(self.results[0][2])):
            output[self.results[0][2][j][0]] = [self.results[i][2][j][1] for i in range(len(self.results))]
        return(output)

    def save_results(self, name):
        """ Save the results from the Monte Carlo to pickle file.
        """
        self.result_to_DF().to_pickle(name)
