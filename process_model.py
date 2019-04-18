#required_inputs, allowable_inputs, allowable_outputs = list
#process_model_inputs = dict

from file_handler import *

class ProcessModel(object):

    def __init__ (self, name, required_inputs, allowable_inputs, allowable_waste_outputs, allowable_bio_techno_outputs, process_model_inputs, material_properties):
        self.name = name
        self.required_inputs = required_inputs
        self.allowable_inputs = allowable_inputs
        self.allowable_waste_outputs = allowable_waste_outputs
        self.allowable_bio_techno_outputs = allowable_bio_techno_outputs
        self.process_model_inputs = process_model_inputs
        self.material_properties = material_properties
        self.outputs = dict()
        self.outputs['Biosphere'] = list()
        self.outputs['Technosphere'] = list()
        self.outputs['Waste'] = list()
        self.outputs['Initial'] = list()
        self.outputs['Waste_technosphere'] = list()
        self.outputs['biosphere3'] = list()
        self.allowable_bio_techno_outputs['Technosphere'] = list()
        self.allowable_bio_techno_outputs['Biosphere'] = list()
        self.allowable_bio_techno_outputs['Waste'] = list()
#        allowable_waste_outputs = list()
        #self.check_process_model()
        
    def check_process_model (self):
        for value in self.required_inputs:
            if value not in self.process_model_inputs:
                raise Exception ('Required input {} not available in Process Model inputs' .format(value))
    
    
    def check_outputs(self, db):
        if db not in ['Biosphere', 'Technosphere', 'Waste']:
            raise Exception ('{} not a Biosphere, Technosphere, Waste output' .format(db))
    
    
    def create_output(self, flow, material, db, code, amount):
        #self.check_outputs(db)
        temp = list()
        temp.append(flow)
        temp.append(material)
        temp.append(db)
        temp.append(code)
        temp.append(amount)
        if flow == 'Initial':
            self.outputs[flow].append(temp)
        else:
            self.outputs[db].append(temp)
            
    
    def write_output(self, filename): 
        write = FileHandler()
        write.writeCSVList (filename,self.outputs['Initial'])
        write.appendCSVList (filename,self.outputs['Biosphere'])
        write.appendCSVList (filename,self.outputs['Technosphere'])
        write.appendCSVList (filename,self.outputs['Waste'])
        write.appendCSVList (filename,self.outputs['Waste_technosphere'])
        write.appendCSVList (filename,self.outputs['biosphere3'])

    def import_from_SWOLF(self, SWOLF_data):
        materials = set()
        for key,value in SWOLF_data['Technosphere'].items():
            for key2, value2 in value.items():
                if value2 != 0:
                    self.allowable_bio_techno_outputs['Technosphere'].append(key2[1])
                    self.create_output(SWOLF_data['process name'],key,key2[0],key2[1],value2)
                    materials.add(key)
                    
        for key,value in SWOLF_data['Biosphere'].items():
            for key2, value2 in value.items():
                if value2 != 0:
                    self.allowable_bio_techno_outputs['Biosphere'].append(key2[1])
                    self.create_output(SWOLF_data['process name'],key,key2[0],key2[1],value2)
                    materials.add(key)

        for key,value in SWOLF_data['Waste'].items():
            for key2, value2 in value.items():
                if value2 != 0:
                    self.allowable_bio_techno_outputs['Waste'].append(key2)
                    self.create_output(SWOLF_data['process name'],key,'Waste',key2,value2)
                    materials.add(key)        
                           
                    
    #    for x in materials:
    #        self.create_output('Initial',x,'Waste','Landfill',1/len(materials))
            
        
class Collection(ProcessModel):
    
    def __init__ (self, name, required_inputs, allowable_inputs, allowable_waste_outputs, allowable_bio_techno_outputs, process_model_inputs, material_properties):
            ProcessModel.__init__(self, name, required_inputs, allowable_inputs, allowable_waste_outputs, allowable_bio_techno_outputs, process_model_inputs, material_properties)
    

class Treatment(ProcessModel):

        def __init__ (self, name, required_inputs, allowable_inputs, allowable_waste_outputs, allowable_bio_techno_outputs, process_model_inputs, material_properties):
            ProcessModel.__init__(self, name, required_inputs, allowable_inputs, allowable_waste_outputs, allowable_bio_techno_outputs, process_model_inputs, material_properties)

            
