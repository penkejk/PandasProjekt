
import os
import pandas as pd

class HtmlWriter:

    def write_data_frame_to_html(self, data_frame: pd.DataFrame, folder :str, file_path:str):
            # if os.path.exists(file_path):
            #     os.remove(file_path)
            data_frame.to_html(open(file_path, 'w'))
