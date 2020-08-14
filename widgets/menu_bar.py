# -*- coding: utf-8 -*-

import math

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import (QPainter, QPaintEvent, QPainterPath, QFont,
                         QMouseEvent)
from PyQt5.QtWidgets import QFrame


class MenuBar(QFrame):
    def __init__(self, parent=None, menu_items: list = None, height: int = 32,
                 arrow_angle: int = 60, arrow_space: int = 6, font_margin: int = 2):
        super().__init__(parent)

        self.setMaximumHeight(height)
        self.setMinimumHeight(height)

        # 菜单栏的各项目名称
        # self.menu_items_list = menu_items
        self.menu_items_list = ['动作', '动作', '动作']

        # 箭头的角度属性
        self.arrow_angle = arrow_angle
        # 箭头的个数
        self.arrow_count = len(self.menu_items_list)
        # 箭头之间的间距
        self.arrow_space = arrow_space
        # 箭头的路径
        self.arrows_path = list()

        # 文字距离边界距离
        self.font_margin = font_margin

        # 当前选择的项目
        self.current_select_index = -1

    # 计算箭头轮廓
    def cal_arrows_patch(self, hei, arrow_wid, delta_wid):
        self.arrows_path = list()

        for i in range(self.arrow_count):
            if i == 0:
                chara_point_one = (0.0, 0.0)
                chara_point_two = (arrow_wid, 0.0)
                chara_point_three = (arrow_wid + delta_wid, hei / 2)
                chara_point_four = (arrow_wid, hei)
                chara_point_five = (0, hei)
                arrow_path = QPainterPath()
                arrow_path.moveTo(*chara_point_one)
                arrow_path.lineTo(*chara_point_two)
                arrow_path.lineTo(*chara_point_three)
                arrow_path.lineTo(*chara_point_four)
                arrow_path.lineTo(*chara_point_five)
                arrow_path.lineTo(*chara_point_one)
                arrow_path.closeSubpath()
                self.arrows_path.append(arrow_path)
            else:
                chara_point_one = (arrow_wid * i + self.arrow_space * i, 0.0)
                chara_point_two = (arrow_wid * (i + 1) + self.arrow_space * i, 0.0)
                chara_point_three = (arrow_wid * (i + 1) + self.arrow_space * i + delta_wid, hei / 2)
                chara_point_four = (arrow_wid * (i + 1) + self.arrow_space * i, hei)
                chara_point_five = (arrow_wid * i + self.arrow_space * i, hei)
                chara_point_six = (arrow_wid * i + self.arrow_space * i + delta_wid, hei / 2)
                arrow_path = QPainterPath()
                arrow_path.moveTo(*chara_point_one)
                arrow_path.lineTo(*chara_point_two)
                arrow_path.lineTo(*chara_point_three)
                arrow_path.lineTo(*chara_point_four)
                arrow_path.lineTo(*chara_point_five)
                arrow_path.lineTo(*chara_point_six)
                arrow_path.lineTo(*chara_point_one)
                arrow_path.closeSubpath()
                self.arrows_path.append(arrow_path)

    # 重写鼠标单击事件
    def mousePressEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton:
            for i, ap in enumerate(self.arrows_path):
                if ap.contains(event.localPos()):
                    self.current_select_index = i
                    self.update()
                    break
            event.accept()
        event.ignore()

    # 重写绘图函数
    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.gray)

        # 计算特征参数
        wid = self.width()
        hei = self.height()
        delta_wid = int(hei / 2 * math.tan(self.arrow_angle * math.pi / 180))
        arrow_wid = int((wid - delta_wid - self.arrow_space * (self.arrow_count - 1)) / self.arrow_count)

        # 绘制箭头
        self.cal_arrows_patch(hei, arrow_wid, delta_wid)
        for i, ap in enumerate(self.arrows_path):
            if i == self.current_select_index:
                painter.setBrush(Qt.yellow)
                painter.drawPath(ap)
                painter.setBrush(Qt.gray)
            else:
                painter.drawPath(ap)
        painter.setPen(Qt.white)
        font = QFont()
        font.setFamily('微软雅黑')
        font.setPixelSize(hei - 4)
        painter.setFont(font)
        # 增加文字
        for i, text in enumerate(self.menu_items_list):
            pos_x = delta_wid + (arrow_wid + self.arrow_space) * i
            pos_y = self.font_margin
            t_wid = arrow_wid - delta_wid
            t_hei = hei - self.font_margin * 2
            # painter.drawRect(QRect(pos_x, pos_y, t_wid, t_hei))
            painter.drawText(QRect(pos_x, pos_y, t_wid, t_hei), Qt.AlignCenter,
                             text)
