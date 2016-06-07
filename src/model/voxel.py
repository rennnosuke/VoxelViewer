#!/usr/bin/env python
# coding: utf-8

"""

voxel.py

ボクセルデータクラスを定義するモジュール


"""

import numpy as np


class Voxel(object):
    """
    描画されるボクセルデータ・モデルクラス
    """
    def __init__(self, np_array, n_div):
        assert isinstance(np_array, np.ndarray)

        self.active_coordinates = np_array
        self.n_div = n_div
