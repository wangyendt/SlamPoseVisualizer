"""
@author: wangye(Wayne)
@license: Apache Licence
@file: run_me.py
@time: 20230331
@contact: wang121ye@hotmail.com
@site:  wangyendt@github.com
@software: PyCharm

# code is far away from bugs.
"""

from DataReader import DataReader
from Visualizer import Visualizer
import re
from typing import List

if __name__ == '__main__':
    def mercury_handler(line: str) -> List[float]:
        if line and 'Twc' in line:
            data = [float(d) for d in re.findall(r'Twc:(.*)', line)[0].split(',')]
            return data
        else:
            return []


    def dm_handler(line: str) -> List[float]:
        if line and 'pose ts' in line:
            data = [float(d) for d in re.findall(r'pose ts:(.*) px:(.*) py:(.*) pz:(.*) qx:(.*) qy:(.*) qz:(.*) qw:(.*)', line)[0]]
            data[4], data[5], data[6], data[7] = data[7], data[4], data[5], data[6]
            return data
        else:
            return []


    def dm_cs_handler(line: str) -> List[float]:
        if line and 'KeyFrameState' in line:
            data = [float(d) for d in re.findall(r'KeyFrameState: timestamp: ([-\d.e]{2,}).*?([-\d.e]{2,}).*?([-\d.e]{2,}).*?([-\d.e]{2,}).*?([-\d.e]{2,}).*?([-\d.e]{2,}).*?([-\d.e]{2,}).*?([-\d.e]{2,}).*', line)[0]]
            return data
        else:
            return []


    reader = DataReader()
    reader.register_offline_reader('example/data.csv')
    # reader.register_online_reader(dm_cs_handler)
    # reader.register_online_reader(mercury_handler)
    visualizer = Visualizer(reader)
    visualizer.run()
