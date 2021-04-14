# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtGui import QPainter, QPaintEvent, QPainterPath, QFont
from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QVBoxLayout, QLabel, QSpacerItem,
                             QSizePolicy, QSlider, QDoubleSpinBox, QAbstractSpinBox,
                             QGroupBox)

from data_models import data_collector, config_info
from widgets.result_info_show_widget import ResultInfoShowWidget


class AircraftFuelTankSketch(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        font = QFont()
        font.setFamily('微软雅黑')
        self.setFont(font)

        # 油量百分比
        self.center_fuel_bank_weight_per = 0
        self.left_fuel_bank_weight_per = 0
        self.right_fuel_bank_weight_per = 0

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
        x0, y0 = data_collector.aircraft.aircraft_fuel_out_frame[0]
        # 移动到初始点
        self.aircraft_fuel_out_path.moveTo(*transform_xy(x0, y0))
        for x, y in data_collector.aircraft.aircraft_fuel_out_frame:
            x, y = transform_xy(x, y)
            self.aircraft_fuel_out_path.lineTo(x, y)
        self.aircraft_fuel_out_path.closeSubpath()
        # 中央翼油箱外形
        self.aircraft_center_fuel_path = QPainterPath()
        x0, y0 = data_collector.aircraft.aircraft_center_fuel_frame[0]
        x0, y0 = transform_xy(x0, y0)
        self.aircraft_center_fuel_path.moveTo(x0, y0)
        left = right = x0
        top = bottom = y0
        for x, y in data_collector.aircraft.aircraft_center_fuel_frame:
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
        x0, y0 = data_collector.aircraft.aircraft_left_fuel_frame[0]
        x0, y0 = transform_xy(x0, y0)
        self.aircraft_left_fuel_path.moveTo(x0, y0)
        left = right = x0
        top = bottom = y0
        for x, y in data_collector.aircraft.aircraft_left_fuel_frame:
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
        x0, y0 = data_collector.aircraft.aircraft_right_fuel_frame[0]
        x0, y0 = transform_xy(x0, y0)
        self.aircraft_right_fuel_path.moveTo(x0, y0)
        left = right = x0
        top = bottom = y0
        for x, y in data_collector.aircraft.aircraft_right_fuel_frame:
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
        if hei * data_collector.aircraft.ratio_w_h > wid:
            hei = wid / data_collector.aircraft.ratio_w_h
        elif hei * data_collector.aircraft.ratio_w_h < wid:
            wid = hei * data_collector.aircraft.ratio_w_h
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


class AircraftFuelTankControl(QFrame):
    signal_fuel_change = pyqtSignal(float, float, float)

    def __init__(self, parent=None):
        super().__init__(parent)

        font = QFont()
        font.setFamily('微软雅黑')
        self.setFont(font)

        self.resize(719, 424)
        self.horizontalLayout_4 = QHBoxLayout(self)
        self.verticalLayout = QVBoxLayout()
        self.label_left_tank_limit = QLabel(self)
        self.label_left_tank_limit.setAlignment(Qt.AlignCenter)
        self.verticalLayout.addWidget(self.label_left_tank_limit)
        self.horizontalLayout = QHBoxLayout()
        spacer_item = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacer_item)
        self.vertical_slider_left_tank = QSlider(self)
        self.vertical_slider_left_tank.setMaximum(100)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.vertical_slider_left_tank.sizePolicy().hasHeightForWidth())
        self.vertical_slider_left_tank.setSizePolicy(size_policy)
        self.vertical_slider_left_tank.setOrientation(Qt.Vertical)
        self.vertical_slider_left_tank.setTickPosition(QSlider.TicksAbove)
        self.horizontalLayout.addWidget(self.vertical_slider_left_tank)
        spacer_item = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacer_item)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_left_tank = QLabel(self)
        self.label_left_tank.setAlignment(Qt.AlignCenter)
        self.verticalLayout.addWidget(self.label_left_tank)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.double_spinBox_left_tank = QDoubleSpinBox(self)
        self.double_spinBox_left_tank.setFrame(QFrame.NoFrame)
        self.double_spinBox_left_tank.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.double_spinBox_left_tank.setDecimals(1)
        self.double_spinBox_left_tank.setMaximum(100000.0)
        self.double_spinBox_left_tank.setSingleStep(0.1)
        self.horizontalLayout_4.addWidget(self.double_spinBox_left_tank)
        self.verticalLayout_2 = QVBoxLayout()
        self.label_center_tank_limit = QLabel(self)
        self.label_center_tank_limit.setAlignment(Qt.AlignCenter)
        self.verticalLayout_2.addWidget(self.label_center_tank_limit)
        self.horizontalLayout_2 = QHBoxLayout()
        spacer_item = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacer_item)
        self.vertical_slider_center_tank = QSlider(self)
        self.vertical_slider_center_tank.setMaximum(100)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.vertical_slider_center_tank.sizePolicy().hasHeightForWidth())
        self.vertical_slider_center_tank.setSizePolicy(size_policy)
        self.vertical_slider_center_tank.setOrientation(Qt.Vertical)
        self.vertical_slider_center_tank.setTickPosition(QSlider.TicksAbove)
        self.horizontalLayout_2.addWidget(self.vertical_slider_center_tank)
        spacer_item = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacer_item)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.label_center_tank = QLabel(self)
        self.label_center_tank.setAlignment(Qt.AlignCenter)
        self.verticalLayout_2.addWidget(self.label_center_tank)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.double_spinBox_center_tank = QDoubleSpinBox(self)
        self.double_spinBox_center_tank.setFrame(QFrame.NoFrame)
        self.double_spinBox_center_tank.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.double_spinBox_center_tank.setDecimals(1)
        self.double_spinBox_center_tank.setMaximum(100000.0)
        self.double_spinBox_center_tank.setSingleStep(0.1)
        self.horizontalLayout_4.addWidget(self.double_spinBox_center_tank)
        self.verticalLayout_3 = QVBoxLayout()
        self.label_right_tank_limit = QLabel(self)
        self.label_right_tank_limit.setAlignment(Qt.AlignCenter)
        self.verticalLayout_3.addWidget(self.label_right_tank_limit)
        self.horizontalLayout_3 = QHBoxLayout()
        spacer_item = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacer_item)
        self.vertical_slider_right_tank = QSlider(self)
        self.vertical_slider_right_tank.setMaximum(100)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.vertical_slider_right_tank.sizePolicy().hasHeightForWidth())
        self.vertical_slider_right_tank.setSizePolicy(size_policy)
        self.vertical_slider_right_tank.setOrientation(Qt.Vertical)
        self.vertical_slider_right_tank.setTickPosition(QSlider.TicksAbove)
        self.horizontalLayout_3.addWidget(self.vertical_slider_right_tank)
        spacer_item = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacer_item)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.label_right_tank = QLabel(self)
        self.label_right_tank.setAlignment(Qt.AlignCenter)
        self.verticalLayout_3.addWidget(self.label_right_tank)
        self.horizontalLayout_4.addLayout(self.verticalLayout_3)
        self.double_spinBox_right_tank = QDoubleSpinBox(self)
        self.double_spinBox_right_tank.setFrame(QFrame.NoFrame)
        self.double_spinBox_right_tank.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.double_spinBox_right_tank.setDecimals(1)
        self.double_spinBox_right_tank.setMaximum(100000.0)
        self.double_spinBox_right_tank.setSingleStep(0.1)
        self.horizontalLayout_4.addWidget(self.double_spinBox_right_tank)

        self.translate()
        # self.display_limit_fuel_value()

        self.vertical_slider_left_tank.valueChanged.connect(self.change_fuel_display)
        self.vertical_slider_center_tank.valueChanged.connect(self.change_fuel_display)
        self.vertical_slider_right_tank.valueChanged.connect(self.change_fuel_display)

    def change_fuel_display(self, value):
        sender = QObject.sender(self)
        if sender == self.vertical_slider_left_tank:
            fuel = value * data_collector.aircraft.fuel_info['left_limit'] / 100
            # 更新data_collector中的数据
            data_collector.aircraft.set_fuel_info(left=fuel)
            # 更新控制条的位置
            self.double_spinBox_left_tank.setValue(fuel)
        if sender == self.vertical_slider_center_tank:
            fuel = value * data_collector.aircraft.fuel_info['center_limit'] / 100
            data_collector.aircraft.set_fuel_info(central=fuel)
            self.double_spinBox_center_tank.setValue(fuel)
        if sender == self.vertical_slider_right_tank:
            fuel = value * data_collector.aircraft.fuel_info['right_limit'] / 100
            data_collector.aircraft.set_fuel_info(right=fuel)
            self.double_spinBox_right_tank.setValue(fuel)

        self.signal_fuel_change.emit(self.vertical_slider_center_tank.value() / 100,
                                     self.vertical_slider_left_tank.value() / 100,
                                     self.vertical_slider_right_tank.value() / 100)

    # 显示限制燃油值
    def display_limit_fuel_value(self):
        self.label_left_tank_limit.setText('%.1f kg' % data_collector.aircraft.fuel_info['left_limit'])
        self.label_center_tank_limit.setText('%.1f kg' % data_collector.aircraft.fuel_info['center_limit'])
        self.label_right_tank_limit.setText('%.1f kg' % data_collector.aircraft.fuel_info['right_limit'])

    # 显示燃油量
    def display_fuel_value(self):
        self.vertical_slider_left_tank.setValue(
            data_collector.aircraft.fuel_info['left'] / data_collector.aircraft.fuel_info['left_limit'] * 100)
        self.vertical_slider_center_tank.setValue(
            data_collector.aircraft.fuel_info['central'] / data_collector.aircraft.fuel_info['center_limit'] * 100)
        self.vertical_slider_right_tank.setValue(
            data_collector.aircraft.fuel_info['right'] / data_collector.aircraft.fuel_info['right_limit'] * 100)

    def translate(self):
        self.label_left_tank_limit.setText("TextLabel")
        self.label_left_tank.setText("左机翼油箱")
        self.label_center_tank_limit.setText("TextLabel")
        self.label_center_tank.setText("中央翼油箱")
        self.label_right_tank_limit.setText("TextLabel")
        self.label_right_tank.setText("右机翼油箱")


class AircraftFuelTankWidget(QGroupBox):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setTitle('燃油设置')
        self.setStyleSheet(config_info.group_box_style)

        self.h_layout = QHBoxLayout(self)
        self.fuel_tank_sketch = AircraftFuelTankSketch()
        self.h_layout.addWidget(self.fuel_tank_sketch)
        self.fuel_tank_control = AircraftFuelTankControl()
        self.h_layout.addWidget(self.fuel_tank_control)
        self.h_layout.setStretch(0, 4)
        self.h_layout.setStretch(1, 1)

        self.fuel_tank_control.signal_fuel_change.connect(self.fuel_tank_sketch.change_fuel_weight)

        self.update_fuel_initial_status()

    # 更新燃油初始状态
    def update_fuel_initial_status(self):
        # 更新燃油限制值
        self.fuel_tank_control.display_limit_fuel_value()
        # 更新初始燃油重量
        self.fuel_tank_control.display_fuel_value()


class AircraftFuelTankPage(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.aircraft_fuel_tank = AircraftFuelTankWidget(self)
        self.verticalLayout.addWidget(self.aircraft_fuel_tank)
        self.show_result_info_widget = ResultInfoShowWidget()
        self.verticalLayout.addWidget(self.show_result_info_widget)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
