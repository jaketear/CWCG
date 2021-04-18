# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QDate, pyqtSignal
from PyQt5.QtGui import QPainter, QPaintEvent, QPainterPath, QMouseEvent
from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QSplitter, QWidget, QVBoxLayout,
                             QGroupBox, QGridLayout, QLabel, QLineEdit, QDialog,
                             QToolButton, QSizePolicy, QDateEdit, QDoubleSpinBox,
                             QAbstractSpinBox)

from data_models import data_collector, config_info
from data_models.data_collector import aircraft
from widgets.aircraft_use_item import AircraftUseItemWidget
from widgets.custom_dialog import WeighDialog


# 绘制飞机外形
class AircraftSketch(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        # 存储轮廓信息
        self.aircraft_path = None

        # 记录变形前的控件尺寸
        self.old_width = self.width()
        self.old_height = self.height()

        # 创建飞机外形的轮廓
        self.load_aircraft_frame_path()
        # 按钮区域
        self.weigh_first_btn_area = None
        self.weigh_second_btn_area = None

    # 创建飞机外形的路径
    def load_aircraft_frame_path(self):
        wid, hei = self.normal_transform_ratio(self.width(), self.height())
        wid = int(wid)
        hei = int(hei)

        # 对外形进行缩放
        def transform_xy(org_x, org_y):
            return ((org_x - 0.5) * 0.95 + 0.5) * wid, ((org_y - 0.5) * 0.95 + 0.5) * hei

        # 飞机外形路径
        self.aircraft_path = QPainterPath()
        x0, y0 = aircraft.aircraft_frame[0]
        # 移动到初始点
        self.aircraft_path.moveTo(*transform_xy(x0, y0))
        for x, y in aircraft.aircraft_frame:
            x, y = transform_xy(x, y)
            self.aircraft_path.lineTo(x, y)
        self.aircraft_path.closeSubpath()

    # 等比例缩放飞机，长宽缩放保持一致
    @staticmethod
    def normal_transform_ratio(wid, hei):
        if hei * data_collector.aircraft.aircraft_frame_ratio_w_h > wid:
            hei = wid / data_collector.aircraft.aircraft_frame_ratio_w_h
        elif hei * data_collector.aircraft.aircraft_frame_ratio_w_h < wid:
            wid = hei * data_collector.aircraft.aircraft_frame_ratio_w_h
        return wid, hei

    # 重写绘图函数
    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        # 绘制飞机外形
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


# 自定义的数值输入框
class CustomDoubleSpinBox(QDoubleSpinBox):
    def __init__(self, parent=None, decimals=0, minimum=0, maximum=1000000, suffix='  kg'):
        super().__init__(parent)

        self.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.setDecimals(decimals)
        self.setMaximum(maximum)
        self.setMinimum(minimum)
        self.setSuffix(suffix)
        self.setStyleSheet(config_info.double_spin_style)


# 各个轮胎上的重量信息输入控件
class TyreWeightGroupbox(QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.gridLayout = QGridLayout(self)
        self.gridLayout.setContentsMargins(6, 2, 6, 6)
        self.gridLayout.setSpacing(9)
        self.label_nose_gear_left = QLabel(self)
        self.label_nose_gear_left.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label_nose_gear_left.setStyleSheet(config_info.label_style)
        self.gridLayout.addWidget(self.label_nose_gear_left, 0, 0, 1, 1)
        self.dsb_nose_gear_left = CustomDoubleSpinBox(self)
        self.gridLayout.addWidget(self.dsb_nose_gear_left, 0, 1, 1, 1)
        self.label_nose_gear_right = QLabel(self)
        self.label_nose_gear_right.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label_nose_gear_right.setStyleSheet(config_info.label_style)
        self.gridLayout.addWidget(self.label_nose_gear_right, 1, 0, 1, 1)
        self.dsb_nose_gear_right = CustomDoubleSpinBox(self)
        self.gridLayout.addWidget(self.dsb_nose_gear_right, 1, 1, 1, 1)
        self.line = QFrame(self)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.gridLayout.addWidget(self.line, 2, 0, 1, 2)
        self.label_left_main_gear_out = QLabel(self)
        self.label_left_main_gear_out.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label_left_main_gear_out.setStyleSheet(config_info.label_style)
        self.gridLayout.addWidget(self.label_left_main_gear_out, 3, 0, 1, 1)
        self.dsb_left_main_gear_out = CustomDoubleSpinBox(self)
        self.gridLayout.addWidget(self.dsb_left_main_gear_out, 3, 1, 1, 1)
        self.label_left_main_gear_in = QLabel(self)
        self.label_left_main_gear_in.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label_left_main_gear_in.setStyleSheet(config_info.label_style)
        self.gridLayout.addWidget(self.label_left_main_gear_in, 4, 0, 1, 1)
        self.dsb_left_main_gear_in = CustomDoubleSpinBox(self)
        self.gridLayout.addWidget(self.dsb_left_main_gear_in, 4, 1, 1, 1)
        self.line_4 = QFrame(self)
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)
        self.gridLayout.addWidget(self.line_4, 5, 0, 1, 2)
        self.label_right_main_gear_in = QLabel(self)
        self.label_right_main_gear_in.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label_right_main_gear_in.setStyleSheet(config_info.label_style)
        self.gridLayout.addWidget(self.label_right_main_gear_in, 6, 0, 1, 1)
        self.dsb_right_main_gear_in = CustomDoubleSpinBox(self)
        self.gridLayout.addWidget(self.dsb_right_main_gear_in, 6, 1, 1, 1)
        self.label_right_main_gear_out = QLabel(self)
        self.label_right_main_gear_out.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label_right_main_gear_out.setStyleSheet(config_info.label_style)
        self.gridLayout.addWidget(self.label_right_main_gear_out, 7, 0, 1, 1)
        self.dsb_right_main_gear_out = CustomDoubleSpinBox(self)
        self.gridLayout.addWidget(self.dsb_right_main_gear_out, 7, 1, 1, 1)

        self.translate()

    def translate(self):
        self.setTitle("GroupBox")
        self.label_nose_gear_left.setText("前起左侧(NL)")
        self.label_nose_gear_right.setText("前起右侧(NR)")
        self.label_left_main_gear_out.setText("左主起外侧(LO)")
        self.label_left_main_gear_in.setText("左主起内侧(LI)")
        self.label_right_main_gear_in.setText("右主起内侧(RI)")
        self.label_right_main_gear_out.setText("右主起外侧(RO)")


class AircraftWeighWidget(QFrame):
    signal_weigh_info_change = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.h_layout = QHBoxLayout(self)
        self.h_layout.setContentsMargins(0, 0, 0, 0)

        self.splitter_record = QSplitter(self)
        self.splitter_record.setOrientation(Qt.Horizontal)
        self.aircraft_sketch = AircraftSketch(self)
        self.splitter_record.addWidget(self.aircraft_sketch)

        self.widget = QWidget(self)
        self.v_layout = QVBoxLayout(self.widget)
        self.v_layout.setContentsMargins(0, 0, 0, 0)

        # 称重基本信息
        self.gb_weigh_info = QGroupBox(self.widget)
        self.gb_weigh_info.setStyleSheet(config_info.group_box_style)
        self.gridLayout = QGridLayout(self.gb_weigh_info)
        self.gridLayout.setContentsMargins(6, 2, 6, 6)
        self.gridLayout.setSpacing(6)

        self.label_weigh_report_id = QLabel(self.gb_weigh_info)
        self.label_weigh_report_id.setStyleSheet(config_info.label_style)
        self.label_weigh_report_id.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.gridLayout.addWidget(self.label_weigh_report_id, 0, 0, 1, 1)
        self.line_edit_weigh_report_id = QLineEdit(self.gb_weigh_info)
        self.line_edit_weigh_report_id.setStyleSheet(config_info.line_edit_style)
        self.gridLayout.addWidget(self.line_edit_weigh_report_id, 0, 1, 1, 7)

        self.label_weigh_date = QLabel(self.gb_weigh_info)
        self.label_weigh_date.setStyleSheet(config_info.label_style)
        self.label_weigh_date.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.gridLayout.addWidget(self.label_weigh_date, 1, 0, 1, 1)
        self.date_edit_weigh_date = QDateEdit(self.gb_weigh_info)
        self.date_edit_weigh_date.setStyleSheet(config_info.date_edit_style)
        self.date_edit_weigh_date.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.gridLayout.addWidget(self.date_edit_weigh_date, 1, 1, 1, 1)
        self.label_weigh_loc = QLabel(self.gb_weigh_info)
        self.label_weigh_loc.setStyleSheet(config_info.label_style)
        self.label_weigh_loc.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.gridLayout.addWidget(self.label_weigh_loc, 1, 2, 1, 1)
        self.line_edit_weigh_loc = QLineEdit(self.gb_weigh_info)
        self.line_edit_weigh_loc.setStyleSheet(config_info.line_edit_style)
        self.gridLayout.addWidget(self.line_edit_weigh_loc, 1, 3, 1, 1)
        self.label_aircraft_type = QLabel(self.gb_weigh_info)
        self.label_aircraft_type.setStyleSheet(config_info.label_style)
        self.label_aircraft_type.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.gridLayout.addWidget(self.label_aircraft_type, 1, 4, 1, 1)
        self.line_edit_aircraft_type = QLineEdit(self.gb_weigh_info)
        self.line_edit_aircraft_type.setStyleSheet(config_info.line_edit_style)
        self.gridLayout.addWidget(self.line_edit_aircraft_type, 1, 5, 1, 1)
        self.label_aircraft_id = QLabel(self.gb_weigh_info)
        self.label_aircraft_id.setStyleSheet(config_info.label_style)
        self.label_aircraft_id.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.gridLayout.addWidget(self.label_aircraft_id, 1, 6, 1, 1)
        self.line_edit_aircraft_id = QLineEdit(self.gb_weigh_info)
        self.line_edit_aircraft_id.setStyleSheet(config_info.line_edit_style)
        self.gridLayout.addWidget(self.line_edit_aircraft_id, 1, 7, 1, 1)
        self.v_layout.addWidget(self.gb_weigh_info)

        self.h_layout_tyre_weights = QHBoxLayout()
        # 各个轮胎上的重量信息
        self.gb_tyre_weights_first = TyreWeightGroupbox(self.widget)
        self.gb_tyre_weights_first.setStyleSheet(config_info.group_box_style)
        self.h_layout_tyre_weights.addWidget(self.gb_tyre_weights_first)
        self.gb_tyre_weights_second = TyreWeightGroupbox(self.widget)
        self.gb_tyre_weights_second.setStyleSheet(config_info.group_box_style)
        self.h_layout_tyre_weights.addWidget(self.gb_tyre_weights_second)
        self.v_layout.addLayout(self.h_layout_tyre_weights)

        # 称重的其他数据，缓冲支柱行程和俯仰角
        self.gb_weigh_data = QGroupBox(self.widget)
        self.gb_weigh_data.setStyleSheet(config_info.group_box_style)
        self.grid_layout_weigh_data = QGridLayout(self.gb_weigh_data)
        self.grid_layout_weigh_data.setContentsMargins(6, 2, 6, 6)
        self.grid_layout_weigh_data.setSpacing(6)

        self.label_left_main_compress_distance = QLabel(self.gb_weigh_data)
        self.label_left_main_compress_distance.setStyleSheet(config_info.label_style)
        self.label_left_main_compress_distance.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.grid_layout_weigh_data.addWidget(self.label_left_main_compress_distance, 0, 0, 1, 1)
        self.dsb_left_main_compress_distance = CustomDoubleSpinBox(self.gb_weigh_data, suffix='  mm')
        self.grid_layout_weigh_data.addWidget(self.dsb_left_main_compress_distance, 0, 1, 1, 1)
        self.label_right_main_compress_distance = QLabel(self.gb_weigh_data)
        self.label_right_main_compress_distance.setStyleSheet(config_info.label_style)
        self.label_right_main_compress_distance.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.grid_layout_weigh_data.addWidget(self.label_right_main_compress_distance, 0, 2, 1, 1)
        self.dsb_right_main_compress_distance = CustomDoubleSpinBox(self.gb_weigh_data, suffix='  mm')
        self.grid_layout_weigh_data.addWidget(self.dsb_right_main_compress_distance, 0, 3, 1, 1)

        self.label_nose_compress_distance = QLabel(self.gb_weigh_data)
        self.label_nose_compress_distance.setStyleSheet(config_info.label_style)
        self.label_nose_compress_distance.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.grid_layout_weigh_data.addWidget(self.label_nose_compress_distance, 1, 0, 1, 1)
        self.dsb_nose_compress_distance = CustomDoubleSpinBox(self.gb_weigh_data, suffix='  mm')
        self.grid_layout_weigh_data.addWidget(self.dsb_nose_compress_distance, 1, 1, 1, 1)

        self.label_pitch_angle = QLabel(self.gb_weigh_data)
        self.label_pitch_angle.setStyleSheet(config_info.label_style)
        self.label_pitch_angle.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.grid_layout_weigh_data.addWidget(self.label_pitch_angle, 1, 2, 1, 1)
        self.dsb_pitch_angle = CustomDoubleSpinBox(self.gb_weigh_data,
                                                   decimals=1, minimum=-90, maximum=90, suffix='  °')
        self.grid_layout_weigh_data.addWidget(self.dsb_pitch_angle, 1, 3, 1, 1)
        self.v_layout.addWidget(self.gb_weigh_data)

        self.h_layout_unit = QHBoxLayout()
        # 多/缺装件信息
        self.gb_surplus_units = AircraftUseItemWidget(self.widget, item_type='redundant item')
        self.gb_surplus_units.btn_submit.setVisible(False)
        self.gb_surplus_units.setStyleSheet(config_info.group_box_style)
        self.h_layout_unit.addWidget(self.gb_surplus_units)
        self.gb_lack_units = AircraftUseItemWidget(self.widget, item_type='absence item')
        self.gb_lack_units.btn_submit.setVisible(False)
        self.gb_lack_units.setStyleSheet(config_info.group_box_style)
        self.h_layout_unit.addWidget(self.gb_lack_units)
        self.v_layout.addLayout(self.h_layout_unit)

        self.btn_cal_weight_cg = QToolButton(self)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.btn_cal_weight_cg.setSizePolicy(size_policy)
        self.btn_cal_weight_cg.setStyleSheet(config_info.button_style)
        self.v_layout.addWidget(self.btn_cal_weight_cg)

        # 结果信息
        self.gb_result_info = QGroupBox(self.widget)
        self.gb_result_info.setStyleSheet(config_info.group_box_style)
        self.gridLayout_result_info = QGridLayout(self.gb_result_info)
        self.gridLayout_result_info.setContentsMargins(6, 2, 6, 6)
        self.gridLayout_result_info.setSpacing(6)
        self.label_real_weight = QLabel(self.gb_result_info)
        self.label_real_weight.setStyleSheet(config_info.label_style)
        self.label_real_weight.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.gridLayout_result_info.addWidget(self.label_real_weight, 0, 0, 1, 1)
        self.dsb_real_weight = CustomDoubleSpinBox(self.gb_result_info)
        self.dsb_real_weight.setReadOnly(True)
        self.gridLayout_result_info.addWidget(self.dsb_real_weight, 0, 1, 1, 1)
        self.label_real_cg = QLabel(self.gb_result_info)
        self.label_real_cg.setStyleSheet(config_info.label_style)
        self.label_real_cg.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.gridLayout_result_info.addWidget(self.label_real_cg, 0, 2, 1, 1)
        self.dsb_real_cg = CustomDoubleSpinBox(self.gb_result_info, decimals=2, suffix='  %MAC')
        self.dsb_real_cg.setReadOnly(True)
        self.gridLayout_result_info.addWidget(self.dsb_real_cg, 0, 3, 1, 1)
        self.label_empty_weight = QLabel(self.gb_result_info)
        self.label_empty_weight.setStyleSheet(config_info.label_style)
        self.label_empty_weight.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.gridLayout_result_info.addWidget(self.label_empty_weight, 1, 0, 1, 1)
        self.dsb_empty_weight = CustomDoubleSpinBox(self.gb_result_info)
        self.dsb_empty_weight.setReadOnly(True)
        self.gridLayout_result_info.addWidget(self.dsb_empty_weight, 1, 1, 1, 1)
        self.label_empty_cg = QLabel(self.gb_result_info)
        self.label_empty_cg.setStyleSheet(config_info.label_style)
        self.label_empty_cg.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.gridLayout_result_info.addWidget(self.label_empty_cg, 1, 2, 1, 1)
        self.dsb_empty_cg = CustomDoubleSpinBox(self.gb_result_info, decimals=2, suffix='  %MAC')
        self.dsb_empty_cg.setReadOnly(True)
        self.gridLayout_result_info.addWidget(self.dsb_empty_cg, 1, 3, 1, 1)
        self.v_layout.addWidget(self.gb_result_info)

        self.splitter_record.addWidget(self.widget)
        self.splitter_record.setStretchFactor(0, 7)
        self.splitter_record.setStretchFactor(1, 1)

        self.h_layout.addWidget(self.splitter_record)

        self.translate_ui()
        self.display_weigh_info()

        self.btn_cal_weight_cg.clicked.connect(self.cal_weigh_result)

    # 计算称重结果
    def cal_weigh_result(self):
        self.set_weigh_info()
        aircraft.export_weight_info_to_json(file_dir='')
        aircraft.update_weigh_result()

        # 设置称重结果
        self.dsb_real_weight.setValue(aircraft.real_weight_in_weigh)
        self.dsb_real_cg.setValue(aircraft.real_cg_in_weigh)
        self.dsb_empty_weight.setValue(aircraft.aircraft_empty_weight)
        self.dsb_empty_cg.setValue(aircraft.aircraft_empty_cg)

        self.signal_weigh_info_change.emit()

    # 显示飞机的称重信息
    def display_weigh_info(self):
        if aircraft.weigh_info:

            # 设置基本信息
            self.date_edit_weigh_date.setDate(QDate.fromString(aircraft.weigh_info['weigh_date'],
                                                               'yyyy/MM/dd'))
            self.line_edit_weigh_loc.setText(aircraft.weigh_info['weigh_location'])
            self.line_edit_aircraft_type.setText(aircraft.weigh_info['aircraft_type'])
            self.line_edit_aircraft_id.setText(aircraft.weigh_info['aircraft'])
            self.line_edit_weigh_report_id.setText(aircraft.weigh_info['weigh_report_id'])

            # 设置第一次称重结果
            self.gb_tyre_weights_first.dsb_nose_gear_left.setValue(aircraft.weigh_info['weigh_tyre_nl'][0])
            self.gb_tyre_weights_first.dsb_nose_gear_right.setValue(aircraft.weigh_info['weigh_tyre_nr'][0])
            self.gb_tyre_weights_first.dsb_left_main_gear_in.setValue(aircraft.weigh_info['weigh_tyre_li'][0])
            self.gb_tyre_weights_first.dsb_left_main_gear_out.setValue(aircraft.weigh_info['weigh_tyre_lo'][0])
            self.gb_tyre_weights_first.dsb_right_main_gear_out.setValue(aircraft.weigh_info['weigh_tyre_ro'][0])
            self.gb_tyre_weights_first.dsb_right_main_gear_in.setValue(aircraft.weigh_info['weigh_tyre_ri'][0])

            # 设置第二次称重结果
            self.gb_tyre_weights_second.dsb_nose_gear_left.setValue(aircraft.weigh_info['weigh_tyre_nl'][1])
            self.gb_tyre_weights_second.dsb_nose_gear_right.setValue(aircraft.weigh_info['weigh_tyre_nr'][1])
            self.gb_tyre_weights_second.dsb_left_main_gear_in.setValue(aircraft.weigh_info['weigh_tyre_li'][1])
            self.gb_tyre_weights_second.dsb_left_main_gear_out.setValue(aircraft.weigh_info['weigh_tyre_lo'][1])
            self.gb_tyre_weights_second.dsb_right_main_gear_out.setValue(aircraft.weigh_info['weigh_tyre_ro'][1])
            self.gb_tyre_weights_second.dsb_right_main_gear_in.setValue(aircraft.weigh_info['weigh_tyre_ri'][1])

            # 设置几何参数
            self.dsb_nose_compress_distance.setValue(aircraft.weigh_info['weigh_pillar_ln'])
            self.dsb_right_main_compress_distance.setValue(aircraft.weigh_info['weigh_pillar_lmr'])
            self.dsb_left_main_compress_distance.setValue(aircraft.weigh_info['weigh_pillar_lml'])
            self.dsb_pitch_angle.setValue(aircraft.weigh_info['pitch_angle'])

            # 设置多装件
            self.gb_surplus_units.display_items()
            # 设置缺装件
            self.gb_lack_units.display_items()

            # 设置称重结果
            self.dsb_real_weight.setValue(aircraft.real_weight_in_weigh)
            self.dsb_real_cg.setValue(aircraft.real_cg_in_weigh)
            self.dsb_empty_weight.setValue(aircraft.aircraft_empty_weight)
            self.dsb_empty_cg.setValue(aircraft.aircraft_empty_cg)

    def set_weigh_info(self):
        # 设置基本信息
        aircraft.weigh_info['weigh_date'] = self.date_edit_weigh_date.date().toString('yyyy/MM/dd')
        aircraft.weigh_info['weigh_location'] = self.line_edit_weigh_loc.text()
        aircraft.weigh_info['aircraft_type'] = self.line_edit_aircraft_type.text()
        aircraft.weigh_info['aircraft'] = self.line_edit_aircraft_id.text()
        aircraft.weigh_info['weigh_report_id'] = self.line_edit_weigh_report_id.text()

        # 设置第一次称重结果
        aircraft.weigh_info['weigh_tyre_nl'][0] = self.gb_tyre_weights_first.dsb_nose_gear_left.value()
        aircraft.weigh_info['weigh_tyre_nr'][0] = self.gb_tyre_weights_first.dsb_nose_gear_right.value()
        aircraft.weigh_info['weigh_tyre_li'][0] = self.gb_tyre_weights_first.dsb_left_main_gear_in.value()
        aircraft.weigh_info['weigh_tyre_lo'][0] = self.gb_tyre_weights_first.dsb_left_main_gear_out.value()
        aircraft.weigh_info['weigh_tyre_ro'][0] = self.gb_tyre_weights_first.dsb_right_main_gear_out.value()
        aircraft.weigh_info['weigh_tyre_ri'][0] = self.gb_tyre_weights_first.dsb_right_main_gear_in.value()

        # 设置第二次称重结果
        aircraft.weigh_info['weigh_tyre_nl'][1] = self.gb_tyre_weights_second.dsb_nose_gear_left.value()
        aircraft.weigh_info['weigh_tyre_nr'][1] = self.gb_tyre_weights_second.dsb_nose_gear_right.value()
        aircraft.weigh_info['weigh_tyre_li'][1] = self.gb_tyre_weights_second.dsb_left_main_gear_in.value()
        aircraft.weigh_info['weigh_tyre_lo'][1] = self.gb_tyre_weights_second.dsb_left_main_gear_out.value()
        aircraft.weigh_info['weigh_tyre_ro'][1] = self.gb_tyre_weights_second.dsb_right_main_gear_out.value()
        aircraft.weigh_info['weigh_tyre_ri'][1] = self.gb_tyre_weights_second.dsb_right_main_gear_in.value()

        # 设置几何参数
        aircraft.weigh_info['weigh_pillar_ln'] = self.dsb_nose_compress_distance.value()
        aircraft.weigh_info['weigh_pillar_lmr'] = self.dsb_right_main_compress_distance.value()
        aircraft.weigh_info['weigh_pillar_lml'] = self.dsb_left_main_compress_distance.value()
        aircraft.weigh_info['pitch_angle'] = self.dsb_pitch_angle.value()

    def translate_ui(self):
        self.gb_weigh_info.setTitle('基本信息')
        self.gb_tyre_weights_first.setTitle('第一次称重地磅称读数*')
        self.gb_tyre_weights_second.setTitle('第二次称重地磅称读数*')
        self.gb_weigh_data.setTitle('其他称重数据*')
        self.label_nose_compress_distance.setText('前起缓冲行程')
        self.label_left_main_compress_distance.setText('左主起缓冲行程')
        self.label_right_main_compress_distance.setText('右主起缓冲行程')
        self.label_pitch_angle.setText('俯仰角')
        self.gb_surplus_units.setTitle('多装件（双击可编辑）')
        self.gb_lack_units.setTitle('缺装件（双击可编辑）')
        self.gb_result_info.setTitle('结果')
        self.label_weigh_date.setText('称重日期')
        self.label_weigh_loc.setText('称重地点')
        self.label_aircraft_type.setText('飞机型号')
        self.label_aircraft_id.setText('架机号')
        self.label_real_weight.setText('实测重量')
        self.label_real_cg.setText('实测重心')
        self.label_empty_weight.setText('试验空机重量')
        self.label_empty_cg.setText('试验空机重心')
        self.btn_cal_weight_cg.setText('计算重量重心')
        self.label_weigh_report_id.setText('重量重心报告号')
