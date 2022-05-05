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
from workers.time_of_day_worker import TimeOfDayWorker
from workers.weekly_data_worker import WeeklyDataWorker


folders = FoldersLookup()
_html_writer = HtmlWriter()


    

def create_final_report()-> pd.DataFrame:
    merged_file_name = 'merged_results.csv'

    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thrusday','Friday','Saturday','Sunday']

    per_file_frames = []
    


    for file_name in os.listdir(folders.by_borough):
        borough_name = f'{file_name}'.replace('.csv','')
        weekday_storage_path = os.path.join(folders.findings_folder, folders.findings_by_weekday,merged_file_name)
        by_vehicle_type_kill = os.path.join(folders.findings_folder, folders.findings_by_vehicle_type_kill,merged_file_name)
        by_vehicle_type_injured = os.path.join(folders.findings_folder, folders.findings_by_vehicle_type_injured,merged_file_name)
        by_time_of_day = os.path.join(folders.findings_folder, folders.findings_by_time_of_day,merged_file_name)  
        print(f'Report for {borough_name}')
        weekday_df = pd.read_csv(weekday_storage_path)
        weekday_df= weekday_df[weekday_df['borough']==borough_name]
        weekday_df = weekday_df[weekday_df['index'] == 0]
        weekday_df.reset_index(drop=True, inplace=True)      
        most_weekday = weekday_df.at[0, 'weekday']
        collisions_wd = weekday_df.at[0, 'COLLISION_ID']
        print(f'The most accidents happened on day {weekdays[most_weekday]} with {collisions_wd} collisions')

        time_of_day_df = pd.read_csv(by_time_of_day)
        time_of_day_df = time_of_day_df[time_of_day_df['index'] == 0]
        time_of_day_df = time_of_day_df[time_of_day_df['borough']==borough_name]
        time_of_day_df.reset_index(drop=True, inplace=True)  
        most_time_day = time_of_day_df.at[0, 'DAY TIME']
        collisions_td = time_of_day_df.at[0, 'COLLISION_ID']
        print(f'The most accidents happened during {most_time_day} with {collisions_td} collisions')

        killing_vehicle_df = pd.read_csv(by_vehicle_type_kill)
        killing_vehicle_df = killing_vehicle_df[killing_vehicle_df['index'] == 0]
        killing_vehicle_df = killing_vehicle_df[killing_vehicle_df['borough']==borough_name]
        killing_vehicle_df.reset_index(drop=True, inplace=True)  
        killing_type = killing_vehicle_df.at[0, 'VEHICLE TYPE CODE 1']
        collisions_kill = killing_vehicle_df.at[0, 'KILLED PEOPLE']
        print(f'The most accidents resulting in kills were caused by {killing_type} with {collisions_kill} kills')

        injuring_vehicle_df = pd.read_csv(by_vehicle_type_injured)
        injuring_vehicle_df = injuring_vehicle_df[injuring_vehicle_df['index'] == 0]
        injuring_vehicle_df = injuring_vehicle_df[injuring_vehicle_df['borough']==borough_name]
        injuring_vehicle_df.reset_index(drop=True, inplace=True)  
        injuring_type = injuring_vehicle_df.at[0, 'VEHICLE TYPE CODE 1']
        collisions_injures = injuring_vehicle_df.at[0, 'INJURED PEOPLE']
        print(f'The most accidents resulting in injuries were caused by {injuring_type} with {collisions_injures} injuries')

        file_data_frame_data = [[borough_name, weekdays[most_weekday], collisions_wd, most_time_day, collisions_td, killing_type,collisions_kill,injuring_type,collisions_injures]]
        columns= ["BOROUGH NAME", "WEEKDAY","NO OF COLLISIONS ON WEEKDAY","TIME OF DAY", "COLLISIONS ON TIME OF DAY", "MOST KILLING VEHICLE", "KILL COUNT", "MOST INJURING VEHICLE", "INJURY COUNT"]
        file_data_frame = pd.DataFrame(data = file_data_frame_data, columns= columns)

        per_file_frames.append(file_data_frame)

        print(f'-------------END OF REPORT FOR {file_name}------------------')
    
    resulting_data_frame = pd.concat(per_file_frames, ignore_index=True)
    return resulting_data_frame

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

    report_data_frame = create_final_report()
    _html_writer.write_data_frame_to_html(report_data_frame,output_file_path)
 


