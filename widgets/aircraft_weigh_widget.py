# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter, QPaintEvent, QPainterPath, QMouseEvent
from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QSplitter, QWidget, QVBoxLayout,
                             QGroupBox, QGridLayout, QLabel, QLineEdit, QDialog)

from data_models import data_collector, config_info
from widgets.aircraft_use_item import AircraftUseItemWidget
from widgets.custom_dialog import WeighDialog


class AircraftSketch(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        # 存储轮廓信息
        self.aircraft_path = None

        # 记录变形前的控件尺寸
        self.old_width = self.width()
        self.old_height = self.height()

        # 加载飞机外形数据
        data_collector.load_aircraft_frame_data_from_excel()
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
        x0, y0 = data_collector.aircraft_frame[0]
        # 移动到初始点
        self.aircraft_path.moveTo(*transform_xy(x0, y0))
        for x, y in data_collector.aircraft_frame:
            x, y = transform_xy(x, y)
            self.aircraft_path.lineTo(x, y)
        self.aircraft_path.closeSubpath()

    # 重写鼠标单击事件
    def mousePressEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton:
            if self.weigh_first_btn_area.contains(event.localPos()):
                dialog = WeighDialog()
                result = dialog.exec()
                if result == QDialog.Accepted:
                    pass
            if self.weigh_second_btn_area.contains(event.localPos()):
                print('2')
            event.accept()
        event.ignore()

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

        # 绘制称重的标识
        font = painter.font()
        font.setPixelSize(int(self.width() / 20))
        painter.setFont(font)
        painter.setPen(Qt.white)
        painter.setBrush(Qt.blue)
        self.weigh_first_btn_area = QRectF(6, 6, self.width() / 10, self.width() / 10)
        painter.drawEllipse(self.weigh_first_btn_area)
        painter.drawText(self.weigh_first_btn_area, Qt.AlignCenter, '1')
        painter.setBrush(Qt.green)
        self.weigh_second_btn_area = QRectF(12 + self.width() / 10, 6, self.width() / 10, self.width() / 10)
        painter.drawEllipse(self.weigh_second_btn_area)
        painter.drawText(self.weigh_second_btn_area, Qt.AlignCenter, '2')

        # 绘制6个称重数据显示区域
        font.setPixelSize(int(self.width() / 30))
        painter.setFont(font)
        rect_nose_first = QRectF(self.width() * 0.2, self.height() * 0.15, self.width() * 0.2, self.height() * 0.06)
        painter.fillRect(rect_nose_first, Qt.blue)
        painter.drawText(rect_nose_first, Qt.AlignCenter, 'nl: 2512\nnr: 2842')

        rect_nose_second = QRectF(self.width() * 0.6, self.height() * 0.15, self.width() * 0.2, self.height() * 0.06)
        painter.fillRect(rect_nose_second, Qt.green)
        painter.drawText(rect_nose_second, Qt.AlignCenter, 'nl: 2514\nnr: 2838')

        rect_main_left_first = QRectF(6, self.height() * 0.6, self.width() * 0.2, self.height() * 0.06)
        painter.fillRect(rect_main_left_first, Qt.blue)
        painter.drawText(rect_main_left_first, Qt.AlignCenter, 'lo: 10815\nli: 9780')

        rect_main_left_second = QRectF(self.width() * 0.22, self.height() * 0.6,
                                       self.width() * 0.2, self.height() * 0.06)
        painter.fillRect(rect_main_left_second, Qt.green)
        painter.drawText(rect_main_left_second, Qt.AlignCenter, 'lo: 10820\nli: 9770')

        rect_main_right_first = QRectF(self.width() * 0.57, self.height() * 0.6,
                                       self.width() * 0.2, self.height() * 0.06)
        painter.fillRect(rect_main_right_first, Qt.blue)
        painter.drawText(rect_main_right_first, Qt.AlignCenter, 'ri: 9830\nro: 10820')

        rect_main_right_second = QRectF(self.width() * 0.78, self.height() * 0.6,
                                        self.width() * 0.2, self.height() * 0.06)
        painter.fillRect(rect_main_right_second, Qt.green)
        painter.drawText(rect_main_right_second, Qt.AlignCenter, 'ri: 9825\nro: 10820')

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


class AircraftWeighWidget(QFrame):
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

        # 称重基本信息
        self.gb_weigh_info = QGroupBox(self.widget)
        self.gb_weigh_info.setStyleSheet(config_info.group_box_style)
        self.gridLayout = QGridLayout(self.gb_weigh_info)
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.gridLayout.setSpacing(6)
        self.label_weigh_date = QLabel(self.gb_weigh_info)
        self.label_weigh_date.setStyleSheet(config_info.label_style)
        self.label_weigh_date.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_weigh_date, 0, 0, 1, 1)
        self.line_edit_weigh_date = QLineEdit(self.gb_weigh_info)
        self.line_edit_weigh_date.setStyleSheet(config_info.line_edit_style)
        self.gridLayout.addWidget(self.line_edit_weigh_date, 0, 1, 1, 1)
        self.label_weigh_loc = QLabel(self.gb_weigh_info)
        self.label_weigh_loc.setStyleSheet(config_info.label_style)
        self.label_weigh_loc.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_weigh_loc, 0, 2, 1, 1)
        self.line_edit_weigh_loc = QLineEdit(self.gb_weigh_info)
        self.line_edit_weigh_loc.setStyleSheet(config_info.line_edit_style)
        self.gridLayout.addWidget(self.line_edit_weigh_loc, 0, 3, 1, 1)
        self.label_aircraft_type = QLabel(self.gb_weigh_info)
        self.label_aircraft_type.setStyleSheet(config_info.label_style)
        self.label_aircraft_type.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_aircraft_type, 1, 0, 1, 1)
        self.line_edit_aircraft_type = QLineEdit(self.gb_weigh_info)
        self.line_edit_aircraft_type.setStyleSheet(config_info.line_edit_style)
        self.gridLayout.addWidget(self.line_edit_aircraft_type, 1, 1, 1, 1)
        self.label_aircraft_id = QLabel(self.gb_weigh_info)
        self.label_aircraft_id.setStyleSheet(config_info.label_style)
        self.label_aircraft_id.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_aircraft_id, 1, 2, 1, 1)
        self.line_edit_aircraft_id = QLineEdit(self.gb_weigh_info)
        self.line_edit_aircraft_id.setStyleSheet(config_info.line_edit_style)
        self.gridLayout.addWidget(self.line_edit_aircraft_id, 1, 3, 1, 1)
        self.v_layout.addWidget(self.gb_weigh_info)

        self.h_layout_unit = QHBoxLayout()
        # 多装件信息
        self.gb_surplus_units = AircraftUseItemWidget(self.widget)
        self.gb_surplus_units.setStyleSheet(config_info.group_box_style)
        self.h_layout_unit.addWidget(self.gb_surplus_units)
        self.gb_lack_units = AircraftUseItemWidget(self.widget)
        self.gb_lack_units.setStyleSheet(config_info.group_box_style)
        self.h_layout_unit.addWidget(self.gb_lack_units)
        self.v_layout.addLayout(self.h_layout_unit)

        # 结果信息
        self.gb_result_info = QGroupBox(self.widget)
        self.gb_result_info.setStyleSheet(config_info.group_box_style)
        self.gridLayout_result_info = QGridLayout(self.gb_result_info)
        self.gridLayout_result_info.setContentsMargins(2, 2, 2, 2)
        self.gridLayout_result_info.setSpacing(6)
        self.label_real_weight = QLabel(self.gb_result_info)
        self.label_real_weight.setStyleSheet(config_info.label_style)
        self.label_real_weight.setAlignment(Qt.AlignCenter)
        self.gridLayout_result_info.addWidget(self.label_real_weight, 0, 0, 1, 1)
        self.line_edit_real_weight = QLineEdit(self.gb_result_info)
        self.line_edit_real_weight.setStyleSheet(config_info.line_edit_style)
        self.gridLayout_result_info.addWidget(self.line_edit_real_weight, 0, 1, 1, 1)
        self.label_real_cg = QLabel(self.gb_result_info)
        self.label_real_cg.setStyleSheet(config_info.label_style)
        self.label_real_cg.setAlignment(Qt.AlignCenter)
        self.gridLayout_result_info.addWidget(self.label_real_cg, 0, 2, 1, 1)
        self.line_edit_real_cg = QLineEdit(self.gb_result_info)
        self.line_edit_real_cg.setStyleSheet(config_info.line_edit_style)
        self.gridLayout_result_info.addWidget(self.line_edit_real_cg, 0, 3, 1, 1)
        self.label_empty_weight = QLabel(self.gb_result_info)
        self.label_empty_weight.setStyleSheet(config_info.label_style)
        self.label_empty_weight.setAlignment(Qt.AlignCenter)
        self.gridLayout_result_info.addWidget(self.label_empty_weight, 1, 0, 1, 1)
        self.line_edit_empty_weight = QLineEdit(self.gb_result_info)
        self.line_edit_empty_weight.setStyleSheet(config_info.line_edit_style)
        self.gridLayout_result_info.addWidget(self.line_edit_empty_weight, 1, 1, 1, 1)
        self.label_empty_cg = QLabel(self.gb_result_info)
        self.label_empty_cg.setStyleSheet(config_info.label_style)
        self.label_empty_cg.setAlignment(Qt.AlignCenter)
        self.gridLayout_result_info.addWidget(self.label_empty_cg, 1, 2, 1, 1)
        self.line_edit_empty_cg = QLineEdit(self.gb_result_info)
        self.line_edit_empty_cg.setStyleSheet(config_info.line_edit_style)
        self.gridLayout_result_info.addWidget(self.line_edit_empty_cg, 1, 3, 1, 1)
        self.v_layout.addWidget(self.gb_result_info)

        self.splitter_record.addWidget(self.widget)
        self.splitter_record.setStretchFactor(0, 5)
        self.splitter_record.setStretchFactor(1, 1)

        self.h_layout.addWidget(self.splitter_record)

        self.translate_ui()

    def translate_ui(self):
        self.gb_weigh_info.setTitle('记录信息')
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
