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
from src.render.object.cube import cube


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
            GL.glBegin(GL.GL_QUADS)
            cube(float(x) / n_div - 0.5,
                 float(y) / n_div - 0.5,
                 float(z) / n_div - 0.5, 1. / n_div)
            GL.glEnd()

    def set_voxel(self, voxel):
        """
        ボクセルのmutator
        :type voxel: Voxel
        :param voxel: ボクセルクラスオブジェクト
        :return:
        """
        self.__voxel = voxel
