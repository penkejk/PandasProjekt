import sys
import os
import pandas as pd
from analysers.findings_combiner import FindingsCombiner
from analysers.time_of_day_analyser.time_of_day_analyser import TimeOfDayAnalyser
from analysers.weekday_analyser.weekday_analyser import WeekDayAnalyser
from data_readers.nypd_reader import NypdReader
from data_writers.borough_splitter import BoroughSplitter
from folders_handling.folders import FoldersLookup
from analysers.casuality_analyser.casuality_analyser import CasualityAnalyser
from analysers.casuality_analyser.injury_type import InjuryType


# pd.set_option('display.max_columns',50)

# pd.set_option('display.width',1000)
# pd.set_option('display.max_colwidth', 100)

combiner = FindingsCombiner()

def prepare_weekly_analysis_files():
    weekAnalyser = WeekDayAnalyser()
    folders = FoldersLookup()
    for file_name in os.listdir(folders.by_borough):
        output_file_name = f'weekly_{file_name}'
        file_path = os.path.join(folders.by_borough, file_name)
        weekAnalyser.store_per_weekday_accident_count(file_path, output_file_name)
    combiner.combine_findings(f'{folders.findings_folder}\\{folders.findings_by_weekday}','COLLISION_ID')


def split_data_by_borough(inputData :pd.DataFrame):
    boroughSplitter = BoroughSplitter()
    boroughSplitter.split_nypd_by_borough(inputData)

def prepare_most_killing_car_types(outputFilePrefix:str, injury :InjuryType ):
    kill_analyser = CasualityAnalyser()
    folders = FoldersLookup()
    for file_name in os.listdir(folders.by_borough):
        output_file_name = f'{outputFilePrefix}{file_name}'
        file_path = os.path.join(folders.by_borough, file_name)
        kill_analyser.store_casuality_info_by_vehicle_type(file_path, output_file_name,injury)
    
    output_file_name = folders.findings_by_vehicle_type_kill
    sort_field_substring = 'KILLED'
    if injury == InjuryType.Injured:
        output_file_name = folders.findings_by_vehicle_type_injured
        sort_field_substring = 'INJURED'
    combiner.combine_findings(f'{folders.findings_folder}\\{output_file_name}',f'{sort_field_substring} PEOPLE')

def prepare_by_time_of_day():
    time_of_day_analyser = TimeOfDayAnalyser()
    folders = FoldersLookup()
    for file_name in os.listdir(folders.by_borough):
        output_file_name = f'{file_name}'
        file_path = os.path.join(folders.by_borough, file_name)
        time_of_day_analyser.store_per_time_of_day_count(file_path, output_file_name)
    combiner.combine_findings(f'{folders.findings_folder}\\{folders.findings_by_time_of_day}','COLLISION_ID')
    

def create_final_report():
    folders = FoldersLookup()
    merged_file_name = 'merged_results.csv'

    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thrusday','Friday','Saturday','Sunday']

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

        print(f'-------------END OF REPORT FOR {file_name}------------------')


if __name__ == "__main__":     
    
    file_path = sys.argv[0]

    #read input file
    reader = NypdReader()
    nypd_data = reader.read_nypd_file_to_data_frame('D:\\Development\\Pandas\\nypd-motor-vehicle-collisions.csv')
    ###nypd_data = reader.read_nypd_file_to_data_frame(file_path)
    split_data_by_borough(nypd_data)
    prepare_weekly_analysis_files()
    prepare_most_killing_car_types('most_killing_vehice_type_',InjuryType.Killed)
    prepare_most_killing_car_types('most_injuring_vehice_type_', InjuryType.Injured)
    prepare_by_time_of_day()      
    create_final_report()
    create_final_report()
    # print(by_borough.head(20))


