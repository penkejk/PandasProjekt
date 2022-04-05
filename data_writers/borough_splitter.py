import os.path
import os
import pandas as pd
from folders_handling.folders import FoldersLookup

class BoroughSplitter():

    __folders_data__ = FoldersLookup()

    def split_nypd_by_borough(self,all_data: pd.DataFrame):
    
        all_data['BOROUGH']=all_data['BOROUGH'].fillna('NOTREPORTED')   
        boroughs = all_data["BOROUGH"].unique()

        by_borough_storage_path = self.__folders_data__.by_borough
        os.makedirs(by_borough_storage_path, exist_ok=True)
        for borough_name in boroughs:
            df_group = all_data[(all_data["BOROUGH"]==borough_name)]
            file_path_to_save = os.path.join(by_borough_storage_path,f'{borough_name}.csv')
            df_group.to_csv(file_path_to_save)
