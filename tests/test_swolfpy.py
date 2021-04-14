# -*- coding: utf-8 -*-
"""
Created on Tue May 12 22:40:36 2020

@author: msmsa

Tests for `swolfpy` package.
"""
from swolfpy_inputdata import CommonData
from swolfpy_processmodels import LF, WTE, SF_Col, Distance
from swolfpy import Technosphere
from swolfpy import Project
from brightway2 import Database, projects


def test_demo_swolfpy():
    project_name = 'test_demo'
    technosphere = Technosphere(project_name)
    common_data = CommonData()

    # Treatment processes
    Treatment_processes = {}
    Treatment_processes['LF'] = {'input_type': ['RWC', 'Bottom_Ash', 'Fly_Ash', 'Other_Residual'], 'model': LF()}
    Treatment_processes['WTE'] = {'input_type': ['RWC', 'Other_Residual'], 'model': WTE()}

    # Distance
    data = Distance.create_distance_table(process_names=['LF', 'WTE', 'SF_COl'],
                                          transport_modes=['Heavy Duty Truck'],
                                          default_dist=20)
    distance = Distance(data)

    # Collection_processes:
    # Ony include one single family sector wih residual waste collection
    Collection_processes = {}
    Collection_scheme_SF_COL = SF_Col.scheme()
    Collection_scheme_SF_COL['RWC']['Contribution'] = 1
    # Collection_scheme_SF_COL['RWC']['separate_col']['SSR'] = 1
    # Collection_scheme_SF_COL['RWC']['separate_col']['SSYW'] = 1
    Collection_processes['SF_COl'] = {'input_type': [],
                                      'model': SF_Col('SF_COl', Collection_scheme_SF_COL, Treatment_processes=Treatment_processes,
                                                      Distance=distance)}

    # project
    demo = Project(project_name, common_data, Treatment_processes, distance, Collection_processes, technosphere)
    demo.init_project()
    demo.write_project()

    ### Check the exchanges
    projects.set_current(project_name)

    def check_exhanges(name, report, waste_frac):
        db = Database(name)
        act = db.get(waste_frac)
        tech_flows = report['Technosphere'][common_data.Index[1]].keys()
        waste_flows = report['Waste'][common_data.Index[1]].keys()
        # Check the technosphere and waste flows (Check that the process model's report is the same as data in the Database )
        assert len(act.technosphere()) == len(tech_flows) + len(waste_flows)
        for x in act.technosphere():
            if x.input.key[0] == 'Technosphere':
                assert report['Technosphere'][waste_frac][x.input.key] == x.amount
            elif x.input.key[0] == name + '_product':
                for y in waste_flows:
                    if y in x.input.key[1]:
                        assert report['Waste'][waste_frac][y] == x.amount
        bio_flows = report['Biosphere'][common_data.Index[1]].keys()
        # Check the elementary exchanges
        assert len(act.biosphere()) == len(bio_flows)
        for x in act.biosphere():
            assert report['Biosphere'][waste_frac][x.input.key] == x.amount

    check_exhanges('LF', Treatment_processes['LF']['model'].report(), common_data.Index[1])
    check_exhanges('LF', Treatment_processes['LF']['model'].report(), common_data.Index[5])
    check_exhanges('WTE', Treatment_processes['WTE']['model'].report(), common_data.Index[3])
    check_exhanges('WTE', Treatment_processes['WTE']['model'].report(), common_data.Index[13])

    ### Group the exchanges
    demo.group_exchanges()

    def check_exchanges_with_param(name, report, waste_frac, param_dict):
        db = Database(name + '_product')
        waste_flows = report['Waste'][common_data.Index[1]].keys()

        for y in waste_flows:
            act = db.get(waste_frac + '_' + y)
            if y + name in param_dict:
                assert len(act.technosphere()) >= len(param_dict[y + name])
                for x in act.technosphere():
                    for z in param_dict[y + name]:
                        if x.input.key[0] == z[0]:
                            assert z[1] == x.amount

    check_exchanges_with_param('WTE', Treatment_processes['WTE']['model'].report(), common_data.Index[1],
                               demo.parameters.param_uncertainty_dict)
    check_exchanges_with_param('SF_COl', Treatment_processes['SF_COl']['model'].report(), common_data.Index[1],
                               demo.parameters.param_uncertainty_dict)

    # Update the parameters
    demo.update_parameters(demo.parameters.default_parameters_list())

    # Check that the update_parameters has update the right exchanges
    check_exchanges_with_param('WTE', Treatment_processes['WTE']['model'].report(), common_data.Index[1],
                               demo.parameters.param_uncertainty_dict)
    check_exchanges_with_param('SF_COl', Treatment_processes['SF_COl']['model'].report(), common_data.Index[1],
                               demo.parameters.param_uncertainty_dict)
