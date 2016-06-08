#!/usr/bin/env python
# coding: utf-8

"""

main_window.py

Qtウィジェット群をまとめるMainWindowクラスを包含するモジュール

"""

import numpy as np
from PyQt4 import QtGui, QtCore
from src.view.widget.gl_widget import GLWidget
from src.util.parse import parse_binvox
from src.util import color
from src.model.voxel import Voxel
from src.render.voxel_renderer import VoxelRenderer


class MainWindow(QtGui.QMainWindow):
    """
    ViewとなるQMainWindow派生クラス
    """
    DEFAULT_BACKGROUND_COLOR = color.DARKULA
    DEFAULT_MENUBAR_COLOR = color.DARKULA_DARK

    def __init__(self, title, parent=None, bg_color=DEFAULT_BACKGROUND_COLOR):
        super(MainWindow, self).__init__(parent)

        # title
        self.setWindowTitle(title)

        # Background Color
        self.set_background_color(bg_color)

        # menu bar
        self.file_menu = self.menuBar().addMenu("File")
        # for mac
        self.menuBar().setNativeMenuBar(False)
        # menu bar action
        self.file_menu.addAction("Open", self.load_binvox)

        # renderer
        self.voxel_renderer = VoxelRenderer()

        # GL widget
        self.gl = GLWidget(self.voxel_renderer)

        # sliders
        x_slider = self.create_slider()
        y_slider = self.create_slider()
        z_slider = self.create_slider()
        slider_layout = QtGui.QVBoxLayout()
        slider_layout.addWidget(x_slider)
        slider_layout.addWidget(y_slider)
        slider_layout.addWidget(z_slider)
        # callback setting for sliders and gl widget.
        x_slider.valueChanged.connect(self.gl.set_x_rotation)
        self.gl.SIGNAL_X_ROTATION_CHANGED.connect(x_slider.setValue)
        y_slider.valueChanged.connect(self.gl.set_y_rotation)
        self.gl.SIGNAL_Y_ROTATION_CHANGED.connect(y_slider.setValue)
        z_slider.valueChanged.connect(self.gl.set_z_rotation)
        self.gl.SIGNAL_Z_ROTATION_CHANGED.connect(z_slider.setValue)

        # light checkbox
        left_light, right_light, bottom_light, top_light = self.gl.LIGHTS
        left_lc = self.create_checkbox(left_light.type.name, color.WHITE)
        right_lc = self.create_checkbox(right_light.type.name, color.WHITE)
        bottom_lc = self.create_checkbox(bottom_light.type.name, color.WHITE)
        top_lc = self.create_checkbox(top_light.type.name, color.WHITE)
        checkbox_layout = QtGui.QVBoxLayout()
        checkbox_layout.addWidget(left_lc)
        checkbox_layout.addWidget(right_lc)
        checkbox_layout.addWidget(bottom_lc)
        checkbox_layout.addWidget(top_lc)
        # callback setting for checkboxes.
        left_lc.stateChanged.connect(lambda state: self.set_light(left_lc))
        right_lc.stateChanged.connect(lambda state: self.set_light(right_lc))
        bottom_lc.stateChanged.connect(lambda state: self.set_light(bottom_lc))
        top_lc.stateChanged.connect(lambda state: self.set_light(top_lc))

        # register all widgets to a main widget.
        layout = QtGui.QGridLayout()
        layout.addWidget(self.gl, 0, 0)
        layout.addLayout(slider_layout, 1, 0, 1, 2)
        layout.addLayout(checkbox_layout, 0, 1)
        main_widget = QtGui.QWidget()
        main_widget.setLayout(layout)

        # add widget to a window.
        self.setCentralWidget(main_widget)

    def set_background_color(self, rgb):
        """
        背景色を変更する
        :type rgb: tuple
        :param rgb: 8ビット256階調のRGB値
        """
        bg_palette = self.palette()
        q_color = QtGui.QColor.fromRgb(*rgb)
        bg_palette.setColor(QtGui.QPalette.Background, q_color)
        self.setPalette(bg_palette)

    def load_binvox(self):
        """
        binvoxファイルの読み込み
        """
        file_name = QtGui.QFileDialog().getOpenFileName(self, 'Open', "~")
        binvox = parse_binvox(file_name)
        voxel = Voxel(np.argwhere(binvox), len(binvox))
        self.voxel_renderer.set_voxel(voxel)
        self.gl.update_object()
        self.gl.updateGL()

    def set_light(self, checkbox):
        self.gl.set_light_enable(str(checkbox.text()), checkbox.isChecked())

    def create_slider(self):
        """
        Sliderウィジェットを生成する
        :return: QSlider
        """
        slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        slider.setRange(0, 360 * self.gl.ROTATE_UNIT)
        slider.setSingleStep(self.gl.ROTATE_UNIT)
        slider.setPageStep(15 * self.gl.ROTATE_UNIT)
        slider.setTickInterval(15 * self.gl.ROTATE_UNIT)
        slider.setTickPosition(QtGui.QSlider.TicksRight)
        return slider

    def create_checkbox(self, text, text_rgb):
        check_box = QtGui.QCheckBox(text, self)
        palette = check_box.palette()
        palette.setColor(QtGui.QPalette.Foreground,
                         QtGui.QColor.fromRgb(*text_rgb))
        check_box.setPalette(palette)
        return check_box
