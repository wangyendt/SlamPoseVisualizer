"""
@author: wangye(Wayne)
@license: Apache Licence
@file: DataReader.py
@time: 20230323
@contact: wang121ye@hotmail.com
@site:  wangyendt@github.com
@software: PyCharm

# code is far away from bugs.
"""

import subprocess
import re
from typing import *
import pandas as pd
import os


class DataReader:
    def __init__(self):
        self.online = False
        self.logcat = None
        self.data_extract_handler = None
        self.path = ''

    def help(self) -> str:
        print('''
# An example of online reader hanlder would be like:

def handler(line: str) -> List[float]:
    if line and 'Twc' in line:
        data = [float(d) for d in re.findall(r'Twc:(.*)', line)[0].split(',')]
        return data
    else:
        return []
        
# Then you just need to call:

reader = DataReader()
reader.register_online_reader(handler)
for data in reader.read():
    print(data)
    
# Or if you want to use offline version, you need to call:

reader = DataReader()
reader.register_offline_reader('example/data.csv')
for data in reader.read():
    print(data)
            ''')

    def register_online_reader(self, data_extract_handler: Callable[[str], List[float]]):
        self.online = True
        self.data_extract_handler = data_extract_handler
        os.system("adb logcat -c")
        self.logcat = subprocess.Popen(["adb", "logcat"], stdout=subprocess.PIPE)

    def register_offline_reader(self, path: str):
        self.online = False
        self.path = path

    def read(self):
        if self.online:
            if not self.data_extract_handler:
                raise NotImplementedError(f'self.data_extract_handler not implemented!'
                                          f'Please call register_online_reader before read!')
            while not self.logcat.poll():
                line = self.logcat.stdout.readline().decode('utf-8').strip()
                data = self.data_extract_handler(line)
                if data:
                    yield data
        else:
            if not self.path or not os.path.exists(self.path):
                raise ValueError('self.path not set or not valid!')
            datas = pd.read_csv(self.path, delimiter=r',|\s').values
            for i in range(datas.shape[0]):
                data = datas[i].astype(list)
                yield data

    def close(self):
        if self.logcat:
            self.logcat.kill()
            self.logcat = None


if __name__ == '__main__':
    def handler(line: str) -> List[float]:
        if line and 'Twc' in line:
            data = [float(d) for d in re.findall(r'Twc:(.*)', line)[0].split(',')]
            return data
        else:
            return []


    reader = DataReader()
    reader.help()
    reader.register_offline_reader('example/data.csv')
    for data in reader.read():
        print(data)
    reader.register_online_reader(handler)
    for data in reader.read():
        print(data)
    reader.close()
