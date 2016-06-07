#!/usr/bin/env python
# coding: utf-8

import sys

from PyQt4 import QtGui

from src.view.window.main_window import MainWindow

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow('viewer')
    window.show()
    sys.exit(app.exec_())
