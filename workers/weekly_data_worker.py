import os
from analysers.findings_combiner import FindingsCombiner
from analysers.weekday_analyser.weekday_analyser import WeekDayAnalyser
from folders_handling.folders import FoldersLookup


class WeeklyDataWorker:
    folders = FoldersLookup()
    combiner = FindingsCombiner()
    
    def prepare_weekly_analysis_files(self):
        weekAnalyser = WeekDayAnalyser()
        for file_name in os.listdir(self.folders.by_borough):
            output_file_name = f'weekly_{file_name}'
            file_path = os.path.join(self.folders.by_borough, file_name)
            weekAnalyser.store_per_weekday_accident_count(file_path, output_file_name)
        self.combiner.combine_findings(f'{self.folders.findings_folder}\\{self.folders.findings_by_weekday}','COLLISION_ID')