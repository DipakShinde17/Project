# Angle measurment with how to reduce -------------


import sys
import numpy as np
import open3d as o3d
from PyQt5 import QtWidgets, QtCore, QtGui
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
import math

class RailwayViewer(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Railway Speed & Angle Suggester (Industrial Project)")
        self.setGeometry(100, 100, 1500, 900)

        self.points = None
        self.colors = None
        self.selected_points = []
        self.measure_mode = False
        self.temp_actors = []
        self.measured_angle = 0.0

        main = QtWidgets.QWidget()
        self.setCentralWidget(main)
        layout = QtWidgets.QHBoxLayout(main)

        # --- Left Panel ---
        left = QtWidgets.QVBoxLayout()

        self.btn_load = QtWidgets.QPushButton("1. Load PLY Data")
        self.btn_load.setFixedHeight(40)
        self.btn_load.clicked.connect(self.load_data)

        self.btn_angle = QtWidgets.QPushButton("2. Start Angle Measurement")
        self.btn_angle.setFixedHeight(40)
        self.btn_angle.clicked.connect(self.enable_angle_measurement)

        # Target Speed Input
        self.speed_label_input = QtWidgets.QLabel("3. Enter Target Speed (km/hr):")
        self.speed_input = QtWidgets.QLineEdit()
        self.speed_input.setPlaceholderText("Ex: 80")
        self.speed_input.setValidator(QtGui.QIntValidator(1, 200)) # फक्त नंबर अलाउड
        self.speed_input.textChanged.connect(self.update_suggestion) # स्पीड बदलली की लगेच रिझल्ट दिसेल

        # Result Labels
        self.result_box = QtWidgets.QGroupBox("Analysis Results")
        res_layout = QtWidgets.QVBoxLayout()
        
        self.label_measured = QtWidgets.QLabel("Measured Angle: --")
        self.label_suggested = QtWidgets.QLabel("Suggested Angle: --")
        self.label_correction = QtWidgets.QLabel("Correction Needed: --")
        self.label_current_speed = QtWidgets.QLabel("Safe Speed (Current): --")
        
        # 
        for lbl in [self.label_measured, self.label_suggested, self.label_correction, self.label_current_speed]:
            lbl.setStyleSheet("font-size: 13px; color: #333;")
        self.label_correction.setStyleSheet("font-weight: bold; color: red;")

        res_layout.addWidget(self.label_measured)
        res_layout.addWidget(self.label_current_speed)
        res_layout.addWidget(QtWidgets.QLabel("-" * 20))
        res_layout.addWidget(self.label_suggested)
        res_layout.addWidget(self.label_correction)
        self.result_box.setLayout(res_layout)

        left.addWidget(self.btn_load)
        left.addWidget(self.btn_angle)
        left.addWidget(self.speed_label_input)
        left.addWidget(self.speed_input)
        left.addWidget(self.result_box)
        left.addStretch()

        left_widget = QtWidgets.QWidget()
        left_widget.setLayout(left)
        left_widget.setFixedWidth(300)

        # --- VTK Viewer ---
        self.vtk = QVTKRenderWindowInteractor(self)
        self.renderer = vtk.vtkRenderer()
        self.vtk.GetRenderWindow().AddRenderer(self.renderer)
        self.vtk.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())

        layout.addWidget(left_widget)
        layout.addWidget(self.vtk)

        self.vtk.Initialize()
        self.vtk.Start()

        self.picker = vtk.vtkCellPicker()
        self.picker.SetTolerance(0.0005)
        self.vtk.SetPicker(self.picker)
        self.vtk.AddObserver("LeftButtonPressEvent", self.on_left_click)

    # --- Calculations Logic ---
    def update_suggestion(self):
       
        if self.measured_angle <= 0 or not self.speed_input.text():
            return

        try:
            target_v = float(self.speed_input.text())
            G = 1.676
            Cd = 75

           
            # R = (V / 0.27)^2 / Cd
            R_req = ((target_v / 0.27)**2) / Cd
            
            # N = sqrt(R / 1.5G)
            N_req = math.sqrt(R_req / (1.5 * G))
            
           #theta = atan(1/N)
            suggested_angle_rad = math.atan(1 / N_req)
            suggested_angle_deg = math.degrees(suggested_angle_rad)
            
            
            correction = self.measured_angle - suggested_angle_deg

            # UI 
            self.label_suggested.setText(f"Suggested Angle: {suggested_angle_deg:.2f}° (1 in {N_req:.1f})")
            self.label_correction.setText(f"Correction: Reduce by {correction:.2f}°" if correction > 0 else f"Correction: Increase by {abs(correction):.2f}°")
        except:
            pass

    def calculate_railway_params(self, angle_deg):
        
        G = 1.676
        Cd = 75
        rad = math.radians(angle_deg)
        N = 1 / math.tan(rad)
        R = 1.5 * G * (N**2)
        V = 0.27 * math.sqrt(R * Cd)
        return N, R, V

    # --- VTK & UI Handlers ---
    def load_data(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open PLY", "", "*.ply")
        if not file: return
        pcd = o3d.io.read_point_cloud(file)
        self.points = np.asarray(pcd.points)
        self.colors = np.asarray(pcd.colors) if pcd.has_colors() else np.ones((len(self.points), 3))
        self.show_points()

    def enable_angle_measurement(self):
        if self.points is None: return
        self.measure_mode = True
        self.selected_points = []
        self.clear_temp_actors()
        self.label_measured.setText("Select 3 points...")

    def calculate_angle(self, p1, p2, p3):
        a, b, c = np.array(p1), np.array(p2), np.array(p3)
        ba, bc = a - b, c - b
        cos_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        return np.degrees(np.arccos(np.clip(cos_angle, -1.0, 1.0)))

    def on_left_click(self, obj, event):
        if not self.measure_mode or self.points is None: return

        click_pos = self.vtk.GetEventPosition()
        self.picker.Pick(click_pos[0], click_pos[1], 0, self.renderer)
        point_id = self.picker.GetPointId()

        if point_id >= 0:
            picked_point = self.points[point_id]
            self.selected_points.append(picked_point)
            self.draw_point_marker(picked_point)

            if len(self.selected_points) == 2:
                self.draw_line(self.selected_points[0], self.selected_points[1])

            if len(self.selected_points) == 3:
                p1, p2, p3 = self.selected_points
                self.draw_line(p2, p3)
                
                self.measured_angle = self.calculate_angle(p1, p2, p3)
                N, R, V = self.calculate_railway_params(self.measured_angle)
                
                self.label_measured.setText(f"Measured Angle: {self.measured_angle:.2f}°")
                self.label_current_speed.setText(f"Safe Speed (Current): {V:.2f} km/hr")
                self.show_angle_text(p2, self.measured_angle)
                
                
                self.update_suggestion()

                self.measure_mode = False
                self.selected_points = []

            self.vtk.GetRenderWindow().Render()

    # --- Helper Drawing Methods ---
    def draw_line(self, p1, p2):
        line = vtk.vtkLineSource()
        line.SetPoint1(p1); line.SetPoint2(p2)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(line.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(1, 0, 0); actor.GetProperty().SetLineWidth(3)
        self.renderer.AddActor(actor)
        self.temp_actors.append(actor)

    def draw_point_marker(self, p):
        sphere = vtk.vtkSphereSource()
        sphere.SetCenter(p); sphere.SetRadius(0.05)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(sphere.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(0, 0, 1)
        self.renderer.AddActor(actor)
        self.temp_actors.append(actor)

    def show_angle_text(self, point, angle):
        text = vtk.vtkBillboardTextActor3D()
        text.SetPosition(point)
        text.SetInput(f"Measured: {angle:.2f}°")
        text.GetTextProperty().SetFontSize(18); text.GetTextProperty().SetColor(0.2, 0.2, 0.2)
        self.renderer.AddActor(text)
        self.temp_actors.append(text)

    def clear_temp_actors(self):
        for actor in self.temp_actors: self.renderer.RemoveActor(actor)
        self.temp_actors = []
        self.vtk.GetRenderWindow().Render()

    def show_points(self):
        vtk_pts = vtk.vtkPoints()
        colors = vtk.vtkUnsignedCharArray()
        colors.SetNumberOfComponents(3)
        for i, p in enumerate(self.points):
            vtk_pts.InsertNextPoint(float(p[0]), float(p[1]), float(p[2]))
            c = (self.colors[i] * 255).astype(np.uint8)
            colors.InsertNextTuple3(int(c[0]), int(c[1]), int(c[2]))
        poly = vtk.vtkPolyData()
        poly.SetPoints(vtk_pts); poly.GetPointData().SetScalars(colors)
        vertices = vtk.vtkCellArray()
        for i in range(len(self.points)):
            vertices.InsertNextCell(1); vertices.InsertCellPoint(i)
        poly.SetVerts(vertices)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(poly)
        actor = vtk.vtkActor()
        actor.SetMapper(mapper); actor.GetProperty().SetPointSize(1)
        self.renderer.RemoveAllViewProps()
        self.renderer.AddActor(actor)
        self.renderer.SetBackground(0.9, 0.9, 0.9)
        self.renderer.ResetCamera()
        self.vtk.GetRenderWindow().Render()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = RailwayViewer()
    win.show()
    sys.exit(app.exec_())



# import sys
# import numpy as np
# import open3d as o3d
# from PyQt5 import QtWidgets, QtCore, QtGui
# from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
# import vtk
# import math


# class RailwayViewer(QtWidgets.QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle("Railway Speed & Angle Suggester — IRS:TR-10 Correct Formulas")
#         self.setGeometry(100, 100, 1500, 900)

#         self.points         = None
#         self.colors         = None
#         self.selected_points = []
#         self.measure_mode   = False
#         self.temp_actors    = []
#         self.measured_angle = 0.0
#         self.bbox_diagonal  = 1.0

#         # ── Indian Railways IRS:TR-10 Constants ──
#         self.G  = 1.676   # Broad Gauge (metres)
#         self.Cd = 75.0    # Cant Deficiency limit (mm) — IRS standard
#         self.Ca = 65.0    # Actual Cant assumed (mm) — typical loop line

#         main = QtWidgets.QWidget()
#         self.setCentralWidget(main)
#         layout = QtWidgets.QHBoxLayout(main)

#         # ── Left Panel ──
#         left = QtWidgets.QVBoxLayout()

#         self.btn_load = QtWidgets.QPushButton("1. Load PLY Data")
#         self.btn_load.setFixedHeight(40)
#         self.btn_load.clicked.connect(self.load_data)

#         self.btn_angle = QtWidgets.QPushButton("2. Start Angle Measurement")
#         self.btn_angle.setFixedHeight(40)
#         self.btn_angle.clicked.connect(self.enable_angle_measurement)

#         self.speed_label_input = QtWidgets.QLabel("3. Enter Target Speed (km/h):")
#         self.speed_input = QtWidgets.QLineEdit()
#         self.speed_input.setPlaceholderText("Ex: 50")
#         self.speed_input.setValidator(QtGui.QIntValidator(1, 200))
#         self.speed_input.textChanged.connect(self.update_suggestion)

#         # ── Result Box ──
#         self.result_box = QtWidgets.QGroupBox("Analysis Results (IRS:TR-10)")
#         res_layout = QtWidgets.QVBoxLayout()

#         self.label_measured       = QtWidgets.QLabel("Measured Angle     : --")
#         self.label_measured_N     = QtWidgets.QLabel("Crossing Number    : --")
#         self.label_measured_R     = QtWidgets.QLabel("Curve Radius (Rc)  : --")
#         self.label_current_speed  = QtWidgets.QLabel("Safe Speed (Current): --")
#         self.label_sep            = QtWidgets.QLabel("─" * 28)
#         self.label_target_speed   = QtWidgets.QLabel("Target Speed       : --")
#         self.label_suggested      = QtWidgets.QLabel("Suggested Angle    : --")
#         self.label_suggested_N    = QtWidgets.QLabel("Suggested Cross No : --")
#         self.label_suggested_R    = QtWidgets.QLabel("Suggested Rc       : --")
#         self.label_correction     = QtWidgets.QLabel("Correction Needed  : --")
#         self.label_formula        = QtWidgets.QLabel(
#             "\nFormulas Used (IRS:TR-10):\n"
#             " N = 1/tan(θ)\n"
#             " Rc = G × N² / 2\n"
#             " V = 0.347 × √Rc\n"
#             " G = 1.676m (BG)\n"
#             " Cd = 75mm (limit)"
#         )

#         for lbl in [
#             self.label_measured, self.label_measured_N,
#             self.label_measured_R, self.label_current_speed,
#             self.label_target_speed, self.label_suggested,
#             self.label_suggested_N, self.label_suggested_R,
#         ]:
#             lbl.setStyleSheet("font-size:12px; color:#222;")

#         self.label_correction.setStyleSheet(
#             "font-size:13px; font-weight:bold; color:#c00;"
#         )
#         self.label_formula.setStyleSheet(
#             "font-size:10px; color:#555; background:#f0f0f0;"
#             "padding:6px; border-radius:4px;"
#         )

#         for w in [
#             self.label_measured, self.label_measured_N,
#             self.label_measured_R, self.label_current_speed,
#             self.label_sep,
#             self.label_target_speed, self.label_suggested,
#             self.label_suggested_N, self.label_suggested_R,
#             self.label_correction, self.label_formula,
#         ]:
#             res_layout.addWidget(w)

#         self.result_box.setLayout(res_layout)

#         left.addWidget(self.btn_load)
#         left.addWidget(self.btn_angle)
#         left.addWidget(self.speed_label_input)
#         left.addWidget(self.speed_input)
#         left.addWidget(self.result_box)
#         left.addStretch()

#         left_widget = QtWidgets.QWidget()
#         left_widget.setLayout(left)
#         left_widget.setFixedWidth(320)

#         # ── VTK Viewer ──
#         self.vtk_w = QVTKRenderWindowInteractor(self)
#         self.renderer = vtk.vtkRenderer()
#         self.vtk_w.GetRenderWindow().AddRenderer(self.renderer)
#         self.vtk_w.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())

#         layout.addWidget(left_widget)
#         layout.addWidget(self.vtk_w)

#         self.vtk_w.Initialize()
#         self.vtk_w.Start()

#         # FIX: vtkCellPicker + GetPickPosition — avoids point_id mismatch
#         self.picker = vtk.vtkCellPicker()
#         self.picker.SetTolerance(0.0001)
#         self.vtk_w.SetPicker(self.picker)
#         self.vtk_w.AddObserver("LeftButtonPressEvent", self.on_left_click)

#     # ──────────────────────────────────────────────────────
#     # CORRECT IRS:TR-10 FORMULAS
#     # ──────────────────────────────────────────────────────
#     def calculate_railway_params(self, angle_deg):
#         if angle_deg <= 0 or angle_deg >= 90:
#             return 0, 0, 0
#         rad = math.radians(angle_deg)

#         # Crossing Number
#         N  = 1.0 / math.tan(rad)

#         # Curve Radius — correct formula (no ÷2)
#         Rc = self.G * N * N          # ← ÷2 hatva

#         # Speed — simplest correct IRS formula
#         V  = 3.65 * N                # ← he vapara

#         return N, Rc, V

#     # def calculate_angle_from_speed(self, target_v):
#     def calculate_angle_from_speed(self, target_v):
#         N   = target_v / 3.65        # ← direct
#         Rc  = self.G * N * N
#         ang = math.degrees(math.atan(1.0 / N)) if N > 0 else 0
#         return N, Rc, ang
    
#     def update_suggestion(self):
#         """Called when target speed input changes."""
#         if self.measured_angle <= 0:
#             return
#         txt = self.speed_input.text().strip()
#         if not txt:
#             return
#         try:
#             target_v = float(txt)
#             if target_v <= 0:
#                 return

#             # Suggested values for target speed
#             N_sug, Rc_sug, ang_sug = self.calculate_angle_from_speed(target_v)

#             correction = self.measured_angle - ang_sug

#             self.label_target_speed.setText(
#                 f"Target Speed       : {target_v:.0f} km/h"
#             )
#             self.label_suggested.setText(
#                 f"Suggested Angle    : {ang_sug:.2f}°"
#             )
#             self.label_suggested_N.setText(
#                 f"Suggested Cross No : N = {N_sug:.1f}  (1 in {N_sug:.1f})"
#             )
#             self.label_suggested_R.setText(
#                 f"Suggested Rc       : {Rc_sug:.1f} m"
#             )

#             if abs(correction) < 0.1:
#                 self.label_correction.setText(
#                     "Correction Needed  : ✓ Current angle is correct!"
#                 )
#                 self.label_correction.setStyleSheet(
#                     "font-size:13px;font-weight:bold;color:green;"
#                 )
#             elif correction > 0:
#                 self.label_correction.setText(
#                     f"Correction Needed  : ↓ Reduce angle by {correction:.2f}°\n"
#                     f"(Current {self.measured_angle:.2f}° → Target {ang_sug:.2f}°)"
#                 )
#                 self.label_correction.setStyleSheet(
#                     "font-size:12px;font-weight:bold;color:#c00;"
#                 )
#             else:
#                 self.label_correction.setText(
#                     f"Correction Needed  : ↑ Increase angle by {abs(correction):.2f}°\n"
#                     f"(Current {self.measured_angle:.2f}° → Target {ang_sug:.2f}°)"
#                 )
#                 self.label_correction.setStyleSheet(
#                     "font-size:12px;font-weight:bold;color:#e07000;"
#                 )

#         except Exception as e:
#             print("update_suggestion error:", e)

#     # ──────────────────────────────────────────────────────
#     # LOAD PLY
#     # ──────────────────────────────────────────────────────
#     def load_data(self):
#         file, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open PLY", "", "*.ply")
#         if not file:
#             return
#         pcd          = o3d.io.read_point_cloud(file)
#         self.points  = np.asarray(pcd.points)
#         self.colors  = (np.asarray(pcd.colors)
#                         if pcd.has_colors()
#                         else np.ones((len(self.points), 3)))
#         self.bbox_diagonal = np.linalg.norm(
#             self.points.max(axis=0) - self.points.min(axis=0)
#         )
#         self.show_points()

#     # ──────────────────────────────────────────────────────
#     # ANGLE MEASUREMENT
#     # ──────────────────────────────────────────────────────
#     def enable_angle_measurement(self):
#         if self.points is None:
#             return
#         self.measure_mode    = True
#         self.selected_points = []
#         self.clear_temp_actors()
#         self.label_measured.setText("Click 1: Main track point")

#     def calculate_angle(self, p1, p2, p3):
#         """Acute crossing angle at vertex p2."""
#         a, b, c = np.array(p1), np.array(p2), np.array(p3)
#         ba, bc  = a - b, c - b
#         n1, n2  = np.linalg.norm(ba), np.linalg.norm(bc)
#         if n1 < 1e-10 or n2 < 1e-10:
#             return 0.0
#         cos_a = np.clip(np.dot(ba, bc) / (n1 * n2), -1.0, 1.0)
#         ang   = np.degrees(np.arccos(cos_a))
#         # Return acute crossing angle
#         return ang if ang <= 90.0 else 180.0 - ang

#     # ──────────────────────────────────────────────────────
#     # CLICK HANDLER — FIX: GetPickPosition not GetPointId
#     # ──────────────────────────────────────────────────────
#     def on_left_click(self, obj, event):
#         if not self.measure_mode or self.points is None:
#             return

#         # FIX: correct interactor + GetPickPosition
#         interactor = self.vtk_w.GetRenderWindow().GetInteractor()
#         cx, cy     = interactor.GetEventPosition()
#         self.picker.Pick(cx, cy, 0, self.renderer)

#         pos = self.picker.GetPickPosition()
#         if self.picker.GetDataSet() is None:
#             n = len(self.selected_points)
#             self.label_measured.setText(
#                 f"⚠ Nothing picked (step {n+1}/3) — click ON a point"
#             )
#             return

#         picked_point = [pos[0], pos[1], pos[2]]
#         self.selected_points.append(picked_point)
#         self.draw_point_marker(picked_point)

#         n = len(self.selected_points)

#         if n == 1:
#             self.label_measured.setText("✓ Pt1 set. Click 2: Switch point")

#         elif n == 2:
#             self.draw_line(self.selected_points[0], picked_point)
#             self.label_measured.setText("✓ Pt2 set. Click 3: Loop line point")

#         elif n == 3:
#             p1, p2, p3 = self.selected_points
#             self.draw_line(p2, picked_point)

#             # Calculate angle
#             self.measured_angle = self.calculate_angle(p1, p2, p3)

#             # Calculate params for measured angle
#             N, Rc, V = self.calculate_railway_params(self.measured_angle)

#             # Update UI
#             self.label_measured.setText(
#                 f"Measured Angle     : {self.measured_angle:.2f}°"
#             )
#             self.label_measured_N.setText(
#                 f"Crossing Number    : N = {N:.1f}  (1 in {N:.1f})"
#             )
#             self.label_measured_R.setText(
#                 f"Curve Radius (Rc)  : {Rc:.1f} m"
#             )
#             self.label_current_speed.setText(
#                 f"Safe Speed (Current): {V:.2f} km/h"
#             )

#             self.show_angle_text(p2, self.measured_angle, V)

#             # Auto-update suggestion if speed already entered
#             self.update_suggestion()

#             self.measure_mode    = False
#             self.selected_points = []

#         self.vtk_w.GetRenderWindow().Render()

#     # ──────────────────────────────────────────────────────
#     # DRAWING HELPERS
#     # ──────────────────────────────────────────────────────
#     def draw_line(self, p1, p2):
#         line = vtk.vtkLineSource()
#         line.SetPoint1(p1)
#         line.SetPoint2(p2)
#         mapper = vtk.vtkPolyDataMapper()
#         mapper.SetInputConnection(line.GetOutputPort())
#         actor = vtk.vtkActor()
#         actor.SetMapper(mapper)
#         actor.GetProperty().SetColor(1, 0.2, 0.1)
#         actor.GetProperty().SetLineWidth(3)
#         self.renderer.AddActor(actor)
#         self.temp_actors.append(actor)

#     def draw_point_marker(self, p):
#         # Auto-scale sphere radius
#         r = max(self.bbox_diagonal * 0.0005, 1e-6)
#         sphere = vtk.vtkSphereSource()
#         sphere.SetCenter(float(p[0]), float(p[1]), float(p[2]))
#         sphere.SetRadius(r)
#         sphere.SetThetaResolution(16)
#         sphere.SetPhiResolution(16)
#         mapper = vtk.vtkPolyDataMapper()
#         mapper.SetInputConnection(sphere.GetOutputPort())
#         actor = vtk.vtkActor()
#         actor.SetMapper(mapper)
#         actor.GetProperty().SetColor(0.1, 0.4, 1.0)
#         self.renderer.AddActor(actor)
#         self.temp_actors.append(actor)

#     def show_angle_text(self, point, angle, speed):
#         text = vtk.vtkBillboardTextActor3D()
#         text.SetPosition(float(point[0]), float(point[1]), float(point[2]))
#         text.SetInput(f"Angle: {angle:.2f} deg | Speed: {speed:.1f} km/h")
#         text.GetTextProperty().SetFontSize(18)
#         text.GetTextProperty().SetColor(0.1, 0.1, 0.8)
#         text.GetTextProperty().BoldOn()
#         self.renderer.AddActor(text)
#         self.temp_actors.append(text)

#     def clear_temp_actors(self):
#         for actor in self.temp_actors:
#             self.renderer.RemoveActor(actor)
#         self.temp_actors = []
#         self.vtk_w.GetRenderWindow().Render()

#     def show_points(self):
#         vtk_pts = vtk.vtkPoints()
#         cols    = vtk.vtkUnsignedCharArray()
#         cols.SetNumberOfComponents(3)
#         cols.SetName("Colors")
#         for i, p in enumerate(self.points):
#             vtk_pts.InsertNextPoint(float(p[0]), float(p[1]), float(p[2]))
#             c = (self.colors[i] * 255).astype(np.uint8)
#             cols.InsertNextTuple3(int(c[0]), int(c[1]), int(c[2]))
#         poly = vtk.vtkPolyData()
#         poly.SetPoints(vtk_pts)
#         poly.GetPointData().SetScalars(cols)
#         verts = vtk.vtkCellArray()
#         for i in range(len(self.points)):
#             verts.InsertNextCell(1)
#             verts.InsertCellPoint(i)
#         poly.SetVerts(verts)
#         mapper = vtk.vtkPolyDataMapper()
#         mapper.SetInputData(poly)
#         actor = vtk.vtkActor()
#         actor.SetMapper(mapper)
#         actor.GetProperty().SetPointSize(2)
#         self.renderer.RemoveAllViewProps()
#         self.renderer.AddActor(actor)
#         self.renderer.SetBackground(0.92, 0.92, 0.92)
#         self.renderer.ResetCamera()
#         self.vtk_w.GetRenderWindow().Render()
#         self.temp_actors = []


# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     win = RailwayViewer()
#     win.show()
#     sys.exit(app.exec_())