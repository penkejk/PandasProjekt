
import os
from analysers.findings_combiner import FindingsCombiner
from analysers.time_of_day_analyser.time_of_day_analyser import TimeOfDayAnalyser
from folders_handling.folders import FoldersLookup


class TimeOfDayWorker:
    folders = FoldersLookup()
    combiner = FindingsCombiner()
    
    def prepare_by_time_of_day(self):
        time_of_day_analyser = TimeOfDayAnalyser()
        for file_name in os.listdir(self.folders.by_borough):
            output_file_name = f'{file_name}'
            file_path = os.path.join(self.folders.by_borough, file_name)
            time_of_day_analyser.store_per_time_of_day_count(file_path, output_file_name)
        self.combiner.combine_findings(f'{self.folders.findings_folder}\\{self.folders.findings_by_time_of_day}','COLLISION_ID')