from kafka import KafkaConsumer
import os
import csv
import datetime

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

today = datetime.datetime.now().strftime('%Y%m%d')
tmp_path = ".\\tmp"
gd_path = "G:\내 드라이브\TestData"

for message in consumer:
    data = message.value.decode('utf-8').replace('"', '')
    data_list = data.split(',')[:-1]
    print(data_list)
    ticker = data_list[0] # 첫째값이 티커

    filename = f'{tmp_path}\\{ticker}.csv'

    if not os.path.isfile(filename):
        open(filename, 'w').close()

    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data_list)