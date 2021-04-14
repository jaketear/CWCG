# -*- coding: utf-8 -*-

import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QResizeEvent
from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QToolButton, QGroupBox,
                             QGraphicsView, QSizePolicy, QGraphicsScene, QSpacerItem,
                             QFileDialog)

from data_models import config_info
from data_models.data_collector import aircraft
from widgets.custom_canvas import WeightCGLimitCanvas
from widgets.custom_tree_view_widget import MatrixDataTree, MultiMatrixTree


# 飞机信息控件
class AircraftInfoWidget(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.h_layout_widget = QHBoxLayout(self)
        self.h_layout_widget.setContentsMargins(0, 0, 0, 0)
        self.v_layout_tool_button = QVBoxLayout()
        self.btn_sel_aircraft_ini = QToolButton(self)
        self.btn_sel_aircraft_ini.setIcon(QIcon(config_info.icon_select_aircraft))
        self.btn_sel_aircraft_ini.setStyleSheet(config_info.button_with_icon_style)
        self.btn_sel_aircraft_ini.setToolTip('选择机型')
        self.v_layout_tool_button.addWidget(self.btn_sel_aircraft_ini)
        self.btn_edit_info = QToolButton(self)
        self.btn_edit_info.setIcon(QIcon(config_info.icon_edit_aircraft_info))
        self.btn_edit_info.setStyleSheet(config_info.button_with_icon_style)
        self.btn_edit_info.setToolTip('修改信息')
        self.v_layout_tool_button.addWidget(self.btn_edit_info)
        self.btn_search_info = QToolButton(self)
        self.btn_search_info.setIcon(QIcon(config_info.icon_search_aircraft_info))
        self.btn_search_info.setStyleSheet(config_info.button_with_icon_style)
        self.btn_search_info.setToolTip('查询信息')
        self.v_layout_tool_button.addWidget(self.btn_search_info)
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.v_layout_tool_button.addItem(spacer_item)
        self.h_layout_widget.addLayout(self.v_layout_tool_button)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        # 飞机基本信息的布局
        self.group_box_aircraft_base_info = QGroupBox(self)
        self.group_box_aircraft_base_info.setStyleSheet(config_info.group_box_style)
        self.group_box_aircraft_base_info.setTitle('飞机基本信息')
        self.v_layout_aircraft_base_info = QVBoxLayout(self.group_box_aircraft_base_info)
        self.v_layout_aircraft_base_info.setContentsMargins(6, 6, 6, 2)
        self.aircraft_base_info_tree = MatrixDataTree(self.group_box_aircraft_base_info)
        self.v_layout_aircraft_base_info.addWidget(self.aircraft_base_info_tree)
        self.horizontalLayout_2.addWidget(self.group_box_aircraft_base_info)

        # 重量重心限制，标签加图的布局
        self.group_box_weigh_cg_limit = QGroupBox(self)
        self.group_box_weigh_cg_limit.setStyleSheet(config_info.group_box_style)
        self.v_layout_weigh_cg_limit = QVBoxLayout(self.group_box_weigh_cg_limit)
        self.v_layout_weigh_cg_limit.setContentsMargins(6, 6, 6, 2)
        self.weigh_cg_limit_graph = WeightCGLimitCanvas(self.group_box_weigh_cg_limit)
        self.v_layout_weigh_cg_limit.addWidget(self.weigh_cg_limit_graph)
        self.horizontalLayout_2.addWidget(self.group_box_weigh_cg_limit)

        # 起飞配平布局
        self.group_box_trim_value = QGroupBox(self)
        self.group_box_trim_value.setStyleSheet(config_info.group_box_style)
        self.v_layout_trim_value = QVBoxLayout(self.group_box_trim_value)
        self.v_layout_trim_value.setContentsMargins(6, 6, 6, 2)
        self.take_off_trim_value_tree = MultiMatrixTree(self.group_box_trim_value)
        self.v_layout_trim_value.addWidget(self.take_off_trim_value_tree)
        self.horizontalLayout_2.addWidget(self.group_box_trim_value)

        # 飞机项目重量重心布局
        self.group_box_major_stowage = QGroupBox(self)
        self.group_box_major_stowage.setStyleSheet(config_info.group_box_style)
        self.v_layout_major_stowage = QVBoxLayout(self.group_box_major_stowage)
        self.v_layout_major_stowage.setContentsMargins(6, 6, 6, 2)
        self.major_stowage_info_tree = MatrixDataTree(self.group_box_major_stowage)
        self.major_stowage_info_tree.header().setHidden(False)
        self.v_layout_major_stowage.addWidget(self.major_stowage_info_tree)
        self.horizontalLayout_2.addWidget(self.group_box_major_stowage)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        # 飞机框位图
        self.group_box_frame_graph = QGroupBox(self)
        self.group_box_frame_graph.setStyleSheet(config_info.group_box_style)
        self.h_layout_bottom = QHBoxLayout(self.group_box_frame_graph)
        self.h_layout_bottom.setContentsMargins(6, 6, 6, 2)
        self.aircraft_frame_graph_scene = QGraphicsScene(self)
        self.aircraft_frame_graph = QGraphicsView(self.aircraft_frame_graph_scene, self)
        # 不显示滚动条
        self.aircraft_frame_graph.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.aircraft_frame_graph.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.h_layout_bottom.addWidget(self.aircraft_frame_graph)
        self.verticalLayout_3.addWidget(self.group_box_frame_graph)

        self.h_layout_widget.addLayout(self.verticalLayout_3)

        self.translate()

        self.display_aircraft_info()

        # 连接信号与槽
        self.btn_sel_aircraft_ini.clicked.connect(self.sel_aircraft_info_file)

    # 显示飞机信息
    def display_aircraft_info(self):
        weight_cg_limit_content = '飞机重量重心限制'
        if aircraft.aircraft_type and aircraft.aircraft_id:
            weight_cg_limit_content = aircraft.aircraft_type + '(' + aircraft.aircraft_id + ')'\
                                      + weight_cg_limit_content
        self.group_box_weigh_cg_limit.setTitle(weight_cg_limit_content)
        self.aircraft_base_info_tree.display_info(aircraft.get_aircraft_base_info(), ['飞机基本信息', ''])
        self.take_off_trim_value_tree.display_info(aircraft.take_off_trim_value, ['重心(%MAC)', '配平值(°)'])
        self.major_stowage_info_tree.display_info(aircraft.major_stowage_data, ['名称', '重量(kg)', '力臂(mm)'])
        self.weigh_cg_limit_graph.plot_curve()
        self.display_aircraft_frame_pic()

    # 显示框位图片
    def display_aircraft_frame_pic(self):
        w = self.aircraft_frame_graph.geometry().width()
        h = self.aircraft_frame_graph.geometry().height()
        if w and h:
            if os.path.isfile(aircraft.aircraft_frame_pic_path):
                self.aircraft_frame_graph_scene.clear()
                temp_png_pixmap = QPixmap(aircraft.aircraft_frame_pic_path)
                temp_png_pixmap = temp_png_pixmap.scaled(w, h, transformMode=Qt.SmoothTransformation)
                self.aircraft_frame_graph_scene.addPixmap(temp_png_pixmap)
                self.aircraft_frame_graph_scene.setSceneRect(self.aircraft_frame_graph_scene.itemsBoundingRect())

    # 窗口缩放时也缩放框位图片
    def resizeEvent(self, event: QResizeEvent):
        self.display_aircraft_frame_pic()
        QFrame.resizeEvent(self, event)

    # 选择飞机信息文件
    def sel_aircraft_info_file(self):
        filename, temp = QFileDialog.getOpenFileName(self, "选择飞机数据文件", ".\\", "数据文件(*.ini)")
        if filename:
            filename = os.path.normpath(filename)
            # 处理文件

    def translate(self):
        self.group_box_trim_value.setTitle('起飞水平安定面配平')
        self.group_box_major_stowage.setTitle('部件重量重心')
        self.group_box_frame_graph.setTitle('飞机框位图')
