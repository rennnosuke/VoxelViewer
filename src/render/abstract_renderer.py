#!/usr/bin/env python
# coding: utf-8

"""

abstract_renderer.py

描画可能オブジェクトのインタフェース定義

"""

import abc


class AbstractRenderer(object):
    """
    描画可能オブジェクトインタフェース
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def render(self):
        pass

    @abc.abstractmethod
    def set_color(self, color):
        pass
