import os.path
import pandas as pd


class BoroughSplitter():


    def split_nypd_by_borough(self,all_data: pd.DataFrame):
    
        all_data['BOROUGH']=all_data['BOROUGH'].fillna('NOTREPORTED')   
        boroughs = all_data["BOROUGH"].unique()

        by_borough_storage_path ='.\data_store\\by_borough'

        for borough_name in boroughs:
            df_group = all_data[(all_data["BOROUGH"]==borough_name)]
            file_path_to_save = os.path.join(by_borough_storage_path,f'{borough_name}.csv')
            df_group.to_csv(file_path_to_save)
