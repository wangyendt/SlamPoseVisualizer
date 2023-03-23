"""
@author: wangye(Wayne)
@license: Apache Licence
@file: Visualizer.py
@time: 20230323
@contact: wang121ye@hotmail.com
@site:  wangyendt@github.com
@software: PyCharm

# code is far away from bugs.
"""

from DataReader import DataReader
from typing import *
import re
import pypangolin as pango
from OpenGL.GL import *
from ahrs import Quaternion, QuaternionArray
import numpy as np


class Visualizer:
    def __init__(self, reader: DataReader):
        self.reader = reader
        self.var_ui = None
        self.s_cam = None
        self.d_cam = None

    def run(self):
        pango.CreateWindowAndBind("pySimpleDisplay", 640, 480)
        glEnable(GL_DEPTH_TEST)
        pm = pango.ProjectionMatrix(640, 480, 420, 420, 320, 240, 0.1, 1000)
        mv = pango.ModelViewLookAt(5, -3, 5, 0, 0, 0, pango.AxisZ)
        s_cam = pango.OpenGlRenderState(pm, mv)
        handler = pango.Handler3D(s_cam)
        ui_width = 180
        d_cam = (
            pango.CreateDisplay()
            .SetBounds(
                pango.Attach(0),
                pango.Attach(1),
                pango.Attach.Pix(ui_width),
                pango.Attach(1),
                -640.0 / 480.0,
            )
            .SetHandler(handler)
        )

        pango.CreatePanel("ui").SetBounds(
            pango.Attach(0), pango.Attach(1), pango.Attach(0), pango.Attach.Pix(ui_width)
        )
        var_ui = pango.Var("ui")
        var_ui.a_Button = False
        var_ui.a_Toggle = (False, pango.VarMeta(toggle=True))
        var_ui.a_double = (0.0, pango.VarMeta(0, 5))
        var_ui.an_int = (2, pango.VarMeta(0, 5))
        var_ui.a_double_log = (3.0, pango.VarMeta(1, 1e4, logscale=True))
        var_ui.a_checkbox = (False, pango.VarMeta(toggle=True))
        var_ui.an_int_no_input = 2
        var_ui.a_str = "sss"

        ctrl = -96

        def a_callback():
            print("a pressed")

        pango.RegisterKeyPressCallback(ctrl + ord("a"), a_callback)

        trajectory = []
        for data in self.reader.read():
            ts, px, py, pz, qw, qx, qy, qz = data
            trajectory.append([px, py, pz])
            quat = Quaternion(np.array([qw, qx, qy, qz]))
            R = quat.to_DCM()
            Twc = np.array([
                [R[0, 0], R[1, 0], R[2, 0], 0],
                [R[0, 1], R[1, 1], R[2, 1], 0],
                [R[0, 2], R[1, 2], R[2, 2], 0],
                [px, py, pz, 1]
            ])
            trajectory.append([px, py, pz])

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            if var_ui.a_checkbox:
                var_ui.an_int = var_ui.a_double

            if var_ui.GuiChanged('an_int'):
                var_ui.an_int_no_input = var_ui.an_int

            d_cam.Activate(s_cam)
            # pango.glDrawColouredCube()

            glLineWidth(3)
            glBegin(GL_LINES)
            glColor3f(1, 0, 0)
            glVertex3f(0, 0, 0)
            glVertex3f(1, 0, 0)
            glColor3f(0, 1, 0)
            glVertex3f(0, 0, 0)
            glVertex3f(0, 1, 0)
            glColor3f(0, 0, 1)
            glVertex3f(0, 0, 0)
            glVertex3f(0, 0, 1)
            glEnd()

            quat = Quaternion(np.array([qw, qx, qy, qz]))
            R = quat.to_DCM()
            glPushMatrix()
            Twc = np.array([
                [R[0, 0], R[1, 0], R[2, 0], 0],
                [R[0, 1], R[1, 1], R[2, 1], 0],
                [R[0, 2], R[1, 2], R[2, 2], 0],
                [px, py, pz, 1]
            ])
            glMultMatrixd(Twc)

            w = 0.2
            h = w * 0.75
            z = w * 0.6
            glLineWidth(2)
            glBegin(GL_LINES)
            glColor3f(0, 1, 1)
            glVertex3f(0, 0, 0)
            glVertex3f(w, h, z)
            glVertex3f(0, 0, 0)
            glVertex3f(w, -h, z)
            glVertex3f(0, 0, 0)
            glVertex3f(-w, -h, z)
            glVertex3f(0, 0, 0)
            glVertex3f(-w, h, z)
            glVertex3f(w, h, z)
            glVertex3f(w, -h, z)
            glVertex3f(-w, h, z)
            glVertex3f(-w, -h, z)
            glVertex3f(-w, h, z)
            glVertex3f(w, h, z)
            glVertex3f(-w, -h, z)
            glVertex3f(w, -h, z)
            glEnd()
            glPopMatrix()

            glLineWidth(2)
            glBegin(GL_LINES)
            glColor3f(0, 1, 0)
            for j in range(len(trajectory) - 1):
                glVertex3d(trajectory[j][0], trajectory[j][1], trajectory[j][2])
                glVertex3d(trajectory[j + 1][0], trajectory[j + 1][1], trajectory[j + 1][2])
            glEnd()

            pango.FinishFrame()
            if pango.ShouldQuit():
                break


if __name__ == '__main__':
    def handler(line: str) -> List[float]:
        if line and 'Twc' in line:
            data = [float(d) for d in re.findall(r'Twc:(.*)', line)[0].split(',')]
            return data
        else:
            return []


    reader = DataReader()
    reader.register_offline_reader('example/data.csv')
    reader.register_online_reader(handler)
    visualizer = Visualizer(reader)
    visualizer.run()
