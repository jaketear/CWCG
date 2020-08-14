# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPaintEvent, QPainterPath
from PyQt5.QtWidgets import QFrame

import data_collector


class AircraftFuelBankWidget(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        # 油量百分比
        self.center_fuel_bank_weight_per = 0.5
        self.left_fuel_bank_weight_per = 1
        self.right_fuel_bank_weight_per = 1

        # 存储轮廓信息，包括机翼外形，中央翼外形，左翼外形，右翼外形
        self.aircraft_fuel_out_path = None
        self.aircraft_center_fuel_path = None
        self.aircraft_left_fuel_path = None
        self.aircraft_right_fuel_path = None
        # 油箱的矩形数据
        self.aircraft_center_fuel_rect = None
        self.aircraft_left_fuel_rect = None
        self.aircraft_right_fuel_rect = None
        # 记录变形前的控件尺寸
        self.old_width = self.width()
        self.old_height = self.height()

        # self.setStyleSheet('QFrame { background: gray }')
        # 加载油箱外形数据
        data_collector.load_fuel_bank_frame_data_from_excel()
        # 创建油箱外形的轮廓
        self.load_fuel_bank_path()

    # 改变燃油量，百分比
    def change_fuel_weight(self, center, left, right):
        self.center_fuel_bank_weight_per = center
        self.left_fuel_bank_weight_per = left
        self.right_fuel_bank_weight_per = right
        self.update()

    # 创建油箱外形的路径
    def load_fuel_bank_path(self):
        wid, hei = self.normal_transform_ratio(self.width(), self.height())
        wid = int(wid)
        hei = int(hei)

        # 对外形进行缩放
        def transform_xy(org_x, org_y):
            return ((org_x - 0.5) * 0.95 + 0.5) * wid, ((org_y - 0.5) * 0.95 + 0.5) * hei

        # 机翼外形路径
        self.aircraft_fuel_out_path = QPainterPath()
        x0, y0 = data_collector.aircraft_fuel_out_frame[0]
        # 移动到初始点
        self.aircraft_fuel_out_path.moveTo(*transform_xy(x0, y0))
        for x, y in data_collector.aircraft_fuel_out_frame:
            x, y = transform_xy(x, y)
            self.aircraft_fuel_out_path.lineTo(x, y)
        self.aircraft_fuel_out_path.closeSubpath()
        # 中央翼油箱外形
        self.aircraft_center_fuel_path = QPainterPath()
        x0, y0 = data_collector.aircraft_center_fuel_frame[0]
        x0, y0 = transform_xy(x0, y0)
        self.aircraft_center_fuel_path.moveTo(x0, y0)
        left = right = x0
        top = bottom = y0
        for x, y in data_collector.aircraft_center_fuel_frame:
            x, y = transform_xy(x, y)
            # 获取遮挡的矩形数据
            if x < left:
                left = x
            if x > right:
                right = x
            if y < top:
                top = y
            if y > bottom:
                bottom = y
            self.aircraft_center_fuel_path.lineTo(x, y)
        self.aircraft_center_fuel_rect = (left, top, right - left, bottom - top)
        self.aircraft_center_fuel_path.closeSubpath()
        # 左翼油箱外形
        self.aircraft_left_fuel_path = QPainterPath()
        x0, y0 = data_collector.aircraft_left_fuel_frame[0]
        x0, y0 = transform_xy(x0, y0)
        self.aircraft_left_fuel_path.moveTo(x0, y0)
        left = right = x0
        top = bottom = y0
        for x, y in data_collector.aircraft_left_fuel_frame:
            x, y = transform_xy(x, y)
            if x < left:
                left = x
            if x > right:
                right = x
            if y < top:
                top = y
            if y > bottom:
                bottom = y
            self.aircraft_left_fuel_path.lineTo(x, y)
        self.aircraft_left_fuel_rect = (left, top, right - left, bottom - top)
        self.aircraft_left_fuel_path.closeSubpath()
        # 右翼油箱外形
        self.aircraft_right_fuel_path = QPainterPath()
        x0, y0 = data_collector.aircraft_right_fuel_frame[0]
        x0, y0 = transform_xy(x0, y0)
        self.aircraft_right_fuel_path.moveTo(x0, y0)
        left = right = x0
        top = bottom = y0
        for x, y in data_collector.aircraft_right_fuel_frame:
            x, y = transform_xy(x, y)
            if x < left:
                left = x
            if x > right:
                right = x
            if y < top:
                top = y
            if y > bottom:
                bottom = y
            self.aircraft_right_fuel_path.lineTo(x, y)
        self.aircraft_right_fuel_rect = (left, top, right - left, bottom - top)
        self.aircraft_right_fuel_path.closeSubpath()

    # 等比例缩放飞机，长宽缩放保持一致
    @staticmethod
    def normal_transform_ratio(wid, hei):
        if hei * data_collector.ratio_w_h > wid:
            hei = wid / data_collector.ratio_w_h
        elif hei * data_collector.ratio_w_h < wid:
            wid = hei * data_collector.ratio_w_h
        return wid, hei

    # 重写绘图函数
    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.gray)
        # self.update_fuel_out_path()
        if self.width() != self.old_width or self.height() != self.old_height:
            wid, hei = self.normal_transform_ratio(self.width(), self.height())
            old_wid, old_hei = self.normal_transform_ratio(self.old_width, self.old_height)
            k = wid / old_wid
            painter.scale(k, k)
        if self.aircraft_fuel_out_path:
            # 绘制飞机外形
            painter.drawPath(self.aircraft_fuel_out_path)
            # 更改颜色，显示油箱轮廓
            painter.setPen(Qt.white)
            painter.setBrush(Qt.gray)
            # 绘制中央翼油箱
            painter.drawPath(self.aircraft_center_fuel_path)
            # 绘制左翼油箱
            painter.drawPath(self.aircraft_left_fuel_path)
            # 绘制右翼油箱
            painter.drawPath(self.aircraft_right_fuel_path)

            # 显示百分比
            painter.setBrush(Qt.darkYellow)
            fill_path = QPainterPath()
            x, y, wid, hei = self.aircraft_center_fuel_rect
            fill_path.addRect(x, y, wid, hei * (1 - self.center_fuel_bank_weight_per))
            painter.drawPath(self.aircraft_center_fuel_path - fill_path)

            fill_path = QPainterPath()
            x, y, wid, hei = self.aircraft_left_fuel_rect
            fill_path.addRect(x, y, wid, hei * (1 - self.left_fuel_bank_weight_per))
            painter.drawPath(self.aircraft_left_fuel_path - fill_path)

            fill_path = QPainterPath()
            x, y, wid, hei = self.aircraft_right_fuel_rect
            fill_path.addRect(x, y, wid, hei * (1 - self.right_fuel_bank_weight_per))
            painter.drawPath(self.aircraft_right_fuel_path - fill_path)
