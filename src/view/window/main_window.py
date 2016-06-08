#!/usr/bin/env python
# coding: utf-8

"""

main_window.py

Qtウィジェット群をまとめるMainWindowクラスを包含するモジュール

"""

import numpy as np
from PyQt4 import QtGui, QtCore
from src.view.widget import gl_widget
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
        self.file_menu = self.menuBar().addMenu("&File")
        # for mac
        self.menuBar().setNativeMenuBar(False)
        # menu bar action
        self.file_menu.addAction("Open", self.load_binvox)

        # renderer
        self.voxel_renderer = VoxelRenderer()

        # GL widget
        self.gl = gl_widget.GLWidget(self.voxel_renderer)

        # sliders
        self.x_slider = self.create_slider()
        self.y_slider = self.create_slider()
        self.z_slider = self.create_slider()

        # register all widgets to a main widget.
        slider_layout = QtGui.QGridLayout()
        slider_layout.addWidget(self.gl)
        slider_layout.addWidget(self.x_slider)
        slider_layout.addWidget(self.y_slider)
        slider_layout.addWidget(self.z_slider)
        main_widget = QtGui.QWidget()
        main_widget.setLayout(slider_layout)

        # add widget to a window.
        self.setCentralWidget(main_widget)

        # callback setting for sliders and gl widget.
        self.x_slider.valueChanged.connect(self.gl.set_x_rotation)
        self.gl.SIGNAL_X_ROTATION_CHANGED.connect(self.x_slider.setValue)
        self.y_slider.valueChanged.connect(self.gl.set_y_rotation)
        self.gl.SIGNAL_Y_ROTATION_CHANGED.connect(self.y_slider.setValue)
        self.z_slider.valueChanged.connect(self.gl.set_z_rotation)
        self.gl.SIGNAL_Z_ROTATION_CHANGED.connect(self.z_slider.setValue)

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
