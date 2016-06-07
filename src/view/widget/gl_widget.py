#!/usr/bin/env python
# coding: utf-8

"""

gl_widget.py

GLWidgetクラスを定義するモジュール


"""

from PyQt4 import QtCore, QtGui, QtOpenGL
from OpenGL import GL
from src.util import color


class GLWidget(QtOpenGL.QGLWidget):
    """
    OpenGLを用いた3D描画を行うQtウィジェットクラス
    """

    DEFAULT_BG_COLOR = color.DARKULA_DARK

    DEFAULT_CAMERA_LOCATION = (0, 0, -10.0)

    MIN_SIZE = (100, 100)
    DEFAULT_SIZE = (400, 400)

    ROTATE_UNIT = 16.

    SIGNAL_X_ROTATION_CHANGED = QtCore.pyqtSignal(int)
    SIGNAL_Y_ROTATION_CHANGED = QtCore.pyqtSignal(int)
    SIGNAL_Z_ROTATION_CHANGED = QtCore.pyqtSignal(int)

    def __init__(self, renderer, parent=None, bg_color=DEFAULT_BG_COLOR):
        super(GLWidget, self).__init__(parent)

        self.object = 0
        self.rx = 0
        self.ry = 0
        self.rz = 0

        self.last_mouse_pos = QtCore.QPoint()

        self.renderer = renderer

        self.bg_color = bg_color

    def minimumSizeHint(self):
        """
        Widgetの最小サイズ
        :return: QSize
        """
        return QtCore.QSize(*self.MIN_SIZE)

    def sizeHint(self):
        """
        Widgetの推奨サイズ
        :return: QSize
        """
        return QtCore.QSize(*self.DEFAULT_SIZE)

    def set_x_rotation(self, angle):
        """
        x軸の回転を設定
        :param angle: 回転度数
        :return:
        """
        angle %= 360 * self.ROTATE_UNIT
        if angle != self.rx:
            self.rx = angle
            self.SIGNAL_X_ROTATION_CHANGED.emit(angle)
            self.updateGL()

    def set_y_rotation(self, angle):
        """
        y軸の回転を設定
        :param angle: 回転度数
        :return:
        """
        angle %= 360 * self.ROTATE_UNIT
        if angle != self.ry:
            self.ry = angle
            self.SIGNAL_Y_ROTATION_CHANGED.emit(angle)
            self.updateGL()

    def set_z_rotation(self, angle):
        """
        z軸の回転を設定
        :param angle: 回転度数
        :return:
        """
        angle %= 360 * self.ROTATE_UNIT
        if angle != self.rz:
            self.rz = angle
            self.SIGNAL_Z_ROTATION_CHANGED.emit(angle)
            self.updateGL()

    def initializeGL(self):
        """
        OpenGL周辺の設定を初期化
        :return:
        """
        self.qglClearColor(QtGui.QColor.fromRgb(*self.bg_color))
        # 描画オブジェクトの初期化
        self.update_object()
        # シェーディングの設定
        GL.glShadeModel(GL.GL_FLAT)
        # デプスバッファの更新を有効化
        GL.glEnable(GL.GL_DEPTH_TEST)
        # 平面の表のみを描画
        GL.glEnable(GL.GL_CULL_FACE)
        GL.glCullFace(GL.GL_FRONT)
        # アンチエイリアス
        GL.glEnable(GL.GL_POLYGON_SMOOTH)

    def paintGL(self):
        """
        OpenGLによる描画処理
        :return:
        """
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glLoadIdentity()
        # カメラをデフォルト位置からどれだけ移動するか
        GL.glTranslated(*self.DEFAULT_CAMERA_LOCATION)
        GL.glRotated(self.rx / self.ROTATE_UNIT, 1.0, 0.0, 0.0)
        GL.glRotated(self.ry / self.ROTATE_UNIT, 0.0, 1.0, 0.0)
        GL.glRotated(self.rz / self.ROTATE_UNIT, 0.0, 0.0, 1.0)
        GL.glCallList(self.object)

    def resizeGL(self, width, height):
        """
        ウィジェットがリサイズされるときの処理
        :param width: 親ウィジェットの幅
        :param height: 親ウィジェットの高さ
        :return:
        """
        side = min(width, height)
        if side < 0:
            return

        GL.glViewport((width - side) / 2, (height - side) / 2, side, side)

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho(-0.5, +0.5, +0.5, -0.5, 4.0, 15.0)
        GL.glMatrixMode(GL.GL_MODELVIEW)

    def mousePressEvent(self, event):
        """
        マウスが押下された時のイベントリスナー
        :param event: イベントオブジェクト
        :return:
        """
        self.last_mouse_pos = event.pos()

    def mouseMoveEvent(self, event):
        """
        マウスが移動した時のイベントリスナー
        :param event:  イベントオブジェクト
        :return:
        """

        if not event.buttons():
            return

        dx = event.x() - self.last_mouse_pos.x()
        dy = event.y() - self.last_mouse_pos.y()

        if QtCore.Qt.LeftButton:
            self.set_x_rotation(self.rx + self.ROTATE_UNIT / 2 * dy)
            self.set_y_rotation(self.ry + self.ROTATE_UNIT / 2 * dx)
        elif QtCore.Qt.RightButton:
            self.set_x_rotation(self.rx + self.ROTATE_UNIT / 2 * dy)
            self.set_z_rotation(self.rz + self.ROTATE_UNIT / 2 * dx)

        self.last_mouse_pos = event.pos()

    def __make_object(self):
        """
        GLWidget上オブジェクトを描画する
        :return:
        """
        genList = GL.glGenLists(1)
        GL.glNewList(genList, GL.GL_COMPILE)

        GL.glBegin(GL.GL_QUADS)

        self.renderer.render()

        GL.glEnd()
        GL.glEndList()

        return genList

    def update_object(self):
        """
        描画オブジェクトを更新する
        :return:
        """
        self.object = self.__make_object()
