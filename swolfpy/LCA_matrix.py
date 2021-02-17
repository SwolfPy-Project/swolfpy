# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 19:09:14 2020

@author: msmsa
"""
from brightway2 import LCA
import numpy as np


class LCA_matrix(LCA):
    """
    This class translate the ``row`` and ``col`` of the ``tech_param`` and ``bio_param`` to
    the acticity `key` in the Brightway2 database. \n
    Both the ``tech_param`` and ``bio_param`` has the ``dtype=[('input', '<u4'), ('output', '<u4'),
    ('row', '<u4'), ('col', '<u4'), ('type', 'u1'), ('uncertainty_type', 'u1'), ('amount', '<f4'),
    ('loc', '<f4'), ('scale', '<f4'), ('shape', '<f4'), ('minimum', '<f4'), ('maximum', '<f4'),
    ('negative', '?')])`` data type. \n

    ``self.tech_matrix`` is a dictionary that includes all the technosphere and waste exhanges as tuple ``(product,Feed)`` key and amount as value:
    ``{(('LF', 'Aerobic_Residual'), ('SF1_product', 'Aerobic_Residual_MRDO')):0.828}``

    ``self.bio_matrix`` is a dictionary taht includes all the biosphere exhanges as tuple ``(product,Feed)`` `key` and amount as `value`
    ``{(('biosphere3', '0015ec22-72cb-4af1-8c7b-0ba0d041553c'), ('Technosphere', 'Boiler_Diesel')):6.12e-15}``

    So we can update the ``tech_params`` and ``bio_params`` by tuple keys that are consistant with the keys
    in the ``ProcessMolde.report()``. Check :ref:`Process models class <ProcessModel>` for more info.
    """
    def __init__(self, functional_unit, method):
        super().__init__(functional_unit, method[0])
        self.lci()
        self.lcia()

        self.functional_unit = functional_unit
        self.method = method

        self.activities_dict, _, self.biosphere_dict = self.reverse_dict()

        self.tech_matrix = dict()
        for i in self.tech_params:
            self.tech_matrix[(self.activities_dict[i[2]], self.activities_dict[i[3]])] = i[6]

        self.bio_matrix = dict()
        for i in self.bio_params:
            if (self.biosphere_dict[i[2]], self.activities_dict[i[3]]) not in self.bio_matrix.keys():
                self.bio_matrix[(self.biosphere_dict[i[2]], self.activities_dict[i[3]])] = i[6]
            else:
                self.bio_matrix[(str(self.biosphere_dict[i[2]]) + " - 1", self.activities_dict[i[3]])] = i[6]
                # print((str(biosphere_dict[i[2]]) + " - 1", activities_dict[i[3]]))

    @staticmethod
    def update_techmatrix(process_name, report_dict, tech_matrix):
        for material, value in report_dict["Technosphere"].items():
            for key2, value2 in value.items():
                if not np.isnan(value2):
                    if ((key2), (process_name, material)) in tech_matrix.keys():
                        if tech_matrix[((key2), (process_name, material))] != value2:
                            tech_matrix[((key2), (process_name, material))] = value2
                    else:
                        raise KeyError('Exchange {} is calculated but not exist in LCA technosphere'.format(((key2), (process_name, material))))
                else:
                    raise ValueError('Amount for Exchange {} is Nan. The amount should be number, check the calculations in the process model'
                                     .format(((key2), (process_name, material))))

        for material, value in report_dict["Waste"].items():
            for key2, value2 in value.items():
                key2 = (process_name + "_product", material + '_' + key2)
                if not np.isnan(value2):
                    if ((key2), (process_name, material)) in tech_matrix.keys():
                        if tech_matrix[((key2), (process_name, material))] != value2:
                            tech_matrix[((key2), (process_name, material))] = value2
                    else:
                        raise KeyError('Exchange {} is calculated but not exist in LCA technosphere'.format(((key2), (process_name, material))))

                else:
                    raise ValueError('Amount for Exchange {} is Nan. The amount should be number, check the calculations in the process model'
                                     .format(((key2), (process_name, material))))

            ### Adding activity for transport between the collection and treatment processes
            if 'LCI' in report_dict.keys():
                for y in report_dict["LCI"].keys():
                    for m in report_dict["LCI"][y].keys():
                        for n in report_dict["LCI"][y][m].keys():
                            if 'biosphere3' not in n:
                                if not np.isnan(report_dict["LCI"][y][m][n]):
                                    if (n, (process_name + '_product', y + '_' + 'to' + '_' + m)) in tech_matrix.keys():
                                        if tech_matrix[(n, (process_name + '_product', y + '_' + 'to' + '_' + m))] != report_dict["LCI"][y][m][n]:
                                            tech_matrix[(n, (process_name + '_product', y + '_' + 'to' + '_' + m))] = report_dict["LCI"][y][m][n]
                                    else:
                                        raise KeyError('Exchange {} is calculated but not exist in LCA technosphere'
                                                       .format((n, (process_name + '_product', y + '_' + 'to' + '_' + m))))
                                else:
                                    raise ValueError("""Amount for Exchange {} is Nan. The amount should be number,
                                                     check the calculations in the process model"""
                                                     .format((n, (process_name + '_product', y + '_' + 'to' + '_' + m))))

    @staticmethod
    def update_biomatrix(process_name, report_dict, bio_matrix):
        for material, value in report_dict["Biosphere"].items():
            for key2, value2 in value.items():
                if not np.isnan(value2):
                    if bio_matrix[((key2), (process_name, material))] != value2:
                        bio_matrix[((key2), (process_name, material))] = value2
                else:
                    raise ValueError('Amount for Exchange {} is Nan. The amount should be number, check the calculations in the process model'
                                     .format(((key2), (process_name, material))))
            ### Adding activity for collection cost
            if 'LCI' in report_dict.keys():
                for y in report_dict["LCI"].keys():
                    for m in report_dict["LCI"][y].keys():
                        for n in report_dict["LCI"][y][m].keys():
                            if 'biosphere3' in n:
                                if not np.isnan(report_dict["LCI"][y][m][n]):
                                    if (n, (process_name + '_product', y + '_' + 'to' + '_' + m)) in bio_matrix.keys():
                                        if bio_matrix[(n, (process_name + '_product', y + '_' + 'to' + '_' + m))] != report_dict["LCI"][y][m][n]:
                                            bio_matrix[(n, (process_name + '_product', y + '_' + 'to' + '_' + m))] = report_dict["LCI"][y][m][n]
                                    else:
                                        raise KeyError('Exchange {} is calculated but not exist in LCA biosphere'
                                                       .format((n, (process_name + '_product', y + '_' + 'to' + '_' + m))))
                                else:
                                    raise ValueError("""Amount for Exchange {} is Nan. The amount should be number,
                                                     check the calculations in the process model"""
                                                     .format((n, (process_name + '_product', y + '_' + 'to' + '_' + m))))
