#!/usr/bin/env python
# coding: utf-8

"""

object.py

OpenGLにおけるモデルを描画する関数を含むモジュール

"""

from OpenGL import GL


def cube(x, y, z, cube_size):
    """
    立方体をOpenGLで描画する関数
    指定した座標を中心に一辺cube_sizeの立方体を描画
    :type x,y,z,cube_cube_size:int
    :param x: 中心座標のx
    :param y: 中心座標のy
    :param z: 中心座標のz
    :param cube_size: 一辺のサイズ
    :return:
    """
    hs = cube_size / 2

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
