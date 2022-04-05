
from glob import glob
import os
import pandas as pd
import glob
from analysers.weekday_analyser.weekday_analyser import WeekDayAnalyser
from data_readers.nypd_reader import NypdReader
from data_writers.borough_splitter import BoroughSplitter
from folders_handling.folders import FoldersLookup


# pd.set_option('display.max_columns',50)

# pd.set_option('display.width',1000)
# pd.set_option('display.max_colwidth', 100)


if __name__ == "__main__":    
    
    folders = FoldersLookup()
    #read input file
    # reader = NypdReader()
    # nypd_data = reader.read_nypd_file_to_data_frame('C:\\Development\\PandasZaliczenie\\nypd-motor-vehicle-collisions.csv')

    # #create per borough files    
    # boroughSplitter = BoroughSplitter()
    # boroughSplitter.split_nypd_by_borough(nypd_data)

    weekAnalyser = WeekDayAnalyser()
    for file_name in os.listdir(folders.by_borough):
        file_path = os.path.join(folders.by_borough, file_name)
        weekAnalyser.get_per_weekday_accident_count(file_path, file_name);



    # print(by_borough.head(20))


