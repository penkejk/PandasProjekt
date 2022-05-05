import os.path
import pandas as pd
from .injury_type import InjuryType
from  folders_handling.folders import FoldersLookup

class CasualityAnalyser():

    __folders__ = FoldersLookup()

    def store_casuality_info_by_vehicle_type(self,file_path: str, output_file_name : str, injury :InjuryType ):
        raw_data = pd.read_csv(file_path)
        
        field_substring = 'KILLED'
        file_name = self.__folders__.findings_by_vehicle_type_kill
        if injury == InjuryType.Injured:
            field_substring = 'INJURED'
            file_name = self.__folders__.findings_by_vehicle_type_injured
        
        raw_data[f'{field_substring} PEOPLE'] = raw_data[f'NUMBER OF PERSONS {field_substring}'] + raw_data[f'NUMBER OF PEDESTRIANS {field_substring}'] + raw_data[f'NUMBER OF CYCLIST {field_substring}'] + raw_data[f'NUMBER OF MOTORIST {field_substring}']
        
        raw_data_only_killed = raw_data[raw_data[f'{field_substring} PEOPLE'] > 0]
        mean_of_killed = raw_data_only_killed[f'{field_substring} PEOPLE'].mean()
        raw_data_only_killed_mean_and_above = raw_data_only_killed[(raw_data_only_killed[f'{field_substring} PEOPLE']>= mean_of_killed)]
        mean_and_above_by_type=  raw_data_only_killed_mean_and_above.groupby('VEHICLE TYPE CODE 1')[f'{field_substring} PEOPLE'].sum()
        mean_and_above_by_type = mean_and_above_by_type.to_frame()
        mean_and_above_by_type=mean_and_above_by_type.sort_values([f'{field_substring} PEOPLE'], ascending=False)
        mean_and_above_by_type['borough'] = file_path.split('\\')[-1].replace('.csv','')
        storage_path = os.path.join(self.__folders__.findings_folder, file_name)
        output_file_path = os.path.join(storage_path, output_file_name)
        os.makedirs(storage_path, exist_ok=True)
        mean_and_above_by_type.to_csv(output_file_path)