#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''  
---------------------------------------
 # @Project    : 随机生成序列号
 # @File       : main.py
 # @Author     : GrayZhao
 # @Date       : 2021/10/17 16:38
 # @Version    : 
 # @Desciption : 
---------------------------------------
'''
import sys
from PySide2.QtWidgets import QApplication
from view import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    stats = MainWindow()
    stats.ui.show()
    sys.exit(app.exec_())