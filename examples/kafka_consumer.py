from kafka import KafkaConsumer
from json import loads
import h5py
import csv
import datetime
import numpy as np
import pandas as pd

# 카프카 서버
bootstrap_servers = ["localhost:9092"]

# 카프카 토픽
str_topic_name    = 'kiwoom'

consumer = KafkaConsumer(
                        str_topic_name,
                        bootstrap_servers=bootstrap_servers,
                        auto_offset_reset='earliest', # 가장 처음부터 소비
                        group_id=None
                        )

"""
HDF5 structure:
filename: yyyymmdd / dataset: [ticker]

Processing method:
- consume daily tick/hoga data from kafka
- consume line by line and make [ticker].csv files
- loop and read in each csv file
- make dataframe data to numpy array
- save as hdf5 file
"""

# Process 1 : save to csv
today = datetime.datetime.now().strftime('%Y%m%d')
tmp_path = ".\\tmp"
gd_path = "G:\\내 드라이브\\TestData"

for message in consumer:
    data = loads(message)
    data_list = data.split(',')
    ticker = data_list[0] # 첫째값이 티커
    
    with open(f'{tmp_path}\\{ticker}.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)

# Process 2 : save to google drive
for f in os.listdir(tmp_path):
    ticker = f.split('.')[0]
    arr = pd.read_csv(f'{tmp_path}\\{f}').to_numpy()
    hd = h5py.File(f'{gd_path}\\{today}.h5', 'w')
    hd.create_dataset(ticker, data=arr)