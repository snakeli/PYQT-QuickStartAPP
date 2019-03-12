"""
Pyqt5 practice.
For quick starting files.

Created by Junjun.Li
"""

#!/usr/bin/env python
# -*- coding:utf-8 -*-
import configparser
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

import win32api

class myconf(configparser.ConfigParser):
    def __init__(self,defaults=None):
        configparser.ConfigParser.__init__(self,defaults=None)
    def optionxform(self, optionstr):
        return optionstr



class DealCFG():
    def __init__(self):
        self.app_dict = {}
        self.config = myconf()

    def read_cfg(self):
        self.config.read("AppQuickStart.cfg")
        print(self.config.sections())
        try:
            for app_name in self.config.options("APP"):
                print(app_name)
                self.app_dict[app_name] = self.config.get("APP", app_name)
        except configparser.NoSectionError:
            print("Can't find the section named DEFAULT")

        return self.app_dict

    def write_cfg(self, app_name, app_path):
        self.config.set("APP", app_name, app_path)
        with open("AppQuickStart.cfg", "w")as config_file:
            self.config.write(config_file)

    def delete_cfg(self, app_name):
        self.config.remove_option("APP", app_name)
        with open("AppQuickStart.cfg", "w")as config_file:
            self.config.write(config_file)


class StartWindow(QWidget):
    def __init__(self, parent=None):
        super(StartWindow, self).__init__(parent)
        self.setWindowTitle("Quick Start")

        self.deal_cfg = DealCFG()
        self.app_dict = self.deal_cfg.read_cfg()
        print(self.app_dict)

        self.groups = {}
        self.pathLineEdit = {}
        self.group_num = 1
        self.create_app()

        self.mainLayout = QGridLayout()
        self.mainLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.addWidget(self.line_edit, 1, 0)
        self.mainLayout.addWidget(self.edit_button, 1, 1)

        for app_name in self.app_dict.keys():
            print(app_name)
            self.CreateGroup(app_name, self.app_dict[app_name])
            self.mainLayout.addWidget(self.top_group, self.group_num, 0, 1, 2)

        self.mainLayout.setRowStretch(1, 1)
        self.mainLayout.setColumnStretch(0, 1)
        self.setLayout(self.mainLayout)

        self.setStyleSheet("QLabel{color:rgb(100,100,100,250);font-size:13px;font-weight:bold;font-family:Roman times;}")
        self.setWindowIcon(QIcon("Icon.ico"))
        self.resize(500, 200)

    def create_app(self):
        self.line_edit = QLineEdit()
        self.edit_button = QPushButton("Add")
        self.edit_button.clicked.connect(self.addAPP)

    def CreateGroup(self, group_name, _path="Click Change Path button to add app"):
        self.top_group = QGroupBox(group_name)
        
        self.groups[group_name] = {}
        self.groups[group_name]["StartButton"] = QPushButton("Start")
        self.groups[group_name]["DeleteButton"] = QPushButton("Delete")
        self.groups[group_name]["ChangePathButton"] = QPushButton("Change Path")
        self.groups[group_name]["PathLineEdit"] = QLabel()

        layout = QGridLayout()
        layout.setAlignment(Qt.AlignBaseline)
        layout.addWidget(self.groups[group_name]["StartButton"], 0, 0)
        layout.addWidget(self.groups[group_name]["DeleteButton"], 0, 1)
        layout.addWidget(self.groups[group_name]["ChangePathButton"], 0, 2)
        layout.addWidget(self.groups[group_name]["PathLineEdit"], 1, 0, 1, 5)

        self.groups[group_name]["StartButton"].setFixedSize(100, 25)
        self.groups[group_name]["DeleteButton"].setFixedSize(100, 25)
        self.groups[group_name]["ChangePathButton"].setFixedSize(100, 25)
        self.groups[group_name]["PathLineEdit"].setText(_path)

        self.groups[group_name]["ChangePathButton"].clicked.connect(lambda: self.changePath(group_name))
        self.groups[group_name]["StartButton"].clicked.connect(lambda: self.startAPP(group_name))
        self.groups[group_name]["DeleteButton"].clicked.connect(lambda: self.deleteAPP(group_name))

        self.top_group.setLayout(layout)

        self.groups[group_name]["top_group"] = self.top_group

        self.group_num += 1

    def changePath(self, group_name):
        open_dialog = QFileDialog()
        _path = open_dialog.getOpenFileName()
        self.groups[group_name]["PathLineEdit"].setText(_path[0])
        self.app_dict[group_name] = _path[0]
        self.deal_cfg.write_cfg(group_name, _path[0])

    def startAPP(self, group_name):
        app_path = self.groups[group_name]["PathLineEdit"].text()
        print(app_path)
        try:
            win32api.ShellExecute(0, 'open', app_path, '', '', 1)
        except Exception as error:
            print(error)
            QMessageBox.information(self, "ERROR", "Can't open the APP, Check its path! ", QMessageBox.Ok)

    def deleteAPP(self, group_name):
        self.groups[group_name]["top_group"].setParent(None)
        self.mainLayout.removeWidget(self.groups[group_name]["top_group"])
        self.deal_cfg.delete_cfg(group_name)
        self.groups.pop(group_name)

    def addAPP(self):
        new_app_text = self.line_edit.text()
        if new_app_text.strip() == "":
            QMessageBox.information(self, "ERROR", "Please enter APP name firstly!", QMessageBox.Ok)
            print("Please enter APP name firstly!")
            return

        if new_app_text in self.app_dict:
            QMessageBox.information(self, "ERROR", "The APP already in the list!", QMessageBox.Ok)
            print("The APP already in the list!")
            return

        self.CreateGroup(new_app_text)
        self.mainLayout.addWidget(self.top_group, self.group_num, 0)

        self.app_dict[new_app_text] = ""
        self.deal_cfg.write_cfg(new_app_text, "")


if __name__ == "__main__":
    APP = QApplication(sys.argv)
    APP.setStyle("Fusion")

    APP.setStyleSheet('''
                        QPushButton{font: bold 12px; min-width: 10em;}
                        QGroupBox{font: bold 16px;}
                    ''')

    WIN = StartWindow()
    WIN.show()
    sys.exit(APP.exec_())
