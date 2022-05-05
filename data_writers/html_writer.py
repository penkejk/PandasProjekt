
import pandas as pd

class HtmlWriter:

    def write_data_frame_to_html(self, data_frame: pd.DataFrame, file_path:str):
            data_frame.to_html(open(file_path, 'w'))
