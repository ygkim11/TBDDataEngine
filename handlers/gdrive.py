import os
import shutil
import datetime
import pandas as pd
import h5py

def _backup(backup_type):
    today = datetime.datetime.now()
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)

    prev_folder_name = yesterday.strftime('%Y-%m-%d')
    folder_name = today.strftime('%Y-%m-%d')

    curr_file_name = f"{today.strftime('%Y-%m-%d_%H')}.csv"

    prev_local_location = f'C:\\Users\\simpl\\real_time_data\\{backup_type}\\{prev_folder_name}'
    local_location = f'C:\\Users\\simpl\\real_time_data\\{backup_type}\\{folder_name}'

    if not os.path.exists(prev_local_location):
        os.makedirs(prev_local_location)

    prev_local_files = os.listdir(prev_local_location)
    local_files = os.listdir(local_location)

    prev_gdrive_location = f'G:\\공유 드라이브\\Project_TBD\\Stock_Data\\real_time\\{backup_type}\\{prev_folder_name}'
    gdrive_location = f'G:\\공유 드라이브\\Project_TBD\\Stock_Data\\real_time\\{backup_type}\\{folder_name}'

    if not os.path.exists(prev_gdrive_location):
        os.makedirs(prev_gdrive_location)

    if not os.path.exists(gdrive_location):
        os.makedirs(gdrive_location)

    prev_gdrive_files = os.listdir(prev_gdrive_location)
    gdrive_files = os.listdir(gdrive_location)

    prev_to_move = list(set(prev_local_files).difference(set(prev_gdrive_files)))
    to_move = list(set(local_files).difference(set(gdrive_files)))

    for file in prev_to_move:
        shutil.copy2(
            f'{prev_local_location}\\{file}',
            f'{prev_gdrive_location}\\{file}'
        )

    for file in to_move:
        if file != curr_file_name:
            shutil.copy2(
                f'{local_location}\\{file}',
                f'{gdrive_location}\\{file}'
            )

def backup_upbit_data():
    _backup('upbit')

def backup_kiwoom_stocks_data():
    _backup('kiwoom_stocks')

def backup_kiwoom_futures_data():
    _backup('kiwoom_futures')


def transform_csv_to_arr():
    loc = 'C:\\Users\\simpl\\real_time_data\\upbit\\2020-12-27'
    file = f'{loc}\\2020-12-27_20.csv'
    df = pd.read_csv(file, header=None)
    # df.sort_values([1, 2, 3], ascending=True, inplace=True)
    # print(df[df[0] == 'KRW-BTC'])
    print(df)

    # arr = df.values
    # print(arr)


if __name__ == '__main__':
    # backup_upbit_data()
    # backup_kiwoom_stocks_data()
    # backup_kiwoom_futures_data()
    transform_csv_to_arr()