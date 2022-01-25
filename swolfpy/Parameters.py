from stats_arrays import UncertaintyBase, MCRandomNumberGenerator
import copy
import graphviz


def approx_eq(x, y):
    tol = 1.0E-6
    return abs(x - y) <= max(abs(x), abs(y)) * tol


class Parameters():
    def __init__(self, processes, CommonData):
        self.param_uncertainty_dict = dict()
        self.static_param_dict = dict()
        self.params_dict = dict()

        self.MC_param_name = list()  # name of parameters that include uncertainty
        self.MC_param_base = list()  # uncertainty base for parameters that have uncertainty
        self.MC_param_uncertainty_dict = dict()

        self.processes = processes
        self.nodes = list(self.processes.keys())

        # Color & shape for plotting the SWM Network
        self.edge_color = {'RWC': 'black', 'SSR': 'blue', 'DSR': 'blue',
                           'MSR': 'blue',
                           'LV': 'green4', 'SSYW': 'green4', 'SSO': 'green4',
                           'SSO_AnF': 'green4', 'SSO_HC': 'green4',
                           'ORG': 'green4', 'DryRes': 'black',
                           'REC': 'blue', 'WetRes': 'black',
                           'MRDO': 'black', 'SSYWDO': 'green4', 'MSRDO': 'blue',
                           'Bottom_Ash': 'gray', 'Fly_Ash': 'gray',
                           'Unreacted_Ash': 'gray',
                           'Separated_Organics': 'green4',
                           'Separated_Recyclables': 'blue',
                           'Other_Residual': 'black', 'RDF': 'red'}
        for i in CommonData.Reprocessing_Index:
            self.edge_color[i] = 'blue'
        self.node_shape = {}
        self.node_color = {}
        for p in self.processes:
            if self.processes[p]['model'].Process_Type != 'Collection':
                self.node_shape[p] = 'rectangle'
                self.node_color[p] = 'cyan3'
            else:
                self.node_shape[p] = 'oval'
                self.node_color[p] = 'azure'

    def add_parameter(self, product, process_model_from, process_model_to, value, dynamic_param=True):
        """
        Define new parameter

        :param product: Name of stream
        :type product: str
        :param process_model_from: Name of the process which is source of stream
        :type process_model_from: str
        :param process_model_to: Name of the process which is destination of stream
        :type process_model_to: str
        :param value: Value for the parameter
        :type value: float

        """
        param_name = 'frac_of_' + product + '_from_' + process_model_from + '_to_' + process_model_to
        key = product + process_model_from
        if dynamic_param:
            if key not in self.param_uncertainty_dict.keys():
                self.param_uncertainty_dict[key] = list()
                self.param_uncertainty_dict[key].append([process_model_to, value, param_name, (process_model_from, process_model_to, product)])
            else:
                self.param_uncertainty_dict[key].append([process_model_to, value, param_name, (process_model_from, process_model_to, product)])
        else:
            if key not in self.static_param_dict.keys():
                self.static_param_dict[key] = list()
                self.static_param_dict[key].append([process_model_to, value, param_name, (process_model_from, process_model_to, product)])
            else:
                self.static_param_dict[key].append([process_model_to, value, param_name, (process_model_from, process_model_to, product)])

    def SWM_network(self, view=True, show_vals=True, all_flow=True,
                    filename='SWM_network'):
        """
        To render the generated DOT source code, you also need to install `Graphviz <https://www.graphviz.org/download>`_.

        ..note:: Make sure that the directory containing the dot executable is on your systems path.

        """
        # Initialize SWM network
        self.network = graphviz.Digraph(name=filename, filename=filename + '.gv', format='png', engine='dot')
        self.network.graph_attr['rankdir'] = 'LR'
        for x in self.nodes:
            self.network.node(x, shape=self.node_shape[x], fillcolor=self.node_color[x], style='filled', width='1.2')

        for param_dict in [self.param_uncertainty_dict.values(), self.static_param_dict.values()]:
            for y in param_dict:
                for x in y:
                    if show_vals:
                        if all_flow:
                            self.add_edge(x[3][0], x[3][1], x[3][2], x[1])
                        elif not all_flow and x[1] > 0:
                            self.add_edge(x[3][0], x[3][1], x[3][2], x[1])
                        else:
                            pass
                    else:
                        self.add_edge(x[3][0], x[3][1], x[3][2])
        try:
            self.network.render(filename + '.gv', view=view)
        except Exception:
            print("""
            To render the generated DOT source code, you also need to install Graphviz (`Graphviz <https://www.graphviz.org/download>`_).\n
            Make sure that the directory containing the dot executable is on your systems’ path.
            """)

    def add_edge(self, head, tail, name, value=None):
        if isinstance(value, (int, float)):
            self.network.edge(head, tail, label=name + ' ({})'.format(value), color=self.edge_color[name])
        else:
            self.network.edge(head, tail, label=name, color=self.edge_color[name])

    def default_parameters_list(self):
        default_parameters_list = []
        for items in self.param_uncertainty_dict.values():
            for list_item in items:
                default_parameters_list.append({'name': list_item[2], 'amount': 1 / len(items)})
        return(default_parameters_list)

    def parameters_list(self):
        parameters_list = []
        for items in self.param_uncertainty_dict.values():
            for list_item in items:
                parameters_list.append({'name': list_item[2], 'amount': list_item[1]})
        return(parameters_list)

    def update_values(self, param_name, val, simulation=False):
        if simulation:
            param_uncertainty_dict = self.MC_param_uncertainty_dict
        else:
            param_uncertainty_dict = self.param_uncertainty_dict

        for items in param_uncertainty_dict.values():
            for list_item in items:
                if list_item[2] == param_name:
                    list_item[1] = val

    def check_sum(self):
        """
        Check that sum of the waste fractions (parameters) for each stream from one source to all available destinations is 1.
        """
        sum_ = 0
        flag = 1
        for item in self.param_uncertainty_dict.values():
            for list_item in item:
                sum_ += list_item[1]
                if list_item[1] < 0 or list_item[1] > 1:
                    raise ValueError("Parameters should be in range(0,1), check: {}".format(list_item[2]))
            if not approx_eq(sum_, 1):
                msg = "Sum of the parameters in group is not 1: \n"
                for i in item:
                    print("{}: {}".format(i[2], i[1]))
                    msg += "{}: {}\n".format(i[2], i[1])
                raise ValueError(msg)
                sum_ = 0
                flag = 0
                break
            sum_ = 0
        return flag

    def add_uncertainty(self, param_name, **kwargs):
        """
        add uncertainty to parameter.

        :param param_name: Name of the parameter (wastefraction) that has uncertainty
        :type param_name: str
        """
        base_dict = dict()
        base_dict['loc'] = kwargs.get('loc', None)
        base_dict['scale'] = kwargs.get('scale', None)
        base_dict['shape'] = kwargs.get('shape', None)
        base_dict['minimum'] = kwargs.get('minimum', None)
        base_dict['maximum'] = kwargs.get('maximum', None)
        base_dict['negative'] = kwargs.get('negative', None)
        base_dict['uncertainty_type'] = kwargs.get('uncertainty_type', None)

        if param_name not in self.MC_param_name:
            self.MC_param_name.append(param_name)
            self.MC_param_base.append(base_dict)
        else:
            self.MC_param_base[self.MC_param_name.index(param_name)] = base_dict

    def setup_MC(self, seed=None):
        """
        Import uncertainty to stats_arrays package.
        """
        self.vars = UncertaintyBase.from_dicts(*self.MC_param_base)
        self.rand = MCRandomNumberGenerator(self.vars, seed=seed)
        self.MC_param_uncertainty_dict = copy.deepcopy(self.param_uncertainty_dict)

    def MC_calc(self):
        """
        Generates new values for uncertain parameters
        """
        new_vals = self.rand.next()
        for i in range(len(new_vals)):
            self.update_values(self.MC_param_name[i], new_vals[i], simulation=True)

        # Normalizing the generated random numbers
        self.normalize()

        param_exchanges_dict = dict()
        param_keys = list()
        param_vals = list()
        for key in self.params_dict.keys():
            param_keys.append(key)
            param_vals.append(self.MC_get_param_val(key))
            for item in self.params_dict[key]:
                param_exchanges_dict[item] = self.MC_get_param_val(key)
        return(param_exchanges_dict, tuple(zip(param_keys, param_vals)))

    def normalize(self):
        """
        Normalize the parameters after updating the valuse by monte carlo.
        """
        for item in self.MC_param_uncertainty_dict.values():
            sum_ = 0
            for list_item in item:
                if list_item[1] < 0:
                    raise ValueError("Parameters should be positive, check the uncertainty base for param: {}".format(list_item[2]))
                sum_ += list_item[1]

            for list_item in item:
                if sum_ != 0:
                    list_item[1] = list_item[1] / sum_
                else:
                    list_item[1] = 1 / len(item)

    def MC_get_param_val(self, param_name):
        """
        Report the uncertain value created for parameter

        :param param_name: Name of the parameter (wastefraction) that has uncertainty
        :type param_name: str
        :return: Value fo the parameter
        :rtype: float
        """
        for item in self.MC_param_uncertainty_dict.values():
            for list_item in item:
                if list_item[2] == param_name:
                    return list_item[1]

    def Param_exchanges(self, new_vals):
        """
        Returns the parameters exchanges with the new values
        """
        param_exchanges_dict = dict()
        self.MC_param_uncertainty_dict = copy.deepcopy(self.param_uncertainty_dict)
        param_list = list(self.params_dict.keys())

        # update parameter
        for i in range(len(new_vals)):
            self.update_values(param_list[i], new_vals[i], simulation=True)
        # update parameters exchanges dict
        for key in param_list:
            for item in self.params_dict[key]:
                param_exchanges_dict[item] = self.MC_get_param_val(key)
        return(param_exchanges_dict)
