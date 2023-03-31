# SlamPoseVisualizer
 A tool for slam pose visualizing via ADB stream base on pypangolin and pyopenGL.

## 0. Demo

Suppose you have your VO / VIO / SLAM algorithm running online and printing realtime position and quaternion (Twc). You can use this tool to visualize the realtime camera pose. 


<img width="640" alt="Snipaste_2023-03-27_19-21-52" src="https://user-images.githubusercontent.com/18455758/227927883-cfb4aaf5-3d41-4567-b66e-fec43d85e2bc.png">

<img width="640" alt="Snipaste_2023-03-27_19-22-29" src="https://user-images.githubusercontent.com/18455758/227927900-cc13d92a-a0ac-47e5-8044-fbcfdeb523de.png">

## 1. Installation & Usage

First, compile official Pangolin python lib.

```bash
# Get Pangolin
cd ~/your_fav_code_directory
git clone --recursive https://github.com/stevenlovegrove/Pangolin.git
cd Pangolin

# Install dependencies (as described above, or your preferred method)
./scripts/install_prerequisites.sh recommended

# Configure and build
cmake -B build
cmake --build build

# GIVEME THE PYTHON STUFF!!!! (Check the output to verify selected python version)
cmake --build build -t pypangolin_pip_install

sudo make install
```



After that, you could run the following script in python to verify Pangolin lib is installed.

```python
import pangolin
```



Then you could run our script.

```bash
cd ~/your_fav_code_directory
git clone https://github.com/wangyendt/adbSlamPoseVisualizer
cd adbSlamPoseVisualizer
python run_me.py # run example
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



## 4. Reference

Thanks to the following repo:

[https://github.com/yuntianli91/pangolin_tutorial](https://github.com/yuntianli91/pangolin_tutorial)
