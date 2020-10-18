import os
import h5py
import datetime
import pandas as pd

today = datetime.datetime.now().strftime('%Y%m%d')
tmp_path = ".\\tmp"
gd_path = "G:\내 드라이브\TestData"

hd = h5py.File(f'{gd_path}\\{today}.h5', 'w')

for f in os.listdir(tmp_path):
    ticker = f.split('.')[0]
    arr = pd.read_csv(f'{tmp_path}\\{f}', header=None).to_numpy()
    hd.create_dataset(ticker, data=arr)