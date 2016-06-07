#!/usr/bin/env python
# coding: utf-8

"""

voxel_renderer.py

Voxel描画用オブジェクトVoxelRendererを包含するモジュール

"""

import warnings
from OpenGL import GL
from abstract_renderer import AbstractRenderer
from src.util.color import RED
from src.model.voxel import Voxel


class VoxelRenderer(AbstractRenderer):
    """
    OpenGL上にボクセルデータを描画するクラス
    """

    def __init__(self, voxel=None):
        if voxel is not None:
            assert isinstance(voxel, Voxel)
        self.__voxel = voxel
        self.__color = RED

    def render(self):
        if self.__voxel is None:
            warnings.warn("VoxelRenderer::render() : voxel is None.")
            return
        # 正規化して描画
        print "render"
        n_div = self.__voxel.n_div
        for x, y, z in self.__voxel.active_coordinates:
            self.__cube(float(x) / n_div - 0.5,
                        float(y) / n_div - 0.5,
                        float(z) / n_div - 0.5, 1. / n_div)

    def set_color(self, color):
        self.__color = color

    def set_voxel(self, voxel):
        self.__voxel = voxel

    def __cube(self, x, y, z, cube_size):
        hs = cube_size / 2

        # self.qglColor(QtGui.QColor.fromRgb(*self.__color))

        # top
        GL.glVertex3d(x - hs, y - hs, z + hs)
        GL.glVertex3d(x + hs, y - hs, z + hs)
        GL.glVertex3d(x + hs, y + hs, z + hs)
        GL.glVertex3d(x - hs, y + hs, z + hs)

        # bottom
        GL.glVertex3d(x - hs, y - hs, z - hs)
        GL.glVertex3d(x - hs, y + hs, z - hs)
        GL.glVertex3d(x + hs, y + hs, z - hs)
        GL.glVertex3d(x + hs, y - hs, z - hs)

        # right side
        GL.glVertex3d(x + hs, y - hs, z - hs)
        GL.glVertex3d(x + hs, y + hs, z - hs)
        GL.glVertex3d(x + hs, y + hs, z + hs)
        GL.glVertex3d(x + hs, y - hs, z + hs)

        # left side
        GL.glVertex3d(x - hs, y - hs, z - hs)
        GL.glVertex3d(x - hs, y - hs, z + hs)
        GL.glVertex3d(x - hs, y + hs, z + hs)
        GL.glVertex3d(x - hs, y + hs, z - hs)

        # back side
        GL.glVertex3d(x - hs, y + hs, z - hs)
        GL.glVertex3d(x - hs, y + hs, z + hs)
        GL.glVertex3d(x + hs, y + hs, z + hs)
        GL.glVertex3d(x + hs, y + hs, z - hs)

        # # front side
        GL.glVertex3d(x - hs, y - hs, z - hs)
        GL.glVertex3d(x + hs, y - hs, z - hs)
        GL.glVertex3d(x + hs, y - hs, z + hs)
        GL.glVertex3d(x - hs, y - hs, z + hs)
