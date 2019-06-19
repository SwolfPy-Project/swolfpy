from db_handler import *

class WasteDB(object):
	def __init__(self,Data_bsae_name):
		if "Data_bsae_name" in databases:
			del databases["Data_bsae_name"]
            
    self.Waste_streams = ['Bottom_Ash','Fly_Ash','Separated_Organics','Other_Residual','RDF',
                          'Wastewater','OCC','Mixed_Paper','ONP','OFF','Fiber_Other','PET','HDPE_Unsorted','HDPE_P',
                          'HDPE_T','PVC','LDPE_Film','Polypropylene','Polystyrene','Plastic_Other','Mixed_Plastic',
                          'Al','Fe','Cu','Brown_glass','Clear_glass','Green_glass','Mixed_Glass'] 
            
    self.db_data ={}
        self.DB_name = Data_bsae_name
        for x in  AA:
            if x in ['Bottom_Ash','Fly_Ash','Separated_Organics','Other_Residual',
                     'RDF','Wastewater']:
                for y in BB:
                    self.db_data[(self.DB_name,x+'_'+y)] ={}    # add activity to database
                    self.db_data[(self.DB_name,x+'_'+y)]['name'] = x+'_'+y
                    self.db_data[(self.DB_name,x+'_'+y)]['unit'] = 'Mg'
                    self.db_data[(self.DB_name,x+'_'+y)]['exchanges'] =[]
            else:
                self.db_data[(self.DB_name,x)] ={}    # add activity to database
                self.db_data[(self.DB_name,x)]['name'] = x
                self.db_data[(self.DB_name,x)]['unit'] = 'Mg'
                self.db_data[(self.DB_name,x)]['exchanges'] =[]
            
            
   
            
		self.dbh = DatabaseHandler('Waste')
		self.activities = ['3_Bottom Ash',
 '4_Fly Ash',
 '5_Separated Organics',
 '6_Other Residual',
 '7_RDF',
 '8_Wastewater',
 '9_OCC',
 '10_Mixed Paper',
 '11_ONP',
 '12_OFF',
 '13_Other',
 '14_PET (#1)',
 '15_HDPE-Unsorted (#2)',
 '16_HDPE-P (#2A)',
 '17_HDPE-T (#2B)',
 '18_PVC (#3)',
 '19_LDPE/Film ( #4)',
 '20_Polypropylene (#5)',
 '21_Polystyrene (#6)',
 '22_Other (#7)',
 '23_Mixed Plastic',
 '24_Al',
 '25_Fe',
 '26_Cu',
 '27_Brown',
 '28_Clear',
 '29_Green',
 '30_Mixed Glass']

		for val in self.activities:
			self.dbh.add_activity(val,val,'Mg')
	
		self.exchanges = dict()

		for activity in self.activities:
			self.exchanges[activity] = Exchange()
	
	def get_activities(self, name):
		return self.dbh.get_all_activities(name)
	
	def write(self):
		self.dbh.write()