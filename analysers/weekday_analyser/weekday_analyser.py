import os.path
import pandas as pd

from folders_handling.folders import FoldersLookup



class WeekDayAnalyser():

    __folders__ = FoldersLookup()

    def get_per_weekday_accident_count(self,filePath: str, outoutFileName : str):
        raw_data = pd.read_csv(filePath)
        raw_data["ACCIDENT DATE"] = pd.to_datetime(raw_data["ACCIDENT DATE"])
        raw_data['weekday'] = raw_data["ACCIDENT DATE"].dt.dayofweek
        grouped_by_day_counts = raw_data.groupby('weekday')['COLLISION_ID'].count()
        grouped_by_day_counts = grouped_by_day_counts.to_frame()
        grouped_by_day_counts=grouped_by_day_counts.sort_values(['COLLISION_ID'], ascending=False)
        os.makedirs(self.__folders__.findings_folder, exist_ok=True)
        storage_path = os.path.join(self.__folders__.findings_folder, outoutFileName)
        grouped_by_day_counts.to_csv(storage_path)


