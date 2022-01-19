# -*- coding: utf-8 -*-
"""
Created on Wed May 29 12:13:23 2019

@author: msmsa
"""
from brightway2 import projects, Database, parameters, LCA, get_activity, calculation_setups, MultiLCA, Method
from bw2data.parameters import ActivityParameter
from .ProcessDB import ProcessDB
from bw2analyzer import ContributionAnalysis
from .Parameters import Parameters
from .Technosphere import Technosphere
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class Project():
    """
    Project class creates a new project in Birghtway2.

    :param project_name: Name for the project
    :type project_name: str

    :param CommonData: CommonData object
    :type CommonData: class: `swolfpy.ProcessMoldes.CommonData`

    :param Treatment_processes: Dictionary for treatment processes include their input type and model.
    :type Treatment_processes: dict

    :param Distance: Distance object.
    :type Distance: class: `swolfpy.Distance.Distance`

    :param Collection_processes: Dictionary for collection processes include their input type and model.
        Input type for the collection process is empty list ``[]`` as they don't accept waste from other processes.
    :type Collection_processes: dict, optional

    .. note:: Treatment processes and distance between them are required for creating a project.
                Collection processes are not required unless they are included in the system boundary.

    :Create sample project:

    Step 1: Create CommonData and Treatment_processes dict with LF and WTE:

    >>> from swolfpy_inputdata import CommonData
    >>> from swolfpy_processmodels import LF
    >>> from swolfpy_processmodels import WTE
    >>> common_data = CommonData()
    >>> Treatment_processes = {}
    >>> Treatment_processes['LF']={'input_type':['RWC','Bottom_Ash','Fly_Ash','Other_Residual'],'model': LF()}
    >>> Treatment_processes['WTE']={'input_type':['RWC','Other_Residual'],'model': WTE()}

    Step 2: Create :ref:`Distance <Distance>` object:

    >>> from swolfpy_processmodels import Distance
    >>> import pandas as pd
    >>> Processes = ['LF','WTE','SF_COl']
    >>> data = Distance.create_distance_table(Processes, ['Heavy Duty Truck'], default_dist=20)
    >>> distance = Distance(data)

    Step 3: Create Collection_processes dict with one single family sector which only has residual waste collection:

    >>> from swolfpy_processmodels import SF_Col
    >>> Collection_processes = {}
    >>> Collection_scheme_SF_COL={'RWC':{'Contribution':1,'separate_col':{'SSR':0,'DSR':0,'MSR':0,'MSRDO':0,'SSYW':0,'SSYWDO':0}},
    >>> 'SSO_DryRes':{'Contribution':0,'separate_col':{'SSR':0,'DSR':0,'MSR':0,'MSRDO':0,'SSYW':0,'SSYWDO':0}},
    >>> 'REC_WetRes':{'Contribution':0,'separate_col':{'SSR':0,'DSR':0,'MSR':0,'MSRDO':0,'SSYW':0,'SSYWDO':0}},
    >>> 'MRDO':{'Contribution':0,'separate_col':{'SSR':0,'DSR':0,'MSR':0,'MSRDO':0,'SSYW':0,'SSYWDO':0}}}
    >>> Collection_processes['SF_COl']={'input_type':[],'model': SF_Col('SF_COl',Collection_scheme_SF_COL,
    >>>                                 Treatment_processes=Treatment_processes,Distance=distance)}

    Step 4: Create project:

    >>> from swolfpy import Project
    >>> demo = Project('demo',common_data,Treatment_processes,distance,Collection_processes)
    >>> demo.init_project()
    >>> demo.write_project()
    >>> demo.group_exchanges()
    >>> demo.parameters.default_parameters_list()
        [{'name': 'frac_of_Bottom_Ash_from_WTE_to_LF', 'amount': 1.0},
         {'name': 'frac_of_Fly_Ash_from_WTE_to_LF', 'amount': 1.0},
         {'name': 'frac_of_RWC_from_SF_COl_to_LF', 'amount': 0.5},
         {'name': 'frac_of_RWC_from_SF_COl_to_WTE', 'amount': 0.5}]
    >>> demo.update_parameters(demo.parameters.default_parameters_list())
    """
    def __init__(self, project_name, CommonData, Treatment_processes, Distance,
                 Collection_processes=None, Technosphere_obj=None, signal=None):
        if Technosphere_obj:
            self.Technosphere = Technosphere_obj
            self.project_name = self.Technosphere.project_name
            if self.project_name != project_name:
                raise Warning('The project name should be same with the name selected for creating the technosphere')
        else:
            self.project_name = project_name
            self.Technosphere = Technosphere(self.project_name)

        self.CommonData = CommonData
        self.Treatment_processes = Treatment_processes
        self.Collection_processes = Collection_processes
        self.Distance = Distance
        if self.Collection_processes:
            for j in self.Collection_processes.keys():
                self.Treatment_processes[j] = self.Collection_processes[j]

        self.processes = [x for x in self.Treatment_processes.keys()]
        self.processTypes = {}
        for p in self.processes:
            self.processTypes[p] = self.Treatment_processes[p]['model'].Process_Type

        projects.set_current(self.project_name)

        self.waste_treatment = {}
        for i in self.CommonData.All_Waste_Pr_Index:
            self.waste_treatment[i] = self._find_destination(i)

        self.process_model = {}

        # Creating swolfpy parameter class
        self.parameters = Parameters(self.Treatment_processes, self.CommonData)

        self._progress = 0

    def _find_destination(self, product):
        """
        Find the processes that can treat the `product`. This function check the ``input_type`` in the ``Treatment_processes`` dictionary.

        :param product: Waste product e.g., RWC, Fly_Ash, Separated_Organics, Other_Residual
        :type product: str

        :return: A list of the discovered processes in the ``Treatment_processes`` dictionary that can treat the `product`
        :rtype: list

        """
        destination = []
        for P in self.Treatment_processes:
            if product in self.Treatment_processes[P]['input_type']:
                destination.append(P)
        return(destination)

    def init_project(self, signal=None):
        """
        Calls the Create_Technosphere_ method to initilize a project.\n
        This function create an empty database for each process as a placeholder, so swolfpy
        can browse these databases in the next step (writing project) and
        create exchanges between them.
        """
        if signal:
            self._progress += 5
            signal.emit(self._progress)

        self.Technosphere.Create_Technosphere()

        if signal:
            self._progress += 10
            signal.emit(self._progress)

        # Initializing the databases
        for DB_name in self.Treatment_processes:
            if self.Treatment_processes[DB_name]['model'].Process_Type in ['Treatment', 'Collection']:
                ProcessDB.init_DB(DB_name, self.CommonData.Index)
            elif self.Treatment_processes[DB_name]['model'].Process_Type == 'Reprocessing':
                ProcessDB.init_DB(DB_name, self.CommonData.Reprocessing_Index)
            elif self.Treatment_processes[DB_name]['model'].Process_Type == 'RDF':
                ProcessDB.init_DB(DB_name, ['RDF'])

        Database("waste").register()
        self.waste_BD = Database("waste")

        if signal:
            self._progress += 5
            signal.emit(self._progress)

    def write_project(self, signal=None):
        """ Call the import_database_ for all the process models.
        """
        self.parameters_dict = {}
        self.parameters_list = []
        self.act_include_param = {}
        for j in self.Treatment_processes:
            (P, G) = self._import_database(j)
            self.parameters_dict[j] = P
            self.act_include_param[j] = G
            self.parameters_list += P

        if signal:
            self._progress += 10
            signal.emit(self._progress)

    def _import_database(self, name):
        """
        .. _import_database:

        Instantiate the ProcessDB_ class for the process model and gets the LCI report from it; then translates
        the report for Brightway2 and populates the databases by Write_DB_ method.

        :return: Returns a tuple (parameters,act_in_group)
        :rtype: tuple
        """
        self.process_model[name] = ProcessDB(name, self.waste_treatment, self.CommonData, self.processTypes, self.Distance)
        self.Treatment_processes[name]['model'].calc()
        self.process_model[name].Report = self.Treatment_processes[name]['model'].report()

        if self.Treatment_processes[name]['model'].Process_Type in ['Treatment', 'Collection']:
            (P, G) = self.process_model[name].Write_DB(waste_flows=self.CommonData.Index,
                                                       parameters=self.parameters,
                                                       Process_Type=self.Treatment_processes[name]['model'].Process_Type)

        elif self.Treatment_processes[name]['model'].Process_Type == 'Reprocessing':
            (P, G) = self.process_model[name].Write_DB(waste_flows=self.CommonData.Reprocessing_Index,
                                                       parameters=self.parameters,
                                                       Process_Type=self.Treatment_processes[name]['model'].Process_Type)

        elif self.Treatment_processes[name]['model'].Process_Type == 'Transfer_Station':
            (P, G) = self.process_model[name].Write_DB(waste_flows=self.Treatment_processes[name]['model']._Extened_Index,
                                                       parameters=self.parameters,
                                                       Process_Type=self.Treatment_processes[name]['model'].Process_Type)
        elif self.Treatment_processes[name]['model'].Process_Type == 'RDF':
            (P, G) = self.process_model[name].Write_DB(waste_flows=['RDF'],
                                                       parameters=self.parameters,
                                                       Process_Type=self.Treatment_processes[name]['model'].Process_Type)
        return((P, G))

    def report_parameters(self):
        """
        Reports the `parameters` in dictionary format.

        :return: dictionary include the processes as key and parameters in each process as values.
        :rtype: dict

        """
        return(self.parameters_dict)

    def report_parameters_list(self):
        """
        Reports the `parameters` in list format.

        :return: List of `parameters` (waste fractions) in the project
        :rtype: list

        """
        return(self.parameters_list)

    def group_exchanges(self, signal=None):
        """
        Create a group for the `parameters` in each database and add the exchanges that include these `parameters`
        to this group. As a results, model know to update the values in those exchanges when the `parameter` is updated
        """
        for j in self.processes:
            print("""
                  Grouping the exchanges with parameters in Database {}
                  """.format(j))
            if len(self.act_include_param[j]) > 0:
                for r in self.act_include_param[j]:
                    parameters.add_exchanges_to_group(j, r)

            if signal:
                self._progress += 70 / len(self.processes)
                signal.emit(self._progress)

        if signal:
            signal.emit(100)

    def update_parameters(self, new_param_data, signal=None):
        """
        Updates the `parameters` and their related exchanges based on the `new_param_data`.

        :param new_param_data: List of `parameters` (waste fractions) in the project with new values
        :type new_param_data: list

        .. note:: `parameters` are waste fractions which show what fraction of waste from one source
                    go to different destinations, so sum of parameters from each source should be 1. (0<= `parameters` <=1)

        """

        progress = 0
        if signal:
            signal.emit(progress)

        for j in new_param_data:
            for k in self.parameters_list:
                if k['name'] == j['name']:
                    self.parameters.update_values(j['name'], j['amount'])

        if self.parameters.check_sum():
            for j in new_param_data:
                for k in self.parameters_list:
                    if k['name'] == j['name']:
                        k['amount'] = j['amount']
            parameters.new_project_parameters(new_param_data)
            for j in self.processes:
                if len(self.act_include_param[j]) > 0:
                    ActivityParameter.recalculate_exchanges(j)

                progress += 100 / len(self.processes)
                if signal:
                    signal.emit(progress)

        else:
            for j in new_param_data:
                for k in self.parameters_list:
                    if k['name'] == j['name']:
                        self.parameters.update_values(k['name'], k['amount'])

    def create_scenario(self, input_dict, scenario_name):
        """Creates a new scenario (activity).
        """
        input_dict = input_dict
        # Calculate Unit
        mass = 0
        for P in input_dict:
            for y in input_dict[P]:
                if input_dict[P][y] != 0:
                    unit_i = get_activity((P, y)).as_dict()['unit'].split(sep=' ')
                    if len(unit_i) > 1:
                        mass += float(unit_i[0]) * input_dict[P][y]
                    if unit_i[0] == 'Mg/year':
                        mass += 1 * input_dict[P][y]
        new_act = self.waste_BD.new_activity(code=scenario_name, name=scenario_name, type="process",
                                             unit='{} Mg/year'.format(np.round(mass, decimals=2)),
                                             **{'reference product': scenario_name})
        new_act.save()
        new_act.new_exchange(input=new_act, amount=1, type="production").save()
        for P in input_dict:
            for y in input_dict[P]:
                if input_dict[P][y] != 0:
                    new_act.new_exchange(input=(P, y), amount=input_dict[P][y], type="technosphere").save()

    @staticmethod
    def setup_LCA(name, functional_units, impact_methods):
        """
        Perform LCA by instantiating the ``bw2calc.multi_lca`` class from Brightway2.
        ``bw2calc.multi_lca`` is a wrapper class for performing LCA calculations with many
        functional units and LCIA methods.
        """
        if len(functional_units) > 0 and len(impact_methods) > 0:
            calculation_setups[name] = {'inv': functional_units, 'ia': impact_methods}
            MultiLca = MultiLCA(name)
            index = [str(x) for x in list(MultiLca.all.keys())]
            columns = [str(x) for x in impact_methods]
            results = pd.DataFrame(MultiLca.results,
                                   columns=columns,
                                   index=index)
            return(results)
        else:
            raise ValueError('Check the in inputs')

    @staticmethod
    def contribution_analysis(functional_unit, impact_method, limit, limit_type='number', target='emissions',
                              figsize=(6, 4), font_scale=1):
        """
        Perform LCA by instantiating the ``bw2calc.lca.LCA`` class from ``Brightway2`` and then
        perform contribution analysis by ``bw2analyzer.ContributionAnalysis`` class.
        Check the following functions in ``bw2analyzer`` for more info:

        * ``bw2analyzer.ContributionAnalysis.annotated_top_processes``
        * ``bw2analyzer.ContributionAnalysis.annotated_top_emissions``

        """
        lca = LCA(functional_unit, impact_method)
        lca.lci()
        lca.lcia()
        impacts = []
        amounts = []
        activities = []
        flow_unit = []
        compartments = []
        f = font_scale * 14

        if target == 'activities':
            data = ContributionAnalysis().annotated_top_processes(lca, limit=50, limit_type='number')
        else:
            data = ContributionAnalysis().annotated_top_emissions(lca, limit=50, limit_type='number')
        for impact, amount, act in data:
            impacts.append(impact)
            amounts.append(amount)
            flow_unit.append(act.as_dict()['unit'])
            if target == 'activities':
                activities.append(act.as_dict()['name'].replace('_', ' '))
            else:
                activities.append(act.as_dict()['name'])
                compartments.append(act.as_dict()['categories'])

        if target == 'activities':
            top_df = pd.DataFrame(columns=['Activity', 'Flow', 'Flow Unit', 'Contribution', 'Unit'])
            top_df['Activity'] = activities
        else:
            top_df = pd.DataFrame(columns=['Emission', 'Compartment', 'Flow', 'Flow Unit', 'Contribution', 'Unit'])
            top_df['Emission'] = activities
            top_df['Compartment'] = compartments

        top_df['Flow'] = amounts
        top_df['Flow Unit'] = flow_unit
        top_df['Contribution'] = impacts
        top_df['Unit'] = Method(lca.method).metadata['unit']

        if limit_type == 'number':
            DF = top_df.loc[0:limit, :]
        else:
            for i, j in enumerate(top_df['Contribution']):
                if abs(j) <= abs((limit * lca.score)):
                    break
                DF = top_df.loc[0:i, :]

        plot_DF = pd.DataFrame(data=[[x for x in DF['Contribution']]],
                               columns=DF.iloc[:, 0].values,
                               index=list(functional_unit.keys()))

        legend = ['Net']
        if target == 'emissions':
            for x, y in DF[['Emission', 'Compartment']].values:
                y = str(y).replace("'", '')
                legend.append('{}\n{}'.format(x, y))
        else:
            for x in DF['Activity'].values:
                if len(x) > 20:
                    x = x[0:15] + x[15:].replace(' ', '\n', 1)
                legend.append(x)

        fig, ax = plt.subplots(figsize=figsize)
        plot_DF.plot(kind='bar', stacked=True, ax=ax, alpha=0.9)
        ax.set_title('Contribution to {}'.format(str(lca.method).replace("'", '')), fontsize=f)
        ax.scatter(0, lca.score, s=50, marker='D', edgecolor='w', facecolor='k')
        ax.legend(legend, fontsize=f, bbox_to_anchor=(1, 0, .2, 1), loc=2)
        ax.tick_params(axis='both', which='major', labelsize=f, rotation='auto')
        ax.tick_params(axis='both', which='minor', labelsize=f, rotation='auto')
        ax.set_ylabel(Method(lca.method).metadata['unit'], fontsize=f)
        return(DF, (fig, ax))

    def save(self, filename):
        """
        Dumps the ``Project`` class to pickle file. User can load the pickle and use it later.

        :param filename:
        :type filename: str
        """
        import pickle
        pickle.dump(self, open(filename, "wb"))
