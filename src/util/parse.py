#!/usr/bin/env python
# coding: utf-8

import struct
import numpy as np


def parse_binvox(binvox_file, show_params=False):
    """
    .binvoxファイルを読み込み、3Dボクセル配列を返す
    :param binvox_file: PATH含むファイル名
    :return: 3Dボクセル配列
    """

    with open(binvox_file, mode='rb') as f:

        # binvox 1
        binvox = f.readline().strip()

        # 分割数
        dim = tuple(map(int, f.readline().strip().split()[1:]))

        # 標準化の際の平行移動
        trans = tuple(map(float, f.readline().strip().split()[1:]))

        # 標準化の際のスケール
        scale = float(f.readline().strip().split()[1])

        # data（バイナリスタート）
        data = f.readline()

        if show_params:
            print binvox
            print dim
            print trans
            print scale
            print data

        # ボクセル配列
        array = np.zeros(shape=(dim[0] * dim[1] * dim[2]), dtype=np.uint8)

        # 先頭Index
        head = 0

        while True:
            # 2バイトずつ取り出し
            binaly = f.read(1)
            num = f.read(1)

            # ファイル終端であれば終了
            if binaly == '':
                break

            # 0 or 1
            bin_uc = struct.unpack('B', binaly)[0]
            # bin_ucの連続数
            n_uc = struct.unpack('B', num)[0]

            # 元々0埋めの配列なので、bin_uc==1の時だけ代入
            if bin_uc == 1:
                array[head:head + n_uc] = 1

            # 次の値格納のために、headをn_ucずらす
            head += n_uc

    # 3Dにして返戻
    return array.reshape(dim)
