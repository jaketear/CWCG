# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QFrame, QSplitter, QGroupBox, QHBoxLayout, QVBoxLayout, QToolButton,
                             QSpacerItem, QSizePolicy)

from data_models import config_info, data_collector
from widgets.custom_canvas import FuelConsumptionCanvas
from widgets.custom_tree_view_widget import WeightInfoTree


# 飞机使用项目控件
class ResultInfoShowWidget(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.h_layout = QHBoxLayout(self)
        self.h_layout.setContentsMargins(0, 0, 0, 0)

        self.splitter_record = QSplitter(self)
        self.splitter_record.setOrientation(Qt.Horizontal)

        self.fuel_curve_group_box = QGroupBox(self)
        self.fuel_curve_group_box.setStyleSheet(config_info.group_box_style)
        self.h_layout_fuel_curve = QHBoxLayout(self.fuel_curve_group_box)

        self.v_layout_tool_button = QVBoxLayout()
        self.btn_display_limit = QToolButton(self)
        self.btn_display_limit.setIcon(QIcon(config_info.icon_select_aircraft))
        self.btn_display_limit.setStyleSheet(config_info.button_with_icon_style)
        self.btn_display_limit.setToolTip('显示包线限制')
        self.btn_display_limit.setCheckable(True)
        self.v_layout_tool_button.addWidget(self.btn_display_limit)
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.v_layout_tool_button.addItem(spacer_item)
        self.h_layout_fuel_curve.addLayout(self.v_layout_tool_button)
        
        self.fuel_consumption_canvas = FuelConsumptionCanvas(self)
        self.h_layout_fuel_curve.addWidget(self.fuel_consumption_canvas)
        self.splitter_record.addWidget(self.fuel_curve_group_box)

        self.weight_info_group_box = QGroupBox(self)
        self.weight_info_group_box.setStyleSheet(config_info.group_box_style)
        self.h_layout_weight_info = QHBoxLayout(self.weight_info_group_box)
        self.weight_info = WeightInfoTree(self)
        self.h_layout_weight_info.addWidget(self.weight_info)
        self.splitter_record.addWidget(self.weight_info_group_box)

        self.splitter_record.setStretchFactor(0, 1)
        self.splitter_record.setStretchFactor(1, 2)
        self.h_layout.addWidget(self.splitter_record)

        self.translate_ui()

    def update_display_result(self, fuel_consumption_sum, cg_real_time, aircraft_weight_info):
        self.fuel_consumption_canvas.refresh_fuel_consume_line_data(fuel_consumption_sum, cg_real_time)
        self.weight_info.display_weight_info(aircraft_weight_info)

    def translate_ui(self):
        self.fuel_curve_group_box.setTitle('燃油消耗曲线')
        self.weight_info_group_box.setTitle('飞机重量重心信息')
