# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QPaintEvent, QPainterPath, QFont
from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QVBoxLayout, QLabel, QSpacerItem,
                             QSizePolicy, QMessageBox, QDoubleSpinBox, QAbstractSpinBox,
                             QGroupBox, QGridLayout, QToolButton, QSplitter)

from data_models import data_collector, config_info
from widgets.custom_tree_view_widget import UseItemTreeView, FuelConsumptionTreeDelegate
from widgets.custom_tree_view_model import FuelConsumptionTreeModel


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


# 自定义文本控件
class CustomLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet(config_info.label_style)


# 自定义的数值输入框
class CustomDoubleSpinBox(QDoubleSpinBox):
    def __init__(self, parent=None, decimals=1, minimum=0, maximum=1000000, suffix='  kg'):
        super().__init__(parent)

        self.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.setDecimals(decimals)
        self.setMaximum(maximum)
        self.setMinimum(minimum)
        self.setSuffix(suffix)
        self.setStyleSheet(config_info.fuel_weight_double_spin_style)


class FuelConsumptionOrder(QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet(config_info.group_box_style)

        self.verticalLayout = QVBoxLayout(self)
        self.horizontalLayout = QHBoxLayout()
        self.btn_add_item = QToolButton(self)
        self.btn_add_item.setToolButtonStyle(Qt.ToolButtonTextOnly)
        self.btn_add_item.setStyleSheet(config_info.button_style)
        self.btn_add_item.setFocusPolicy(Qt.NoFocus)
        self.horizontalLayout.addWidget(self.btn_add_item)
        self.btn_del_item = QToolButton(self)
        self.btn_del_item.setToolButtonStyle(Qt.ToolButtonTextOnly)
        self.btn_del_item.setStyleSheet(config_info.button_style)
        self.btn_del_item.setFocusPolicy(Qt.NoFocus)
        self.horizontalLayout.addWidget(self.btn_del_item)
        spacer_item = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacer_item)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tree_view_fuel_consumption_list = UseItemTreeView(self)
        self.verticalLayout.addWidget(self.tree_view_fuel_consumption_list)
        self.tree_model_fuel_consumption_list = FuelConsumptionTreeModel(list(), self.tree_view_fuel_consumption_list)
        self.tree_view_fuel_consumption_list.setModel(self.tree_model_fuel_consumption_list)
        self.tree_delegate = FuelConsumptionTreeDelegate()
        self.tree_view_fuel_consumption_list.setItemDelegate(self.tree_delegate)

        self.translate_ui()
        # 连接信号与槽
        self.btn_add_item.clicked.connect(self.add_fuel_consumption_point)
        self.btn_del_item.clicked.connect(self.del_fuel_consumption_point)

    # 增加一个燃油消耗转折点
    def add_fuel_consumption_point(self, flags=False, left_tank=0, center_tank=0, right_tank=0):
        position = self.tree_model_fuel_consumption_list.rowCount()
        status = self.tree_model_fuel_consumption_list.insertRows(position, 1)
        if status:
            widget_index = self.tree_model_fuel_consumption_list.index(position, 0)
            item = self.tree_model_fuel_consumption_list.getItem(widget_index)
            item.set_data(0, left_tank)
            item.set_data(1, center_tank)
            item.set_data(2, right_tank)

    # 删除燃油消耗转折点
    def del_fuel_consumption_point(self):
        cur_index = self.tree_view_fuel_consumption_list.currentIndex()
        if cur_index.row() != -1:
            message = QMessageBox.warning(self, '删除燃油消耗转折点', '确定要删除燃油消耗转折点吗?',
                                          QMessageBox.Yes | QMessageBox.No)
            if message == QMessageBox.Yes:
                self.tree_model_fuel_consumption_list.removeRow(cur_index.row())

    def translate_ui(self):
        self.setTitle('')
        self.btn_add_item.setText('   添加   ')
        self.btn_del_item.setText('   删除   ')


