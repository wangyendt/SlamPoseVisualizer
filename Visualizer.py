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

        self.view_point_f = 500
        self.view_point_x = 0
        self.view_point_y = -0.7
        self.view_point_z = -3.5
        self.w = 640
        self.h = 480
        self.fx = 496.9221841793908
        self.fy = 496.67218249523825
        self.cx = 320.13043105863295
        self.cy = 241.12304842660265

    def run(self):
        pango.CreateWindowAndBind("pySimpleDisplay", 640, 480)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        pm = pango.ProjectionMatrix(self.w, self.h, self.fx, self.fy, self.cx, self.cy, 0.1, 1000)
        mv = pango.ModelViewLookAt(5, -3, 5, 0, 0, 0, pango.AxisZ)
        s_cam = pango.OpenGlRenderState(pm, mv)
        handler = pango.Handler3D(s_cam)

        ui_width = pango.Attach(0.3)  # 180
        d_cam = (
            pango.CreateDisplay()
            .SetBounds(
                pango.Attach(0),
                pango.Attach(1),
                ui_width,  # pango.Attach.Pix(ui_width)
                pango.Attach(1),
                -self.w / self.h,
            )
            .SetHandler(handler)
        )

        log = pango.DataLog()
        log.SetLabels(["x", "y", "z"])
        plotter = pango.Plotter(log, 0, 400, -10, 10, 1, 1)
        plotter.Track("$i")
        plotter.SetBounds(pango.Attach(0.4), pango.Attach(0.8),
                          pango.Attach(0), ui_width)

        log2 = pango.DataLog()
        log2.SetLabels(["roll", "pitch", "yaw"])
        plotter2 = pango.Plotter(log2, 0, 400, -200, 200, 1, 1)
        plotter2.Track("$i")
        plotter2.AddMarker(pango.Marker.Horizontal, 180, pango.Marker.GreaterThan, pango.Colour.Red().WithAlpha(0.2))
        plotter2.AddMarker(pango.Marker.Horizontal, -180, pango.Marker.LessThan, pango.Colour.Red().WithAlpha(0.2))
        plotter2.AddMarker(pango.Marker.Horizontal, 0, pango.Marker.Equal, pango.Colour.Green().WithAlpha(0.2))
        plotter2.SetBounds(pango.Attach(0), pango.Attach(0.4),
                           pango.Attach(0), ui_width)
        pango.DisplayBase().AddDisplay(plotter)
        pango.DisplayBase().AddDisplay(plotter2)

        pango.CreatePanel("ui").SetBounds(
            pango.Attach(0.8), pango.Attach(1.0), pango.Attach(0), ui_width
        )
        var_ui = pango.Var("ui")
        var_ui.follow_camera = (False, pango.VarMeta(toggle=True))
        var_ui.camera_view = False
        b_follow = True
        b_camera_view = True
        # var_ui.a_Toggle = (False, pango.VarMeta(toggle=True))
        # var_ui.a_double = (0.0, pango.VarMeta(0, 5))
        # var_ui.an_int = (2, pango.VarMeta(0, 5))
        # var_ui.a_double_log = (3.0, pango.VarMeta(1, 1e4, logscale=True))
        # var_ui.a_checkbox = (False, pango.VarMeta(toggle=True))
        # var_ui.an_int_no_input = 2
        # var_ui.a_str = "sss"

        ctrl = -96

        def a_callback():
            print("a pressed")

        pango.RegisterKeyPressCallback(ctrl + ord("a"), a_callback)

        trajectory = []
        camera_Twc = []
        for data in self.reader.read():
            ts, px, py, pz, qw, qx, qy, qz = data
            trajectory.append([px, py, pz])
            quat = Quaternion(np.array([qw, qx, qy, qz]))
            R = quat.to_DCM()
            E = quat.to_angles() * 180 / np.pi
            Twc = np.array([
                [R[0, 0], R[1, 0], R[2, 0], 0],
                [R[0, 1], R[1, 1], R[2, 1], 0],
                [R[0, 2], R[1, 2], R[2, 2], 0],
                [px, py, pz, 1]
            ])
            TwcGL = pango.OpenGlMatrix(Twc.T)
            OwGL = pango.OpenGlMatrix(np.array([
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [px, py, pz, 1.0]
            ]))
            log.Log(px, py, pz)
            log2.Log(E[0], E[1], E[2])
            trajectory.append([px, py, pz])

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            if var_ui.a_checkbox:
                var_ui.an_int = var_ui.a_double

            if var_ui.GuiChanged('an_int'):
                var_ui.an_int_no_input = var_ui.an_int

            if var_ui.follow_camera and b_follow:
                if b_camera_view:
                    s_cam.Follow(TwcGL)
                else:
                    s_cam.Follow(OwGL)
            elif var_ui.follow_camera and not b_follow:
                if b_camera_view:
                    s_cam.SetProjectionMatrix(pango.ProjectionMatrix(self.w, self.h, self.view_point_f, self.view_point_f, self.cx, self.cy, 0.1, 1000))
                    s_cam.SetModelViewMatrix(pango.ModelViewLookAt(self.view_point_x, self.view_point_y, self.view_point_z, 0, 0, 0, 0.0, -1.0, 0.0))
                    s_cam.Follow(TwcGL)
                else:
                    s_cam.SetProjectionMatrix(pango.ProjectionMatrix(self.w, self.h, 3000, 3000, self.cx, self.cy, 0.1, 1000))
                    s_cam.SetModelViewMatrix(pango.ModelViewLookAt(0, 0.01, 10, 0, 0, 0, 0.0, 0.0, 1.0))
                    s_cam.Follow(OwGL)
                b_follow = True
            elif not var_ui.follow_camera and b_follow:
                b_follow = False

            if var_ui.camera_view:
                var_ui.camera_view = False
                b_camera_view = True
                s_cam.SetProjectionMatrix(pango.ProjectionMatrix(self.w, self.h, self.view_point_f, self.view_point_f, self.cx, self.cy, 0.1, 10000))
                s_cam.SetModelViewMatrix(pango.ModelViewLookAt(self.view_point_x, self.view_point_y, self.view_point_z, 0, 0, 0, 0.0, -1.0, 0.0))
                s_cam.Follow(TwcGL)

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

            camera_Twc.append(Twc)
            camera_Twc_ = camera_Twc[:-1][::10] + [camera_Twc[-1]]
            for i, Twc_ in enumerate(camera_Twc_):
                w = 0.2
                h = w * 0.75
                z = w * 0.6
                glPushMatrix()
                glMultMatrixd(Twc_)
                glLineWidth(2)
                glBegin(GL_LINES)
                glColor4f(0, 1, 1, (i + 1) / len(camera_Twc_))
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


    reader = DataReader()
    reader.register_offline_reader('example/data.csv')
    # reader.register_online_reader(mercury_handler)
    visualizer = Visualizer(reader)
    visualizer.run()
