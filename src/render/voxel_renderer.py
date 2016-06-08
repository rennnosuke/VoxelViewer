#!/usr/bin/env python
# coding: utf-8

"""

voxel_renderer.py

Voxel描画用オブジェクトVoxelRendererを包含するモジュール

"""

import warnings
from OpenGL import GL
from abstract_renderer import AbstractRenderer
from src.model.voxel import Voxel


class VoxelRenderer(AbstractRenderer):
    """
    OpenGL上にボクセルデータを描画するクラス
    """

    def __init__(self, voxel=None):
        if voxel is not None:
            assert isinstance(voxel, Voxel)
        self.__voxel = voxel

    def render(self):
        if self.__voxel is None:
            warnings.warn("VoxelRenderer::render() : voxel is None.")
            return
        # 正規化して描画
        n_div = self.__voxel.n_div
        for x, y, z in self.__voxel.active_coordinates:
            self.__cube(float(x) / n_div - 0.5,
                        float(y) / n_div - 0.5,
                        float(z) / n_div - 0.5, 1. / n_div)

    def set_voxel(self, voxel):
        """
        ボクセルのmutator
        :type voxel: Voxel
        :param voxel: ボクセルクラスオブジェクト
        :return:
        """
        self.__voxel = voxel

    def __cube(self, x, y, z, cube_size):
        """
        立方体をOpenGLで描画するメソッド
        指定した座標を中心に一辺cube_sizeの立方体を描画
        :type x,y,z,cube_cube_size:int
        :param x: 中心座標のx
        :param y: 中心座標のy
        :param z: 中心座標のz
        :param cube_size: 一辺のサイズ
        :return:
        """
        hs = cube_size / 2

        GL.glBegin(GL.GL_QUADS)

        # top
        GL.glNormal3dv((0.0, 0.0, 1.0))
        GL.glVertex3d(x - hs, y - hs, z + hs)
        GL.glVertex3d(x + hs, y - hs, z + hs)
        GL.glVertex3d(x + hs, y + hs, z + hs)
        GL.glVertex3d(x - hs, y + hs, z + hs)

        # bottom
        GL.glNormal3dv((0.0, 0.0, -1.0))
        GL.glVertex3d(x - hs, y - hs, z - hs)
        GL.glVertex3d(x - hs, y + hs, z - hs)
        GL.glVertex3d(x + hs, y + hs, z - hs)
        GL.glVertex3d(x + hs, y - hs, z - hs)

        # right side
        GL.glNormal3dv((1.0, 0.0, 0.0))
        GL.glVertex3d(x - hs, y - hs, z - hs)
        GL.glVertex3d(x + hs, y - hs, z - hs)
        GL.glVertex3d(x + hs, y + hs, z - hs)
        GL.glVertex3d(x + hs, y + hs, z + hs)
        GL.glVertex3d(x + hs, y - hs, z + hs)

        # left side
        GL.glNormal3dv((-1.0, 0.0, 0.0))
        GL.glVertex3d(x - hs, y - hs, z - hs)
        GL.glVertex3d(x - hs, y - hs, z + hs)
        GL.glVertex3d(x - hs, y + hs, z + hs)
        GL.glVertex3d(x - hs, y + hs, z - hs)

        # back side
        GL.glNormal3dv((0.0, 1.0, 0.0))
        GL.glVertex3d(x - hs, y + hs, z - hs)
        GL.glVertex3d(x - hs, y + hs, z + hs)
        GL.glVertex3d(x + hs, y + hs, z + hs)
        GL.glVertex3d(x + hs, y + hs, z - hs)

        # front side
        GL.glNormal3dv((0.0, -1.0, 0.0))
        GL.glVertex3d(x - hs, y - hs, z - hs)
        GL.glVertex3d(x + hs, y - hs, z - hs)
        GL.glVertex3d(x + hs, y - hs, z + hs)
        GL.glVertex3d(x - hs, y - hs, z + hs)

        GL.glEnd()
