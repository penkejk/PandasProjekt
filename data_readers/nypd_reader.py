import pandas as pd

class NypdReader():
    
    def read_nypd_file_to_data_frame(self,filePath:str) -> pd.DataFrame:
        return pd.read_csv(filePath)
