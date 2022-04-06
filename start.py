import os
import pandas as pd
from analysers.weekday_analyser.weekday_analyser import WeekDayAnalyser
from data_readers.nypd_reader import NypdReader
from data_writers.borough_splitter import BoroughSplitter
from folders_handling.folders import FoldersLookup
from analysers.casuality_analyser.killed_analyser import KilledAnalyser


# pd.set_option('display.max_columns',50)

# pd.set_option('display.width',1000)
# pd.set_option('display.max_colwidth', 100)


def prepare_weekly_analysis_files():
    weekAnalyser = WeekDayAnalyser()
    folders = FoldersLookup()
    for file_name in os.listdir(folders.by_borough):
        output_file_name = f'weekly_{file_name}'
        file_path = os.path.join(folders.by_borough, file_name)
        weekAnalyser.store_per_weekday_accident_count(file_path, output_file_name)

def split_data_by_borough(inputData :pd.DataFrame):
    boroughSplitter = BoroughSplitter()
    boroughSplitter.split_nypd_by_borough(inputData)

def prepare_most_killing_car_types():
    kill_analyser = KilledAnalyser()
    folders = FoldersLookup()
    for file_name in os.listdir(folders.by_borough):
        output_file_name = f'most_killing_vehice_type_{file_name}'
        file_path = os.path.join(folders.by_borough, file_name)
        kill_analyser.store_killed_info_by_vehicle_type(file_path, output_file_name)


if __name__ == "__main__":    
    
    
    #read input file
    reader = NypdReader()
    nypd_data = reader.read_nypd_file_to_data_frame('C:\\Development\\PandasZaliczenie\\nypd-motor-vehicle-collisions.csv')
    split_data_by_borough(nypd_data)
    prepare_weekly_analysis_files()
    prepare_most_killing_car_types()

    # print(by_borough.head(20))


