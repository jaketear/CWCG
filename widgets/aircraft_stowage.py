# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtGui import QPainter, QPaintEvent, QPainterPath, QBrush, QPen, QFont
from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QVBoxLayout, QLabel, QSpacerItem,
                             QSizePolicy, QSlider, QDoubleSpinBox, QAbstractSpinBox, QTableWidget)

from data_models import data_collector
import turtle as t
import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QFrame, QApplication)
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import *
# from qtpy import QtCore


class AircraftStowageSketch(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.col = QColor(255, 255, 255)
        self.label = QLabel("hello", self)
        self.label.move(10, 50)
        self.frame_list=["FR22","FR23","FR24","FR25","FR26","FR27","FR28","FR29","FR30","FR31","FR32","FR33","FR34","FR35","FR36",
                         "FR37","FR38","FR39","FR40","FR41","FR42","FR43","FR44","FR45","FR46","FR47","FR48","FR49","FR50","FR51",
                         "FR52","FR53","FR54","FR55","FR56","FR57","FR58","FR59","FR60","FR61","FR62","FR63","FR64","FR65","FR66"]
        self.brush_dic={'FR22':300,'FR23':330,'FR24':360,'FR25':390,'FR26':420,'FR27':450,'FR28':480,'FR29':510,'FR30':540}
        self.aircraft_frame=0
        self.stowage_weight=0
        self.brush_rec_x = 0
        self.flag=False
        self.brush_list=[]
        # self.square1 = QFrame(self)
        # self.square1.setGeometry(150, 100, 40, 40)
        # self.square2 = QFrame(self)
        # self.square2.setGeometry(280, 100, 40, 40)
        # self.square1.setStyleSheet("QWidget { background-color: %s }" %
        #                           self.col.name())
        # self.square2.setStyleSheet("QWidget { background-color: %s }" %
        #                           self.col.name())
        self.show()


    def getDialogSignal(self, stowage_dic):
        self.aircraft_frame=list(stowage_dic.keys())[0]
        self.stowage_weight=list(stowage_dic.values())[0]

        self.brush_rec_x=self.brush_dic[self.aircraft_frame]
        self.brush_list.append(self.brush_rec_x)
        self.flag=True
        self.update()
        print(self.brush_list)
        # self.label.setText(connect)
        # if connect=='FR22':
        #     self.col.setRed(0)
        #     self.square1.setStyleSheet("QFrame { background-color: %s }" %self.col.name())
        # if connect=='FR23':
        #     self.col.setRed(0)
        #     self.square2.setStyleSheet("QFrame { background-color: %s }" %self.col.name())


    def paintEvent(self, event):

        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing)
        self.drawBezierCurve(qp)
        self.drawRectangles(qp)
        if self.flag:
            self.drawBrushes(qp,self.brush_list)
        self.drawLines(qp)
        self.drawText(event, qp)

        qp.end()

    def drawRectangles(self, qp):

        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')
        qp.setPen(col)
        qp.setBrush(QColor(255, 255, 255))

        for i in range(0, 16):
            qp.drawRect(300+i*30, 160, 20, 20)
        qp.drawRect(790, 160, 20, 20)
        qp.drawRect(830, 160, 20, 20)
        for i in range(0, 23):
            qp.drawRect(870+i*30, 160, 20, 20)

        qp.drawRect(195, 140, 45, 80) #前登机门
        qp.drawRect(415, 220, 105, 60) #前货舱
        qp.drawRect(1135, 220, 105, 60) #后货舱
        qp.drawRect(415, 220, 105, 60)  # 前登机门
        #后登机门

    def drawBrushes(self, qp,k):

        brush = QBrush(Qt.SolidPattern)
        qp.setBrush(brush)

        for i in range(0,len(k)):
            qp.drawRect(k[i], 160, 20, 20)


    def drawLines(self, qp):
        pen = QPen(Qt.black, 2, Qt.SolidLine)

        pen.setStyle(Qt.CustomDashLine)
        pen.setDashPattern([1, 4, 5, 4])
        qp.setPen(pen)
        for i in range(0,17):
            qp.drawLine(295+i*30, 80, 295+i*30, 310)
        qp.drawLine(785, 80, 785, 310)
        qp.drawLine(815, 80, 815, 310)
        qp.drawLine(825, 80, 825, 310)
        qp.drawLine(855, 80, 855, 310)
        for i in range(0,24):
            qp.drawLine(865+i*30, 80, 865+i*30, 310)


    def drawText(self, event, qp):

        qp.setPen(QColor(0,0,0))
        qp.setFont(QFont('黑体', 10))

        qp.drawText(440, 255, "前货舱")
        qp.drawText(1160, 255, "后货舱")

        qp.rotate(90)
        for i in range(0,16):
            qp.drawText(35,-290-i*30,self.frame_list[i])
        qp.drawText(35, -770 + 3, self.frame_list[16])
        qp.drawText(35, -770 - 12, self.frame_list[17])

        qp.drawText(35, -810 + 3, self.frame_list[18])
        qp.drawText(35, -810 - 12, self.frame_list[19])

        qp.drawText(35, -850 + 3, self.frame_list[20])
        qp.drawText(35, -850 - 12, self.frame_list[21])
        for i in range(20,43):
            qp.drawText(35,-290-i*30,self.frame_list[i+2])

        # qp.drawText(55, , self.frame_list[18])

    def drawBezierCurve(self, qp):

        path = QPainterPath()
        #绘制飞机外形
        path.moveTo(17, 230)
        path.cubicTo(17, 230, 42, 206, 99, 169)
        path.moveTo(99, 169)
        path.cubicTo(99, 169, 173, 124, 244, 126)
        path.lineTo(1330, 126)
        path.cubicTo(1330, 126, 1528, 135, 1623, 159)
        path.cubicTo(1623, 159, 1650, 185, 1623, 213) #尾部
        path.cubicTo(1623, 213,1357, 283,1126, 300)
        path.cubicTo(1126, 300,733, 312,216, 305)
        path.moveTo(20,264)
        path.cubicTo(20,264,42,282,99,295)
        path.cubicTo(99,295,150,304,216,305)
        path.moveTo(17, 230)
        path.cubicTo(17, 230, 10, 248, 20, 264)
        #huizhi fadongji

        #绘制机头划分区域
        path.moveTo(41, 209)
        path.lineTo(53, 228)
        path.lineTo(53, 281)

        #绘制窗户1
        path.moveTo(57.5, 197)
        path.lineTo(104, 197)
        path.lineTo(134, 167)
        path.lineTo(103, 167)
        # 绘制窗户2
        path.moveTo(144, 167)
        path.cubicTo(144, 167, 160, 170, 170, 167)
        path.moveTo(144, 167)
        path.lineTo(115, 198)
        path.moveTo(170, 167)
        path.lineTo(180, 199)
        path.moveTo(115, 198)
        path.cubicTo(115, 198, 140, 205, 180, 199)
        #绘制发动机


        qp.drawPath(path)


