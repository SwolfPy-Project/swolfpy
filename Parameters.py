from project_class import *
from stats_arrays import *
import copy

class Parameters():
    def __init__ (self):
        self.param_uncertainty_dict = dict()
        self.params_dict = dict()
        self.uncertainty_base = list()
        self.uncertainty_vals = list()
        self.param_uncertainty_dict_MC = dict()
    
    def add_parameter (self, waste_stream, process_model_from, process_model_to):
        long_name = 'frac_of_' + waste_stream + '_from_' + process_model_from + '_to_' + process_model_to
        key = waste_stream + process_model_from
        if key not in self.param_uncertainty_dict.keys():
            self.param_uncertainty_dict[key] = list()
            self.param_uncertainty_dict[key].append([process_model_to, 0.0, long_name])
        else:
            self.param_uncertainty_dict[key].append([process_model_to, 0.0, long_name])
            
    def update_values (self, long_name, val, MC = None):
        if MC:
            for items in self.param_uncertainty_dict_MC.values():
                for list_item in items:
                    if list_item[2] == long_name:
                        list_item[1] = val
        
        else:
            for items in self.param_uncertainty_dict.values():
                for list_item in items:
                    if list_item[2] == long_name:
                        list_item[1] = val

    
    def normalize(self):
        sum = 0 
        for item in self.param_uncertainty_dict_MC.values():
            for list_item in item:
                sum += list_item[1]
                
            for list_item in item:
                if sum != 0:
                    list_item[1] = list_item[1]/sum
                else:
                    list_item[1] = 1 /len(item)
            sum = 0
    
    
    def check_sum(self):
        sum = 0
        flag = 1
        for item in self.param_uncertainty_dict.values():
            for list_item in item:
                sum += list_item[1]
            if sum != 1:
                print("Sum of the parameters is not 1")
                for i in item:
                    print ("%s : %f" % (i[2],i[1]))
                sum = 0
                flag = 0
                break
            sum = 0
        return flag
            
    def set_params_uncertainty_dict(self, uncertainty_dict):
        self.param_uncertainty_dict = uncertainty_dict

        
    def set_params_dict(self, params_dict):
        self.params_dict = params_dict
        
    def get_param_MC_val(self, long_name):
        for item in self.param_uncertainty_dict_MC.values():
            for list_item in item:
                if list_item[2] == long_name:
                    return list_item[1]
        
    def add_uncertainty(self, long_name, **kwargs):

        base_dict = dict()
        base_dict['loc'] = kwargs.get('loc', None)
        base_dict['scale'] = kwargs.get('scale', None)
        base_dict['shape'] = kwargs.get('shape', None)
        base_dict['minimum'] = kwargs.get('minimum', None)
        base_dict['maximum'] = kwargs.get('maximum', None)
        base_dict['negative'] = kwargs.get('negative', None)
        base_dict['uncertainty_type'] = kwargs.get('uncertainty_type', None)
        
        if long_name not in self.uncertainty_vals:
            self.uncertainty_vals.append(long_name)
            self.uncertainty_base.append(base_dict)
            
        else:
            self.uncertainty_base[self.uncertainty_vals.index(long_name)] = base_dict
            
    def setup_MC(self,seed=None):
        self.vars = UncertaintyBase.from_dicts(*self.uncertainty_base)
        self.rand = MCRandomNumberGenerator(self.vars,seed=seed)
        self.param_uncertainty_dict_MC = copy.deepcopy(self.param_uncertainty_dict)
            
    def MC_calc(self):
        vals = self.rand.next()
        i = 0
        sum = 0
        matrix = dict()
        for item in vals:
            self.update_values(self.uncertainty_vals[i],item,1)
            i+=1
        
        i=0
        param_keys = list()
        param_vals = list()
        self.normalize()
        for key in self.params_dict.keys():
            param_keys.append(key)
            param_vals.append(self.get_param_MC_val(key))
            for item in self.params_dict[key]:
                #if self.get_param_MC_val(key) != 0:
                    matrix[item] = self.get_param_MC_val(key)
        #for item in vals:
        #    for item2 in self.params_dict[self.uncertainty_vals[i]]:
        #        matrix[item2] = self.get_param_MC_val(self.uncertainty_vals[i])            
        #    i+=1
        return (matrix,tuple(zip(param_keys,param_vals)))
            
            