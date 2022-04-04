
import pandas as pd
import os.path
from data_readers.nypd_reader import NypdReader
from data_writers.borough_splitter import BoroughSplitter


# pd.set_option('display.max_columns',50)

# pd.set_option('display.width',1000)
# pd.set_option('display.max_colwidth', 100)


if __name__ == "__main__":    
    
    reader = NypdReader()
    nypd_data = reader.read_nypd_file_to_data_frame('D:\\Development\\Pandas\\nypd-motor-vehicle-collisions.csv')
    boroughSplitter = BoroughSplitter()
    boroughSplitter.split_nypd_by_borough(nypd_data)



    # print(by_borough.head(20))


