#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
import sys
import json
import base64
import requests
import serial
import PySide2.QtWidgets
from PySide2.QtGui import QPixmap
import os
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QApplication,QMainWindow,QPushButton,QPlainTextEdit,QTabWidget,QWidget,QDialog,QLineEdit,QLabel
import time
from PySide2 import *
import datetime
import cv2

trans = {
        '30': '0',
        '31': '1',
        '32': '2',
        '33': '3',
        '34': '4',
        '35': '5',
        '36': '6',
        '37': '7',
        '38': '8',
        '39': '9',
        'b0': '0',
        'b1': '1',
        'b2': '2',
        'b3': '3',
        'b4': '4',
        'b5': '5',
        'b6': '6',
        'b7': '7',
        'b8': '8',
        'b9': '9',
        'c1': 'a',
        'c2': 'b',
        'c3': 'c',
        'c4': 'd',
        'c5': 'e',
        'c6': 'f',
        '41': 'a',
        '42': 'b',
        '43': 'c',
        '44': 'd',
        '45': 'e',
        '46': 'f'

    }
class MainWindow(QtWidgets.QMainWindow):
    def read_out_Status(self,txt):
        lib = {'3a30b130b130b13030c6448d0a': [0, 0, 0, 0],
               '3a30b130b130b130b1c6c38d0a': [1, 0, 0, 0],
               '3a30b130b130b130b2c6428d0a': [0, 1, 0, 0],
               '3a30b130b130b130b4c6398d0a': [0, 0, 1, 0],
               '3a30b130b130b130b8c6358d0a': [0, 0, 0, 1],
               '3a30b130b130b13033c6418d0a': [1, 1, 0, 0],
               '3a30b130b130b13035c6b88d0a': [1, 0, 1, 0],
               '3a30b130b130b13039c6b48d0a': [1, 0, 0, 1],
               '3a30b130b130b13036c6b78d0a': [0, 1, 1, 0],
               '3a30b130b130b13041c6338d0a': [0, 1, 0, 1],
               '3a30b130b130b130c3c6b18d0a': [0, 0, 1, 1],
               '3a30b130b130b130b7c6368d0a': [1, 1, 1, 0],
               '3a30b130b130b13042c6b28d0a': [1, 1, 0, 1],
               '3a30b130b130b13044c6308d0a': [1, 0, 1, 1],
               '3a30b130b130b130c5c5c68d0a': [0, 1, 1, 1],
               '3a30b130b130b130c6c5c58d0a': [1, 1, 1, 1],
               }

        if lib.get(txt) != None:
            return lib.get(txt)
        else:
            return False

    def PLC_send(self,txt):
        # txt=input_txt1.text()
        # todo:端口修改
        port = "com4"

        try:
            ser = serial.Serial(port, 9600)  # 选择串口，并设置波特率
            if ser.is_open:
                # print("port open success")
                # hex(16进制)转换为bytes(2进制)，应注意Python3.7与Python2.7此处转换的不同
                # 开始符3A  从站地址3031 指令符3030 地址3035 3030 位数3030 3031 lrc校验4630 结束字符0D0A
                send_data = bytes.fromhex(txt)  # 发送数据转换为b'\xff\x01\x00U\x00\x00V'
                ser.write(send_data)  # 发送命令
                time.sleep(0.5)  # 延时，否则len_return_data将返回0！！！
                len_return_data = ser.inWaiting()  # 获取缓冲数据（接收数据）长度
                if len_return_data:
                    return_data = ser.read(len_return_data)  # 读取缓冲数据
                    # bytes(2进制)转换为hex(16进制)，应注意Python3.7与Python2.7此处转换的不同，并转为字符串后截取所需数据字段，再转为10进制
                    str_return_data = str(return_data.hex())
                    # feedback_data = int(str_return_data[-6:-2], 16)
                    print(str_return_data)
                    return str_return_data
                else:
                    return "端口({})指令执行错误！！！".format(port)
        except:
            return "端口({})指令执行错误！！！".format(port)

    def set_txt(self):
        info = self.get_info()
        self.textEdit1.setText('湿度：' + str(info[0]) + "%")
        self.textEdit2.setText('温度：' + str(info[1]) + "℃")

    def load_xlsx(self):
        path = r'C:\Users\Endymion\Desktop\myapp\data.xlsx'
        os.startfile(path)

    def update_xlsx(self):
        self.up_date()
        self.textEdit3.setText("获取传感器数据成功")

    def open_data_xlsx(self):
        os.system(r"start explorer C:\Users\Endymion\Desktop\myapp\data.xlsx")

    def func(self):
        print('do func!')
        self.input_txt16.setText('do func success!!!'
                                 f'{self.wuliao1.text()}'
                                 f'{self.wuliao2.text()}'
                                 f'{self.wuliao3.text()}'
                                 f'{self.wuliao4.text()}'
                                 f'{self.wuliao5.text()}')
        pass


    def  __init__(self):
        super(MainWindow, self).__init__()
        self.img1 = 'img/img1.png'

        self.resize(750, 550)
        self.move(900, 550)
        self.setWindowTitle('PLC控制系统V1.00')

        self.Dialog1 = QDialog()
        self.Dialog2 = QDialog()
        # Dialog3 = QDialog()

        self.TableWidget = QTabWidget(self)
        self.TableWidget.resize(750, 550)
        self.TableWidget.addTab(self.Dialog1, "物料选择")
        self.TableWidget.addTab(self.Dialog2, "状态监控")
        # TableWidget.addTab(Dialog3, "Tab3")

        '''Tab1'''
        self.input_txt10 = PySide2.QtWidgets.QLabel(self.Dialog1)
        self.input_txt10.setText('请选择物料：')
        self.input_txt10.move(10, 10)
        self.input_txt10.resize(300, 33)

        # pixmap = QPixmap('')
        # self.img1 = QLabel.setPixmap(self.Dialog1)
        # self.img1 = QLabel.setPixmap(QPixmap(self.img1))
        self.place_x =20
        self.place_y = 130

        self.input_txt11 = PySide2.QtWidgets.QLabel(self.Dialog1)
        self.input_txt11.setText('物料1')
        self.input_txt11.move(self.place_x, self.place_y)
        self.input_txt11.resize(300, 30)
        self.wuliao1 = QtWidgets.QLineEdit('0',self.Dialog1)
        self.wuliao1.setAlignment(QtCore.Qt.AlignCenter)
        self.wuliao1.move(self.place_x-10,self.place_y+40)
        self.wuliao1.resize(70, 30)


        self.input_txt12 = PySide2.QtWidgets.QLabel(self.Dialog1)
        self.input_txt12.setText('物料2')
        self.input_txt12.move(self.place_x+100, self.place_y)
        self.input_txt12.resize(300, 30)
        self.wuliao2 = QtWidgets.QLineEdit('0',self.Dialog1)
        self.wuliao2.setAlignment(QtCore.Qt.AlignCenter)
        self.wuliao2.move(self.place_x+85,self.place_y+40)
        self.wuliao2.resize(70, 30)
        
        self.input_txt13 = PySide2.QtWidgets.QLabel(self.Dialog1)
        self.input_txt13.setText('物料3')
        self.input_txt13.move(self.place_x+200, self.place_y)
        self.input_txt13.resize(300, 30)
        self.wuliao3 = QtWidgets.QLineEdit('0',self.Dialog1)
        self.wuliao3.setAlignment(QtCore.Qt.AlignCenter)
        self.wuliao3.move(self.place_x+190,self.place_y+40)
        self.wuliao3.resize(70, 30)
        
        self.input_txt14 = PySide2.QtWidgets.QLabel(self.Dialog1)
        self.input_txt14.setText('物料4')
        self.input_txt14.move(self.place_x+300, self.place_y)
        self.input_txt14.resize(300, 30)
        self.wuliao4 = QtWidgets.QLineEdit('0',self.Dialog1)
        self.wuliao4.setAlignment(QtCore.Qt.AlignCenter)
        self.wuliao4.move(self.place_x+285,self.place_y+40)
        self.wuliao4.resize(70, 30)
        
        self.input_txt15 = PySide2.QtWidgets.QLabel(self.Dialog1)
        self.input_txt15.setText('物料5')
        self.input_txt15.move(self.place_x+400, self.place_y)
        self.input_txt15.resize(300, 30)
        self.wuliao5 = QtWidgets.QLineEdit('0',self.Dialog1)
        self.wuliao5.setAlignment(QtCore.Qt.AlignCenter)
        self.wuliao5.move(self.place_x+380,self.place_y+40)
        self.wuliao5.resize(70, 30)

        self.button10 = QPushButton('下发指令', self.Dialog1)
        self.button10.move(self.place_x-10, self.place_y+100)
        self.button10.clicked.connect(self.func)
        self.input_txt16 = PySide2.QtWidgets.QLineEdit(self.Dialog1)
        self.input_txt16.setText('提示框')
        self.input_txt16.move(self.place_x-10, self.place_y+140)
        self.input_txt16.resize(600, 200)
        self.input_txt16.setReadOnly(True)
        self.input_txt16.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)

        '''Tab2'''
        self.place2_x = 10
        self.place2_y = 20

        self.input_txt21 = PySide2.QtWidgets.QLabel(self.Dialog2)
        self.input_txt21.setText('当前配置信息')
        self.input_txt21.move(self.place2_x, self.place2_y)
        self.input_txt21.resize(300, 30)

        self.button20 = PySide2.QtWidgets.QLabel(self.Dialog2)
        self.button20.setText('获取系统状态')
        self.button20.move(self.place2_x, self.place2_y+160)
        self.button20.resize(300, 30)
        
        
