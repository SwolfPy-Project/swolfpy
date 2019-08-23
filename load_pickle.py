from project_class import *
from building_matrices import *
from WTE import *
from Composting import *
import pickle

proj = pickle.load(open("project.p","rb"))

project = "demo_6"
projects.set_current(project)
db = Database("waste")
functional_unit = {db.get("scenario3") : 1}
method = ('IPCC 2007', 'climate change', 'GWP 100a')


process_models = list()
process_model_names = list()

process_models.append(WTE())
process_models.append(WTE())
process_models.append(WTE())
process_models.append(WTE())
process_models.append(Comp())
process_models.append(Comp())
process_models.append(Comp())
process_models.append(Comp())


process_model_names.append('WTE')
process_model_names.append('WTE1')
process_model_names.append('WTE2')
process_model_names.append('WTE3')
process_model_names.append('COMP')
process_model_names.append('COMP1')
process_model_names.append('COMP2')
process_model_names.append('COMP3')


proj.unified_params.add_uncertainty('frac_of_Other_Residual_from_COMP_to_LF', loc = 0.2, scale = 0.1, uncertainty_type = 3)
proj.unified_params.add_uncertainty('frac_of_Other_Residual_from_COMP_to_WTE', loc = 0.2, scale = 0.1, uncertainty_type = 3)
proj.unified_params.add_uncertainty('frac_of_Other_Residual_from_COMP_to_WTE1', loc = 0.2, scale = 0.1, uncertainty_type = 3)
proj.unified_params.add_uncertainty('frac_of_Other_Residual_from_COMP_to_WTE2', loc = 0.2, scale = 0.1, uncertainty_type = 3)
proj.unified_params.add_uncertainty('frac_of_Other_Residual_from_COMP_to_WTE3', loc = 0.2, scale = 0.1, uncertainty_type = 3)

proj.unified_params.add_uncertainty('frac_of_Other_Residual_from_COMP1_to_LF', loc = 0.2, scale = 0.1, uncertainty_type = 3)
proj.unified_params.add_uncertainty('frac_of_Other_Residual_from_COMP1_to_WTE', loc = 0.2, scale = 0.1, uncertainty_type = 3)
proj.unified_params.add_uncertainty('frac_of_Other_Residual_from_COMP1_to_WTE1', loc = 0.2, scale = 0.1, uncertainty_type = 3)
proj.unified_params.add_uncertainty('frac_of_Other_Residual_from_COMP1_to_WTE2', loc = 0.2, scale = 0.1, uncertainty_type = 3)
proj.unified_params.add_uncertainty('frac_of_Other_Residual_from_COMP1_to_WTE3', loc = 0.2, scale = 0.1, uncertainty_type = 3)

proj.unified_params.add_uncertainty('frac_of_Other_Residual_from_COMP2_to_LF', loc = 0.2, scale = 0.1, uncertainty_type = 3)
proj.unified_params.add_uncertainty('frac_of_Other_Residual_from_COMP2_to_WTE', loc = 0.2, scale = 0.1, uncertainty_type = 3)
proj.unified_params.add_uncertainty('frac_of_Other_Residual_from_COMP2_to_WTE1', loc = 0.2, scale = 0.1, uncertainty_type = 3)
proj.unified_params.add_uncertainty('frac_of_Other_Residual_from_COMP2_to_WTE2', loc = 0.2, scale = 0.1, uncertainty_type = 3)
proj.unified_params.add_uncertainty('frac_of_Other_Residual_from_COMP2_to_WTE3', loc = 0.2, scale = 0.1, uncertainty_type = 3)


proj.unified_params.add_uncertainty('frac_of_Other_Residual_from_COMP3_to_LF', loc = 0.2, scale = 0.1, uncertainty_type = 3)
proj.unified_params.add_uncertainty('frac_of_Other_Residual_from_COMP3_to_WTE', loc = 0.2, scale = 0.1, uncertainty_type = 3)
proj.unified_params.add_uncertainty('frac_of_Other_Residual_from_COMP3_to_WTE1', loc = 0.2, scale = 0.1, uncertainty_type = 3)
proj.unified_params.add_uncertainty('frac_of_Other_Residual_from_COMP3_to_WTE2', loc = 0.2, scale = 0.1, uncertainty_type = 3)
proj.unified_params.add_uncertainty('frac_of_Other_Residual_from_COMP3_to_WTE3', loc = 0.2, scale = 0.1, uncertainty_type = 3)



a = ParallelData(functional_unit, method, project, parameters=proj.unified_params) 
a.run(8,1000)
from matplotlib.pylab import *
hist(a.results, density=True, histtype="step")
xlabel('(IPCC 2007, climate change, GWP 100a)')
ylabel("Probability")
    