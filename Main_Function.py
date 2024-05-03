# -*- encoding:utf-8 -*-

from Main_Window import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import json
import os
import subprocess
import re
import webbrowser
import tools.GitHubTools


class fun_main(QtWidgets.QMainWindow, Ui_MainWindow):
    setting = ""
    global repo
    repo = "zrydnoob/Ori-Archive-Manager"
    def __init__(self):
        super(fun_main, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setupUi(self)
        self.listWidget.itemClicked.connect(self.switchPages)
        self.setting()
        self.findGameSave()
        self.findLocalSaves()

        self.pushButton_21.clicked.connect(self.selectGameSavePath)
        self.pushButton_23.clicked.connect(self.selectLocalSavePath)

        self.pushButton_22.clicked.connect(self.openGameSavePath)
        self.pushButton_24.clicked.connect(self.openLocalSavePath)

        self.pushButton_8.clicked.connect(self.refresh)

        self.pushButton_9.clicked.connect(self.openGithub)

        self.buttonGroup.buttonClicked.connect(self.nameToInfo)
        try:
            self.label_22.setText(tools.GitHubTools.getLastCommit(repo)['sha'][0:7])
        except:
            self.label_22.setText("无法获取")


        # 存档操作按钮时间绑定
        self.pushButton_6.clicked.connect(self.copyToLocal)
        self.pushButton_7.clicked.connect(self.moveToLocal)

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

# 路径设置
    def setting(self):
        try:
            f = open('setting.json','r')
            content = f.read()
            global settingJson
            settingJson = json.loads(content)
            self.label_11.setText(settingJson["gameSavePath"])
            self.label_13.setText(settingJson["localSavePath"])
        except FileNotFoundError:
            a = {
                "gameSavePath":"",
                "localSavePath":""
            }
            with open("setting.json",'w',encoding='utf-8') as w:
                json.dump(a,w,ensure_ascii=False)

# 选择游戏存档目录
    def selectGameSavePath(self):
        dir_path = QFileDialog.getExistingDirectory(self, "选择目录", "F:/", QFileDialog.ShowDirsOnly)
        if dir_path:
            print("选择的目录路径：", dir_path)
            # 读取JSON文件
            with open("setting.json", "r") as file:
                data = json.load(file)

            # 修改JSON数据
            data["gameSavePath"] = dir_path

            # 将修改后的数据写回文件中
            with open("setting.json", "w") as file:
                json.dump(data, file, indent=4)
            self.setting()

    # 打开Github仓库
    def openGithub(self):
        webbrowser.open("https://github.com/zrydnoob/Ori-Archive-Manager")

        pass
# 选择本地存档目录
    def selectLocalSavePath(self):
        dir_path = QFileDialog.getExistingDirectory(self, "选择目录", "F:/", QFileDialog.ShowDirsOnly)
        if dir_path:
            print("选择的目录路径：", dir_path)
            # 读取JSON文件
            with open("setting.json", "r") as file:
                data = json.load(file)

            # 修改JSON数据
            data["localSavePath"] = dir_path

            # 将修改后的数据写回文件中
            with open("setting.json", "w") as file:
                json.dump(data, file, indent=4)
            self.setting()

    def openGameSavePath(self):
        os.startfile(settingJson["gameSavePath"])

    def openLocalSavePath(self):
        os.startfile(settingJson["localSavePath"])

    def findGameSave(self):
        saveList_HB = os.listdir(settingJson["gameSavePath"])

        saveList = [s for s in saveList_HB if 'saveFile' in s and 'bkup' not in s]
        child_widgets = self.frame_9.findChildren(QRadioButton)
        for i in range(0,len(saveList)):
            child_widgets[i].setProperty("saveName",saveList[i])
            print(child_widgets[i].property("saveName"))
    
    def nameToInfo(self):
        try:
            savePath = settingJson["gameSavePath"] + "/" + str(self.buttonGroup.button(self.buttonGroup.checkedId()).property("saveName"))
            print(savePath)

            with open(savePath, "r", encoding='gbk',errors="ignore") as f:
                saveData = [line.strip() for line in f]
            areaName = saveData[0]
            self.label_17.setText(re.sub(r"[\W]", "", areaName)[7:])
        except:
            self.label_17.setText("所在区域")

    def findLocalSaves(self):
        saveList_BD = os.listdir(settingJson["localSavePath"])
        print(saveList_BD)
        self.listWidget_2.clear()
        for i in range(0,len(saveList_BD)):
            item = QtWidgets.QListWidgetItem()
            self.listWidget_2.addItem(item)
            item = self.listWidget_2.item(i)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/Placeholding/Placeholding/10972.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            item.setIcon(icon)
            item.setText(saveList_BD[i])

    def refresh(self):
        self.findLocalSaves()
        self.findGameSave()

    def copyToLocal(self):
        try:
            savePath = settingJson["gameSavePath"] + "/" + str(self.buttonGroup.button(self.buttonGroup.checkedId()).property("saveName"))
            copyToPath = settingJson["localSavePath"] + "/" + str(self.buttonGroup.button(self.buttonGroup.checkedId()).property("saveName"))
            self.copyFile(savePath,copyToPath)
        except:
            pass
        self.refresh()


    def moveToLocal(self):
        try:
            savePath = settingJson["gameSavePath"] + "/" + str(self.buttonGroup.button(self.buttonGroup.checkedId()).property("saveName"))
            moveToPath = settingJson["localSavePath"] + "/" + str(self.buttonGroup.button(self.buttonGroup.checkedId()).property("saveName"))
            self.moveFile(savePath,moveToPath)
        except:
            pass
        self.refresh()

    def copyFile(self,fr:str,to:str):
        with open(fr, "r") as source_file:  
            with open(to, "w") as target_file:
                for line in source_file.readlines():
                    target_file.write(line)

    def moveFile(self,source_path:str, destination_path:str):
        self.copyFile(source_path,destination_path)
        os.remove(source_path)
