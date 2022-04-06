import os.path
import pandas as pd

from  folders_handling.folders import FoldersLookup

class KilledAnalyser():

    __folders__ = FoldersLookup()

    def store_killed_info_by_vehicle_type(self,filePath: str, outputFileName : str):
        raw_data = pd.read_csv(filePath)

        raw_data['KILLED PEOPLE'] = raw_data['NUMBER OF PERSONS KILLED'] + raw_data['NUMBER OF PEDESTRIANS KILLED'] + raw_data['NUMBER OF CYCLIST KILLED'] + raw_data['NUMBER OF MOTORIST KILLED']
        
        raw_data_only_killed = raw_data[raw_data['KILLED PEOPLE'] > 0]
        mean_of_killed = raw_data_only_killed['KILLED PEOPLE'].mean()
        raw_data_only_killed_mean_and_above = raw_data_only_killed[(raw_data_only_killed['KILLED PEOPLE']>= mean_of_killed)]
        mean_and_above_by_type=  raw_data_only_killed_mean_and_above.groupby(['VEHICLE TYPE CODE 1'])['KILLED PEOPLE'].sum()

        mean_and_above_by_type['borough'] = filePath.split('\\')[-1].replace('.csv','')
        storage_path = os.path.join(self.__folders__.findings_folder, self.__folders__.findings_by_vehicle_type)
        output_file_path = os.path.join(storage_path, outputFileName)
        os.makedirs(storage_path, exist_ok=True)
        mean_and_above_by_type.to_csv(output_file_path)