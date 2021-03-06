# -*- coding: utf-8 -*-

import math

from PyQt5.QtCore import Qt, QRect, pyqtSignal
from PyQt5.QtGui import (QPainter, QPaintEvent, QPainterPath, QFont,
                         QMouseEvent, QBrush, QColor)
from PyQt5.QtWidgets import QFrame


class MenuBar(QFrame):
    signal_selected_item_change = pyqtSignal(int)

    def __init__(self, parent=None, height: int = 40, arrow_angle: int = 60,
                 arrow_space: int = 12, font_margin: int = 6):
        super().__init__(parent)

        self.setMaximumHeight(height)
        self.setMinimumHeight(height)

        # 菜单栏的各项目名称
        # self.menu_items_list = menu_items
        self.menu_items_list = ['机型', '称重', '配载', '项目', '燃油', '报告']

        # 箭头的角度属性
        self.arrow_angle = arrow_angle
        # 箭头的个数
        self.arrow_count = len(self.menu_items_list)
        # 箭头之间的间距
        self.arrow_space = arrow_space
        # 箭头的路径
        self.arrows_path = list()

        # 箭头选中的颜色
        self.selected_brush = QBrush(QColor('#3F51B5'))
        # self.un_selected_brush = Qt.gray
        self.un_selected_brush = QBrush(QColor('#9FA8DA'))

        # 文字距离边界距离
        self.font_margin = font_margin

        # 当前选择的项目
        self.current_select_index = 0

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
                    self.signal_selected_item_change.emit(self.current_select_index)
                    self.update()
                    break
            event.accept()
        event.ignore()

    # 重写绘图函数
    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.un_selected_brush)

        # 计算特征参数
        wid = self.width()
        hei = self.height()
        delta_wid = int(hei / 2 * math.tan(self.arrow_angle * math.pi / 180))
        arrow_wid = int((wid - delta_wid - self.arrow_space * (self.arrow_count - 1)) / self.arrow_count)

        # 绘制箭头
        self.cal_arrows_patch(hei, arrow_wid, delta_wid)
        for i, ap in enumerate(self.arrows_path):
            if i == self.current_select_index:
                painter.setBrush(self.selected_brush)
                painter.drawPath(ap)
                painter.setBrush(self.un_selected_brush)
            else:
                painter.drawPath(ap)
        painter.setPen(Qt.white)
        font = QFont()
        font.setFamily('微软雅黑')
        font.setBold(True)
        font.setPixelSize(hei - self.font_margin * 2 - 2)
        painter.setFont(font)
        # 增加文字
        for i, text in enumerate(self.menu_items_list):
            pos_x = delta_wid + (arrow_wid + self.arrow_space) * i
            pos_y = self.font_margin
            t_wid = arrow_wid - delta_wid
            t_hei = hei - self.font_margin * 2 - 2
            # painter.drawRect(QRect(pos_x, pos_y, t_wid, t_hei))
            painter.drawText(QRect(pos_x, pos_y, t_wid, t_hei), Qt.AlignCenter,
                             text)
