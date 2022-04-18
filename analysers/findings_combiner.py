import pandas as pd
import os


class FindingsCombiner:


    def combine_findings(self,folder_path:str, sortColumnName:str):

        resulting_file_name_path = f'{folder_path}\\merged_results.csv'
        if os.path.exists(resulting_file_name_path):
            os.remove(resulting_file_name_path)

        findings_frames = []
        for file_path in os.listdir(folder_path):
            raw_data = pd.read_csv(f'{folder_path}\\{file_path}')
            findings_frames.append(raw_data)
        mergedData = pd.concat(findings_frames, axis='index')
        mergedData.index.name = 'index'
        mergedData=mergedData.sort_values([sortColumnName], ascending=False)
        mergedData.to_csv(resulting_file_name_path)