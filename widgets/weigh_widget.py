# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPaintEvent, QPainterPath
from PyQt5.QtWidgets import QFrame

from data_models import data_collector


class AircraftSketch(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        # 存储轮廓信息
        self.aircraft_path = None

        # 记录变形前的控件尺寸
        self.old_width = self.width()
        self.old_height = self.height()

        # 加载油箱外形数据
        data_collector.load_aircraft_frame_data_from_excel()
        # 创建油箱外形的轮廓
        self.load_fuel_bank_path()

    # 创建油箱外形的路径
    def load_fuel_bank_path(self):
        wid, hei = self.normal_transform_ratio(self.width(), self.height())
        wid = int(wid)
        hei = int(hei)

        # 对外形进行缩放
        def transform_xy(org_x, org_y):
            return ((org_x - 0.5) * 0.95 + 0.5) * wid, ((org_y - 0.5) * 0.95 + 0.5) * hei

        # 飞机外形路径
        self.aircraft_path = QPainterPath()
        x0, y0 = data_collector.aircraft_frame[0]
        # 移动到初始点
        self.aircraft_path.moveTo(*transform_xy(x0, y0))
        for x, y in data_collector.aircraft_frame:
            x, y = transform_xy(x, y)
            self.aircraft_path.lineTo(x, y)
        self.aircraft_path.closeSubpath()

    # 等比例缩放飞机，长宽缩放保持一致
    @staticmethod
    def normal_transform_ratio(wid, hei):
        if hei * data_collector.aircraft_frame_ratio_w_h > wid:
            hei = wid / data_collector.aircraft_frame_ratio_w_h
        elif hei * data_collector.aircraft_frame_ratio_w_h < wid:
            wid = hei * data_collector.aircraft_frame_ratio_w_h
        return wid, hei

    # 重写绘图函数
    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.gray)
        if self.width() != self.old_width or self.height() != self.old_height:
            wid, hei = self.normal_transform_ratio(self.width(), self.height())
            old_wid, old_hei = self.normal_transform_ratio(self.old_width, self.old_height)
            k = wid / old_wid
            painter.scale(k, k)
        if self.aircraft_path:
            # 绘制飞机外形
            painter.drawPath(self.aircraft_path)
