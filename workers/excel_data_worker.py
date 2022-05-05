import pandas as pd

from data_writers.borough_splitter import BoroughSplitter

class ExcelDataWorker:
    def split_data_by_borough(self,inputData :pd.DataFrame):
        boroughSplitter = BoroughSplitter()
        boroughSplitter.split_nypd_by_borough(inputData)