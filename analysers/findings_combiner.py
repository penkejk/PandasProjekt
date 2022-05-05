import os
import pandas as pd


class FindingsCombiner:
    

    def combine_findings(self,folder_path:str, sort_column_name:str):
        """
        Combines findings from separate by borough files
        and sorts them using the specified column.
        """

        resulting_file_name_path = f'{folder_path}\\merged_results.csv'
        if os.path.exists(resulting_file_name_path):
            os.remove(resulting_file_name_path)

        findings_frames = []
        for file_path in os.listdir(folder_path):
            raw_data = pd.read_csv(f'{folder_path}\\{file_path}')
            findings_frames.append(raw_data)
        mergedData = pd.concat(findings_frames, axis='index')
        mergedData.index.name = 'index'
        mergedData=mergedData.sort_values([sort_column_name], ascending=False)
        mergedData.to_csv(resulting_file_name_path)