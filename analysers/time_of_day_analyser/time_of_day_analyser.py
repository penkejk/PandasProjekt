import os.path
import pandas as pd
import numpy as np

from folders_handling.folders import FoldersLookup



class TimeOfDayAnalyser():

    __folders__ = FoldersLookup()


    def __extract_hour__(self,input:str) -> str:
        return input.split(':')[0]

    def store_per_time_of_day_count(self,file_path: str, output_file_name : str):
        raw_data = pd.read_csv(file_path)
        raw_data['HOUR'] = raw_data.apply(lambda x: self.__extract_hour__(x['ACCIDENT TIME']), axis=1).astype(int)
        raw_data['DAY TIME'] = 'N/A'
        

        raw_data.loc[raw_data['HOUR'] <= 4,  'DAY TIME'] = 'NIGHT (22-4)'
        raw_data.loc[raw_data['HOUR'].between(4,7),  'DAY TIME'] = 'EARLY MORNING (4,7)'
        raw_data.loc[raw_data['HOUR'].between(7,10),  'DAY TIME'] = 'MORNING COMMUTE (7,10)'
        raw_data.loc[raw_data['HOUR'].between(10,16),  'DAY TIME'] = 'WORK TIME (10,16)'
        raw_data.loc[raw_data['HOUR'].between(16,19),  'DAY TIME'] = 'EVENING COMMUTE (16,19)'
        raw_data.loc[raw_data['HOUR'].between(19,22),  'DAY TIME'] = 'EVENING (19,22)'
        raw_data.loc[raw_data['HOUR'] > 22,  'DAY TIME'] = 'NIGHT (22-4)'
        grouped_by_day_time = raw_data.groupby('DAY TIME')['COLLISION_ID'].count()
        grouped_by_day_time = grouped_by_day_time.to_frame()
        grouped_by_day_time['borough'] = file_path.split('\\')[-1].replace('.csv','')
        grouped_by_day_time=grouped_by_day_time.sort_values(['COLLISION_ID'], ascending=False)
        storage_path = os.path.join(self.__folders__.findings_folder, self.__folders__.findings_by_time_of_day)
        output_file_path = os.path.join(storage_path, output_file_name)
        os.makedirs(storage_path, exist_ok=True)     
        grouped_by_day_time.to_csv(output_file_path)



