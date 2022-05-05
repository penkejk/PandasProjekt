import os
import pandas as pd
from analysers.findings_combiner import FindingsCombiner
from analysers.time_of_day_analyser.time_of_day_analyser import TimeOfDayAnalyser
from analysers.weekday_analyser.weekday_analyser import WeekDayAnalyser
from data_readers.nypd_reader import NypdReader
from data_writers.borough_splitter import BoroughSplitter
from data_writers.html_writer import HtmlWriter
from folders_handling.folders import FoldersLookup
from analysers.casuality_analyser.casuality_analyser import CasualityAnalyser
from analysers.casuality_analyser.injury_type import InjuryType
from workers.casuality_worker import CasualityWorker
from workers.excel_data_worker import ExcelDataWorker
from workers.report_data_worker import ReportDataWorker
from workers.time_of_day_worker import TimeOfDayWorker
from workers.weekly_data_worker import WeeklyDataWorker


folders = FoldersLookup()
html_writer = HtmlWriter()

if __name__ == "__main__":     
    

    input_file_path = f'{folders.input_data}\\nypd-motor-vehicle-collisions.csv'
    output_file_path = f'{folders.output_data}\\analysys_report.html'
    if os.path.exists(input_file_path) == False:
        raise Exception(f'The input file cannot be found under {input_file_path}')

    reader = NypdReader()
    nypd_data = reader.read_nypd_file_to_data_frame(input_file_path)
    ExcelDataWorker().split_data_by_borough(nypd_data)
    WeeklyDataWorker().prepare_weekly_analysis_files()
    casuality_worker = CasualityWorker()
    casuality_worker.prepare_most_killing_car_types('most_killing_vehice_type_',InjuryType.Killed)
    casuality_worker.prepare_most_killing_car_types('most_injuring_vehice_type_', InjuryType.Injured)
    TimeOfDayWorker().prepare_by_time_of_day_overview()     

    report_data_frame = ReportDataWorker().create_final_report()
    html_writer.write_data_frame_to_html(report_data_frame,output_file_path)