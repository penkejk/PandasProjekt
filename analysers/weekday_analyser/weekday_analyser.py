import os.path
import pandas as pd

from folders_handling.folders import FoldersLookup



class WeekDayAnalyser():

    __folders__ = FoldersLookup()

    def store_per_weekday_accident_count(self,file_path: str, output_file_name : str):
        raw_data = pd.read_csv(file_path)
        raw_data["ACCIDENT DATE"] = pd.to_datetime(raw_data["ACCIDENT DATE"])
        raw_data['weekday'] = raw_data["ACCIDENT DATE"].dt.dayofweek
        grouped_by_day_counts = raw_data.groupby('weekday')['COLLISION_ID'].count()
        grouped_by_day_counts = grouped_by_day_counts.to_frame()
        grouped_by_day_counts['borough'] = file_path.split('\\')[-1].replace('.csv','')
        grouped_by_day_counts=grouped_by_day_counts.sort_values(['COLLISION_ID'], ascending=False)
        storage_path = os.path.join(self.__folders__.findings_folder, self.__folders__.findings_by_weekday)
        output_file_path = os.path.join(storage_path, output_file_name)
        os.makedirs(storage_path, exist_ok=True)
        grouped_by_day_counts.to_csv(output_file_path)


