from .project_class import *
from stats_arrays import *
import copy
import math


def approx_eq(x, y):
    tol = 1.0E-6
    return abs(x - y) <= max(abs(x), abs(y)) * tol

class Parameters():
    def __init__ (self):
        self.param_uncertainty_dict = dict() 
        self.params_dict = dict()
        
        self.MC_param_name = list() #name of parameters that include uncertainty
        self.MC_param_base = list() #uncertainty base for parameters that have uncertainty
        self.MC_param_uncertainty_dict = dict()

    
    def add_parameter (self, product, process_model_from, process_model_to,value):
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
        if key not in self.param_uncertainty_dict.keys():
            self.param_uncertainty_dict[key] = list()
            self.param_uncertainty_dict[key].append([process_model_to, value, param_name])
        else:
            self.param_uncertainty_dict[key].append([process_model_to, value, param_name])

            
    def default_parameters_list(self):
        default_parameters_list=[]
        for items in self.param_uncertainty_dict.values():
            for list_item in items:
                default_parameters_list.append({'name':list_item[2] ,'amount':1/len(items)})
        return(default_parameters_list)
 
    def parameters_list(self):
        parameters_list=[]
        for items in self.param_uncertainty_dict.values():
            for list_item in items:
                parameters_list.append({'name':list_item[2] ,'amount':list_item[1]})
        return(parameters_list)    
    
    
    def update_values (self, param_name, val, simulation = False):
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
        sum = 0
        flag = 1
        for item in self.param_uncertainty_dict.values():
            for list_item in item:
                sum += list_item[1]
                if list_item[1] < 0 or list_item[1]>1:
                    raise ValueError("Parameters should be in range(0,1), check: {}".format(list_item[2]))
            if not approx_eq(sum, 1):
                for i in item:
                    print ("{} : {}".format(i[2],i[1]))
                raise ValueError("Sum of the parameters is not 1")
                sum = 0
                flag = 0
                break
            sum = 0
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
            
    def setup_MC(self,seed=None):
        """
        Import uncertainty to stats_arrays package.
        """
        self.vars = UncertaintyBase.from_dicts(*self.MC_param_base)
        self.rand = MCRandomNumberGenerator(self.vars,seed=seed)
        self.MC_param_uncertainty_dict = copy.deepcopy(self.param_uncertainty_dict)
            
    def MC_calc(self):
        """
        Generates new values for uncertain parameters
        """
        new_vals = self.rand.next()
        for i in range(len(new_vals)):
            self.update_values(self.MC_param_name[i],new_vals[i],simulation=True)
  
        #Normalizing the generated random numbers
        self.normalize()
      
        param_exchanges_dict = dict()
        param_keys = list()
        param_vals = list()
        for key in self.params_dict.keys():
            param_keys.append(key)
            param_vals.append(self.MC_get_param_val(key))
            for item in self.params_dict[key]:
                param_exchanges_dict[item] = self.MC_get_param_val(key)
        return (param_exchanges_dict,tuple(zip(param_keys,param_vals)))

    def normalize(self):
        """
        Normalize the parameters after updating the valuse by monte carlo.
        """
         
        for item in self.MC_param_uncertainty_dict.values():
            sum = 0
            for list_item in item:
                if list_item[1] < 0:
                    raise ValueError("Parameters should be positive, check the uncertainty base for param: {}".format(list_item[2]))
                sum += list_item[1]
                
            for list_item in item:
                if sum != 0:
                    list_item[1] = list_item[1]/sum
                else:
                    list_item[1] = 1 /len(item)
        
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
        
        #update parameter
        for i in range(len(new_vals)):
            self.update_values(param_list[i],new_vals[i],simulation=True)
        #update parameters exchanges dict
        for key in param_list:
            for item in self.params_dict[key]:
                param_exchanges_dict[item] = self.MC_get_param_val(key)
        return (param_exchanges_dict)
        
        