class LoginWidget(QtWidgets.QMainWindow):
    def __init__(self):
        super(LoginWidget, self).__init__()
        # 设定登录页面大小
        self.setWindowTitle('智能大棚控制系统V1.00')
        self.resize(433, 334)
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        # 添加组控件
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(50, 60, 361, 171))
        self.groupBox.setTitle('用户登录')
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(30, 30, 48, 16))
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_3.setText('用户名称')
        self.label_3.resize(100, 30)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(30, 80, 48, 16))
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_4.setText('用户密码')
        self.label_4.resize(100, 30)
        self.lineEdit_1 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_1.setGeometry(QtCore.QRect(120, 30, 200, 20))
        self.lineEdit_1.setMaximumSize(QtCore.QSize(200, 20))
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(120, 80, 200, 20))
        self.lineEdit.setMaximumSize(QtCore.QSize(200, 20))
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(110, 260, 75, 25))
        self.pushButton.setMaximumSize(QtCore.QSize(16777215, 25))
        self.pushButton.setText('确定')
        # 确定按钮绑定回车快捷键
        self.pushButton.setShortcut('Enter')
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(240, 260, 75, 25))
        self.pushButton_2.setMaximumSize(QtCore.QSize(16777215, 25))
        self.pushButton_2.setText('取消')

        # 禁止窗口最大最小化
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        # 禁止拉伸窗口
        self.setFixedSize(self.width(), self.height())
        # 密码隐藏
        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        # 连接信号和槽函数，实现功能：点击取消按钮，退出应用
        self.connect(self.pushButton_2, QtCore.SIGNAL('clicked()'), self.closeWin)
        # 连接信号和函数，实现功能：点击确定按钮，进入主窗口
        self.pushButton.clicked.connect(self.openMain)

    def openMain(self):
        #todo
        if self.lineEdit_1.text() == '1' and self.lineEdit.text() == '1':
            self.mw = MainWindow()
            self.mw.show()
            self.hide()
        else:
            # 密码错误，弹出提示框
            QtWidgets.QMessageBox.information(self, u'提示', u'账户密码错误，请重新输入', QtWidgets.QMessageBox.Ok)
            print('账户密码错误，请重新输入')

    def closeWin(self):
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = LoginWidget()
    gui.show()
    sys.exit(app.exec_())