class AircraftStowageControl(QFrame):
    # signal_fuel_change = pyqtSignal(float, float, float)
    #自定义信号传递参数为字典
    mySignal = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        # self.itemChanged.connect(self.update)

        # self.resize(319, 424)
        layout = QHBoxLayout()
        self.TableWidget=QTableWidget(10,2)
        self.TableWidget.setHorizontalHeaderLabels([ '框位','配载重量' ])

        frame_list=['FR22','FR23','FR24','FR25','FR26','FR27','FR28','FR29','FR30','FR31']

        for i in range(0,10):
            newItem = QTableWidgetItem(frame_list[i])
            newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.TableWidget.setItem(i, 0, newItem)
            newItem.setFlags(Qt.ItemIsEnabled)

        newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.TableWidget.setItem(3, 0, newItem)
        self.TableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        layout.addWidget(self.TableWidget)
        # self.TableWidget.cellClicked.connect(self.sendEditContent)
        self.TableWidget.cellChanged.connect(self.sendEditContent) #表格内容发生变化
        self.setLayout(layout)



    def sendEditContent(self,row,colum):

        aircraft_frame = self.TableWidget.item(row, colum-1).text()
        stowage_weight = self.TableWidget.item(row, colum).text()
        stowage_dic = {aircraft_frame:int(stowage_weight)}
        self.mySignal.emit(stowage_dic)  # 发射信号

class AircraftStowageWidget(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.h_layout = QHBoxLayout(self)
        self.fuel_tank_sketch = AircraftStowageSketch()
        self.h_layout.addWidget(self.fuel_tank_sketch)
        self.fuel_tank_control = AircraftStowageControl()
        self.h_layout.addWidget(self.fuel_tank_control)
        self.h_layout.setStretch(0, 7)
        self.h_layout.setStretch(1, 1)

        #发送信号
        dic={}
        self.fuel_tank_control.mySignal.connect(self.fuel_tank_sketch.getDialogSignal) ##暂时注释


        # self.update_fuel_initial_status()

##水配重类 许鑫 2021-3-28日
class WaterCounterweightSketch(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.col = QColor(255, 255, 255)
        self.label = QLabel("hello", self)
        self.label.move(10, 50)
        self.width = self.width()
        self.height = self.height()

        self.water_tank1 = QLineEdit(self)
        self.water_tank1.move(60, 100)


        self.water_tank1.textChanged[str].connect(self.onChanged)

        self.show()


    def onChange(self, text):
        pass


    def paintEvent(self, event):

        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing)
        self.drawBezierCurve(qp)
        self.drawRectangles(qp)
        # if self.flag:
        #     self.drawBrushes(qp,self.brush_list)
        # self.drawLines(qp)
        # self.drawText(event, qp)

        qp.end()

    def drawRectangles(self, qp):

        pass
        #后登机门

    def drawBrushes(self, qp,k):

        pass


    def drawLines(self, qp):

        pass


    def drawText(self, event, qp):

        pass

    def drawBezierCurve(self, qp):

        path = QPainterPath()

        begin_y=self.height/2-50
        #水箱1
        for i in range(0,8):
            begin_x = 77+i*150
            path.moveTo(begin_x,begin_y)
            path.cubicTo(begin_x, begin_y, begin_x-22, begin_y-40, begin_x, begin_y-80)
            path.lineTo(begin_x+100, begin_y-80)
            path.cubicTo(begin_x+100, begin_y-80, begin_x+120, begin_y - 40, begin_x+100, begin_y)
            path.lineTo(begin_x,begin_y)

        for i in range(0,8):
            begin_x = 77+i*150
            begin_y = self.height-150
            path.moveTo(begin_x,begin_y)
            path.cubicTo(begin_x, begin_y, begin_x-22, begin_y-40, begin_x, begin_y-80)
            path.lineTo(begin_x+100, begin_y-80)
            path.cubicTo(begin_x+100, begin_y-80, begin_x+120, begin_y - 40, begin_x+100, begin_y)
            path.lineTo(begin_x,begin_y)
        # path.lineTo(134, 167)
        # path.lineTo(103, 167)
        # 绘制窗户2

        #绘制发动机


        qp.drawPath(path)