class AircraftFuelTankControl(QFrame):
    signal_fuel_change = pyqtSignal(float, float, float)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.gb_fuel_weight = QGroupBox(self)
        self.gridLayout = QGridLayout(self.gb_fuel_weight)
        self.btn_tran_kg_lb = QToolButton(self.gb_fuel_weight)
        self.btn_tran_kg_lb.setStyleSheet(config_info.button_style)
        self.gridLayout.addWidget(self.btn_tran_kg_lb, 0, 0, 1, 1)
        self.label_left_fuel_tank = CustomLabel(self.gb_fuel_weight)
        self.gridLayout.addWidget(self.label_left_fuel_tank, 0, 1, 1, 1)
        self.label_center_fuel_tank = CustomLabel(self.gb_fuel_weight)
        self.gridLayout.addWidget(self.label_center_fuel_tank, 0, 2, 1, 1)
        self.label_right_fuel_tank = CustomLabel(self.gb_fuel_weight)
        self.gridLayout.addWidget(self.label_right_fuel_tank, 0, 3, 1, 1)
        self.label_total_fuel_weight = CustomLabel(self.gb_fuel_weight)
        self.gridLayout.addWidget(self.label_total_fuel_weight, 0, 4, 1, 1)
        self.label_display_fuel_weight = CustomLabel(self.gb_fuel_weight)
        self.gridLayout.addWidget(self.label_display_fuel_weight, 1, 0, 1, 1)
        self.dsb_left_display = CustomDoubleSpinBox(self.gb_fuel_weight)
        self.gridLayout.addWidget(self.dsb_left_display, 1, 1, 1, 1)
        self.dsb_center_display = CustomDoubleSpinBox(self.gb_fuel_weight)
        self.gridLayout.addWidget(self.dsb_center_display, 1, 2, 1, 1)
        self.dsb_right_display = CustomDoubleSpinBox(self.gb_fuel_weight)
        self.gridLayout.addWidget(self.dsb_right_display, 1, 3, 1, 1)
        self.dsb_total_display = CustomDoubleSpinBox(self.gb_fuel_weight)
        self.dsb_total_display.setReadOnly(True)
        self.gridLayout.addWidget(self.dsb_total_display, 1, 4, 1, 1)
        self.label_real_fuel_weight = CustomLabel(self.gb_fuel_weight)
        self.gridLayout.addWidget(self.label_real_fuel_weight, 2, 0, 1, 1)
        self.dsb_left_actual = CustomDoubleSpinBox(self.gb_fuel_weight)
        self.gridLayout.addWidget(self.dsb_left_actual, 2, 1, 1, 1)
        self.dsb_center_actual = CustomDoubleSpinBox(self.gb_fuel_weight)
        self.gridLayout.addWidget(self.dsb_center_actual, 2, 2, 1, 1)
        self.dsb_right_actual = CustomDoubleSpinBox(self.gb_fuel_weight)
        self.gridLayout.addWidget(self.dsb_right_actual, 2, 3, 1, 1)
        self.dsb_total_actual = CustomDoubleSpinBox(self.gb_fuel_weight)
        self.dsb_total_actual.setReadOnly(True)
        self.gridLayout.addWidget(self.dsb_total_actual, 2, 4, 1, 1)
        self.verticalLayout.addWidget(self.gb_fuel_weight)
        self.gb_fuel_consumption_order = FuelConsumptionOrder(self)
        self.verticalLayout.addWidget(self.gb_fuel_consumption_order)
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacer_item)

        # 为了批量化处理
        self.dsb_list = [self.dsb_left_display, self.dsb_center_display, self.dsb_right_display, self.dsb_total_display,
                         self.dsb_left_actual, self.dsb_center_actual, self.dsb_right_actual, self.dsb_total_actual]
        self.dsb_flag_list = [('left', 'display'), ('central', 'display'), ('right', 'display'), ('total', 'display'),
                              ('left', 'actual'), ('central', 'actual'), ('right', 'actual'), ('total', 'actual')]

        self.translate_ui()

        # 进行单位切换
        self.btn_tran_kg_lb.clicked.connect(self.trans_kg_lb)
        for i, dsb in enumerate(self.dsb_list):
            if (i + 1) % 4 != 0:
                dsb.editingFinished.connect(self.fuel_tank_fuel_changed)

    # 计算油量百分比
    def cal_fuel_weight_percent(self):
        unit = self.dsb_center_actual.suffix()
        if unit == '  kg':
            left_tank = self.dsb_left_actual.value() / data_collector.aircraft.fuel_limit['左机翼油箱限制']
            center_tank = self.dsb_center_actual.value() / data_collector.aircraft.fuel_limit['中央翼油箱限制']
            right_tank = self.dsb_right_actual.value() / data_collector.aircraft.fuel_limit['右机翼油箱限制']
            return left_tank, center_tank, right_tank
        if unit == '  lb':
            left_tank = self.dsb_left_actual.value() * 0.454 / data_collector.aircraft.fuel_limit['左机翼油箱限制']
            center_tank = self.dsb_center_actual.value() * 0.454 / data_collector.aircraft.fuel_limit['中央翼油箱限制']
            right_tank = self.dsb_right_actual.value() * 0.454 / data_collector.aircraft.fuel_limit['右机翼油箱限制']
            return left_tank, center_tank, right_tank

    # 显示燃油量
    def display_fuel_value(self):
        self.dsb_left_actual.setValue(data_collector.aircraft.fuel_info['left'])
        self.dsb_center_actual.setValue(data_collector.aircraft.fuel_info['central'])
        self.dsb_right_actual.setValue(data_collector.aircraft.fuel_info['right'])
        self.dsb_total_actual.setValue(data_collector.aircraft.fuel_info['left'] +
                                       data_collector.aircraft.fuel_info['central'] +
                                       data_collector.aircraft.fuel_info['right'])

        # 显示油量计算
        fuel_tank_value = data_collector.aircraft.get_fuel_tank_fuel_weight('display')
        self.dsb_left_display.setValue(fuel_tank_value[0])
        self.dsb_center_display.setValue(fuel_tank_value[1])
        self.dsb_right_display.setValue(fuel_tank_value[2])
        self.dsb_total_display.setValue(fuel_tank_value[0] + fuel_tank_value[1] + fuel_tank_value[2])

        l, c, r = self.cal_fuel_weight_percent()
        # print('left: %f center: %f right: %f' % (l, c, r))
        self.signal_fuel_change.emit(c, l, r)

    # 油箱油量被改变
    def fuel_tank_fuel_changed(self):
        sender = self.sender()
        # 判断是否是修改了油量
        if isinstance(sender, CustomDoubleSpinBox) and sender in self.dsb_list:
            # 判断修改了哪个油量
            index = self.dsb_list.index(sender)
            fuel_tank, fuel_type = self.dsb_flag_list[index]

            # 判断油量是否超限
            actual_fuel = None
            is_over_limit = False
            limit_value = None
            try:
                if fuel_type == 'actual':
                    actual_fuel = sender.value()
                if fuel_type == 'display':
                    actual_fuel = data_collector.aircraft.fuel_display_actual_relation(sender.value(),
                                                                                       fuel_type, fuel_tank)
                # 根据实际油量判断是否超限
                if fuel_tank == 'left' and actual_fuel > data_collector.aircraft.fuel_limit['左机翼油箱限制']:
                    is_over_limit = True
                    limit_value = data_collector.aircraft.fuel_limit['左机翼油箱限制']
                if fuel_tank == 'central' and actual_fuel > data_collector.aircraft.fuel_limit['中央翼油箱限制']:
                    is_over_limit = True
                    limit_value = data_collector.aircraft.fuel_limit['中央翼油箱限制']
                if fuel_tank == 'right' and actual_fuel > data_collector.aircraft.fuel_limit['右机翼油箱限制']:
                    is_over_limit = True
                    limit_value = data_collector.aircraft.fuel_limit['右机翼油箱限制']
            except IndexError:
                # 超出插值范围
                is_over_limit = True
                if fuel_tank == 'left':
                    limit_value = data_collector.aircraft.fuel_limit['左机翼油箱限制']
                if fuel_tank == 'central':
                    limit_value = data_collector.aircraft.fuel_limit['中央翼油箱限制']
                if fuel_tank == 'right':
                    limit_value = data_collector.aircraft.fuel_limit['右机翼油箱限制']
            # 如果超限则提示超了什么限制并恢复原先的显示
            if is_over_limit:
                if fuel_type == 'actual':
                    sender.setValue(data_collector.aircraft.fuel_info[fuel_tank])
                if fuel_type == 'display':
                    d_value = data_collector.aircraft.fuel_display_actual_relation(
                        data_collector.aircraft.fuel_info[fuel_tank], 'actual', fuel_tank)
                    sender.setValue(d_value)
                QMessageBox.information(self, '提示', '输入的燃油量超出限制: %.1f kg/ %.1f lb' % (limit_value,
                                                                                      limit_value / 0.454))
                return

            # 如果修改了实际油量的处理
            if fuel_type == 'actual':
                # 更改飞机对象中的实际油量
                data_collector.aircraft.fuel_info[fuel_tank] = sender.value()
                # 相应的更改显示油量
                display_value = data_collector.aircraft.fuel_display_actual_relation(sender.value(),
                                                                                     fuel_type, fuel_tank)
                self.dsb_list[index - 4].setValue(display_value)
            # 如果修改了显示油量的处理
            if fuel_type == 'display':
                actual_value = data_collector.aircraft.fuel_display_actual_relation(sender.value(),
                                                                                    fuel_type, fuel_tank)
                data_collector.aircraft.fuel_info[fuel_tank] = actual_value
                self.dsb_list[index + 4].setValue(actual_value)
            # 更新总油量
            self.dsb_total_actual.setValue(data_collector.aircraft.fuel_info['left'] +
                                           data_collector.aircraft.fuel_info['central'] +
                                           data_collector.aircraft.fuel_info['right'])
            fuel_tank_value = data_collector.aircraft.get_fuel_tank_fuel_weight('display')
            self.dsb_total_display.setValue(fuel_tank_value[0] + fuel_tank_value[1] + fuel_tank_value[2])

            l, c, r = self.cal_fuel_weight_percent()
            self.signal_fuel_change.emit(c, l, r)

    # 单位换算
    def trans_kg_lb(self):
        unit = self.dsb_center_actual.suffix()
        if unit == '  kg':
            # 转换成lb
            for dsb in self.dsb_list:
                value = dsb.value()
                dsb.setValue(value / 0.454)
                dsb.setSuffix('  lb')
        if unit == '  lb':
            # 转换成lb
            for dsb in self.dsb_list:
                value = dsb.value()
                dsb.setValue(value * 0.454)
                dsb.setSuffix('  kg')

    def translate_ui(self):
        self.gb_fuel_weight.setTitle("燃油")
        self.btn_tran_kg_lb.setText("kg与lb切换")
        self.label_left_fuel_tank.setText("左机翼油箱")
        self.label_center_fuel_tank.setText("中央翼油箱")
        self.label_right_fuel_tank.setText("右机翼油箱")
        self.label_total_fuel_weight.setText("总油量")
        self.label_display_fuel_weight.setText("显示油量")
        self.label_real_fuel_weight.setText("实际油量")
        self.gb_fuel_consumption_order.setTitle("燃油消耗顺序")


class AircraftFuelTankWidget(QGroupBox):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setTitle('燃油设置')
        self.setStyleSheet(config_info.group_box_style)

        self.h_layout = QHBoxLayout(self)
        self.h_layout.setContentsMargins(0, 0, 6, 6)

        self.splitter_fuel_setting = QSplitter(self)
        self.splitter_fuel_setting.setOrientation(Qt.Horizontal)
        self.fuel_tank_sketch = AircraftFuelTankSketch()
        self.splitter_fuel_setting.addWidget(self.fuel_tank_sketch)
        self.fuel_tank_control = AircraftFuelTankControl()
        self.splitter_fuel_setting.addWidget(self.fuel_tank_control)

        self.splitter_fuel_setting.setStretchFactor(0, 3)
        self.splitter_fuel_setting.setStretchFactor(1, 2)
        self.h_layout.addWidget(self.splitter_fuel_setting)

        self.fuel_tank_control.signal_fuel_change.connect(self.fuel_tank_sketch.change_fuel_weight)

        self.update_fuel_initial_status()

    # 更新燃油初始状态
    def update_fuel_initial_status(self):
        # 更新初始燃油重量
        self.fuel_tank_control.display_fuel_value()
