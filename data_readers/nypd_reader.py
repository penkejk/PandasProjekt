import pandas as pd

class NypdReader():
    
    def read_nypd_file_to_data_frame(self,file_path:str) -> pd.DataFrame:
        return pd.read_csv(file_path)
