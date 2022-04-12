import os.path
import pandas as pd
from .injury_type import InjuryType
from  folders_handling.folders import FoldersLookup

class CasualityAnalyser():



    __folders__ = FoldersLookup()

    def store_casuality_info_by_vehicle_type(self,filePath: str, outputFileName : str, injury :InjuryType ):
        raw_data = pd.read_csv(filePath)
        
        field_substring = 'KILLED'
        if injury == InjuryType.Injured:
            field_substring = 'INJURED'
        
        raw_data[f'{field_substring} PEOPLE'] = raw_data[f'NUMBER OF PERSONS {field_substring}'] + raw_data[f'NUMBER OF PEDESTRIANS {field_substring}'] + raw_data[f'NUMBER OF CYCLIST {field_substring}'] + raw_data[f'NUMBER OF MOTORIST {field_substring}']
        
        raw_data_only_killed = raw_data[raw_data[f'{field_substring} PEOPLE'] > 0]
        mean_of_killed = raw_data_only_killed[f'{field_substring} PEOPLE'].mean()
        raw_data_only_killed_mean_and_above = raw_data_only_killed[(raw_data_only_killed[f'{field_substring} PEOPLE']>= mean_of_killed)]
        mean_and_above_by_type=  raw_data_only_killed_mean_and_above.groupby('VEHICLE TYPE CODE 1')[f'{field_substring} PEOPLE'].sum()
        mean_and_above_by_type = mean_and_above_by_type.to_frame()
        mean_and_above_by_type=mean_and_above_by_type.sort_values([f'{field_substring} PEOPLE'], ascending=False)
        mean_and_above_by_type['borough'] = filePath.split('\\')[-1].replace('.csv','')
        storage_path = os.path.join(self.__folders__.findings_folder, self.__folders__.findings_by_vehicle_type)
        output_file_path = os.path.join(storage_path, outputFileName)
        os.makedirs(storage_path, exist_ok=True)
        mean_and_above_by_type.to_csv(output_file_path)