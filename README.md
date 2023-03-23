# adbSlamPoseVisualizer
 A tool for slam pose visualizing via ADB stream base on pypangolin and pyopenGL.

## 0. Demo

Suppose you have your VO / VIO / SLAM algorithm running online and printing realtime position and quaternion (Twc). You can use this tool to visualize the realtime camera pose. 

![image-20230323133512971](https://p.ipic.vip/kcz16p.png)

## 1. Usage

```
git clone https://github.com/wangyendt/adbSlamPoseVisualizer
cd adbSlamPoseVisualizer
python Visualizer.py # run example
```

### 1.1 online version

In your script, define a handler to handle each line of your logcat to extract the required pose and quaternion, a.k.a Twc. If you are not familiar with the procedure, you can call ``reader.help()`` to show an example code.

```python
from DataReader import DataReader
from Visualizer import Visualizer

def handler(line: str) -> List[float]:
  if line and 'Twc' in line:
    data = [float(d) for d in re.findall(r'Twc:(.*)', line)[0].split(',')]
    return data
  else:
    return []
reader = DataReader()
reader.register_online_reader(handler)
visualizer = Visualizer(reader)
visualizer.run()
```

### 1.2 offline version

If you have a log file, you can use this offline version. The data format should be like:

````
timestamp, pos_x, pos_y, pos_z, quat_w, quat_x, quat_y, quat_z
````

Make sure the delimiter to be either comma or space. And quaternion uses Hamiton convention.

```python
from DataReader import DataReader
from Visualizer import Visualizer

reader = DataReader()
reader.register_offline_reader('example/data.csv')
visualizer = Visualizer(reader)
visualizer.run()
```

## 2. License

```
MIT License

Copyright (c) 2022 Ye Wang

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 3. Video

(To be added)
