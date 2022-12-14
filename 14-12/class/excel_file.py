#create excel file class

import cv2
import os
import pandas as pd
import numpy as np



#inherit x and time list from eye tracking class
class ExcelFile():
    
    def __init__(self, x_list, time_list):
        #create x and time list       
    
        self.x_list = x_list
        self.time_list = time_list
        
    #create function that creates excel file
    def create_excel_file(self):
    #create dictionary
        #save both x and y coordinates in one csv file
        x_dataFrame=np.array(self.x_list)
        time_dataFranme=np.array(self.time_list)        
        
        #create dataframe
        df = pd.DataFrame({'x': time_dataFranme,  'y': x_dataFrame})        
        
        #check if save file already exists
        excel_file_counter=1
        excel_file_name = '13-12/list'
        while os.path.exists(excel_file_name+'.csv'):
            excel_file_name = '13-12/list'+str(excel_file_counter)
            excel_file_counter+=1
            
        #add df1 and df2 to csv file with two columns
        df.to_csv(excel_file_name+'.csv', index=False)
    
