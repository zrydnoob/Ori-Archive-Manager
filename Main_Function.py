# -*- encoding:utf-8 -*-

from Main_Window import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor,QEnterEvent


class fun_main(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(fun_main, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setupUi(self)
        self.listWidget.itemClicked.connect(self.switchPages)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.draggable = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.draggable:
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.draggable = False

    def switchPages(self,item):
        self.stackedWidget.setCurrentIndex(self.listWidget.currentRow()+1)