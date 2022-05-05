import os
from analysers.casuality_analyser.casuality_analyser import CasualityAnalyser
from analysers.casuality_analyser.injury_type import InjuryType
from analysers.findings_combiner import FindingsCombiner
from folders_handling.folders import FoldersLookup


class CasualityWorker:
    folders = FoldersLookup()
    combiner = FindingsCombiner()

    def prepare_most_killing_car_types(self,outputFilePrefix:str, injury :InjuryType ):
        kill_analyser = CasualityAnalyser()
        for file_name in os.listdir(self.folders.by_borough):
            output_file_name = f'{outputFilePrefix}{file_name}'
            file_path = os.path.join(self.folders.by_borough, file_name)
            kill_analyser.store_casuality_info_by_vehicle_type(file_path, output_file_name,injury)
        
        output_file_name = self.folders.findings_by_vehicle_type_kill
        sort_field_substring = 'KILLED'
        if injury == InjuryType.Injured:
            output_file_name = self.folders.findings_by_vehicle_type_injured
            sort_field_substring = 'INJURED'
        self.combiner.combine_findings(f'{self.folders.findings_folder}\\{output_file_name}',f'{sort_field_substring} PEOPLE')