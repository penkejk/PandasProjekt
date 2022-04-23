
import os
from numpy import delete
import pandas as pd

class HtmlWriter():

    def write_data_frame_to_html(self, data_frame: pd.DataFrame, folder :str, file_path:str):
            if os.path.exists(file_path):
                os.remove(file_path)

            html_output = data_frame.to_html()
            os.makedirs(folder, exist_ok=True)
            with open(file_path, 'x') as file:
                file.write(html_output)