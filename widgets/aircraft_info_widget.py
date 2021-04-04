# -*- coding: utf-8 -*-

import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QResizeEvent
from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QToolButton,
                             QGraphicsView, QLabel, QComboBox, QSpacerItem, QSizePolicy,
                             QGraphicsScene, QFileDialog, QMessageBox)

from data_models import config_info
from data_models.data_collector import aircraft
from widgets.custom_canvas import WeightCGLimitCanvas
from widgets.custom_tree_view_widget import MatrixDataTree, MultiMatrixTree


# 飞机信息控件
class AircraftInfoWidget(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.verticalLayout_3 = QVBoxLayout(self)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        
        # 飞机基本信息的布局
        self.verticalLayout = QVBoxLayout()
        self.btn_import_aircraft_ini = QToolButton(self)
        self.btn_import_aircraft_ini.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.btn_import_aircraft_ini.setIcon(QIcon(config_info.icon_select_aircraft))
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.btn_import_aircraft_ini.sizePolicy().hasHeightForWidth())
        self.btn_import_aircraft_ini.setSizePolicy(size_policy)
        self.btn_import_aircraft_ini.setStyleSheet(config_info.button_style)
        self.verticalLayout.addWidget(self.btn_import_aircraft_ini)
        self.aircraft_base_info_tree = MatrixDataTree(self)
        self.verticalLayout.addWidget(self.aircraft_base_info_tree)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        # 重量重心限制，标签加图的布局
        self.v_layout_weigh_cg_limit = QVBoxLayout()
        self.v_layout_weigh_cg_limit.setSpacing(0)
        self.label_weigh_cg_limit = QLabel(self)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.label_weigh_cg_limit.sizePolicy().hasHeightForWidth())
        self.label_weigh_cg_limit.setSizePolicy(size_policy)
        self.label_weigh_cg_limit.setStyleSheet(config_info.aircraft_title_label_style)
        self.v_layout_weigh_cg_limit.addWidget(self.label_weigh_cg_limit)
        self.weigh_cg_limit_graph = WeightCGLimitCanvas(self)
        self.v_layout_weigh_cg_limit.addWidget(self.weigh_cg_limit_graph)
        self.horizontalLayout_2.addLayout(self.v_layout_weigh_cg_limit)

        # 起飞配平布局
        self.v_layout_trim_value = QVBoxLayout()
        self.v_layout_trim_value.setSpacing(4)
        self.label_trim_value = QLabel(self)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.label_trim_value.sizePolicy().hasHeightForWidth())
        self.label_trim_value.setSizePolicy(size_policy)
        self.label_trim_value.setStyleSheet(config_info.aircraft_title_label_style)
        self.v_layout_trim_value.addWidget(self.label_trim_value)
        self.take_off_trim_value_tree = MultiMatrixTree(self)
        self.v_layout_trim_value.addWidget(self.take_off_trim_value_tree)
        self.horizontalLayout_2.addLayout(self.v_layout_trim_value)

        # 飞机项目重量重心布局
        self.v_layout_major_stowage = QVBoxLayout()
        self.v_layout_major_stowage.setSpacing(4)
        self.label_major_stowage = QLabel(self)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.label_major_stowage.sizePolicy().hasHeightForWidth())
        self.label_major_stowage.setSizePolicy(size_policy)
        self.label_major_stowage.setStyleSheet(config_info.aircraft_title_label_style)
        self.v_layout_major_stowage.addWidget(self.label_major_stowage)
        self.major_stowage_info_tree = MatrixDataTree(self)
        self.v_layout_major_stowage.addWidget(self.major_stowage_info_tree)
        self.horizontalLayout_2.addLayout(self.v_layout_major_stowage)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.h_layout_bottom = QHBoxLayout()
        self.aircraft_frame_graph_scene = QGraphicsScene(self)
        self.aircraft_frame_graph = QGraphicsView(self.aircraft_frame_graph_scene, self)
        # 不显示滚动条
        self.aircraft_frame_graph.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.aircraft_frame_graph.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.h_layout_bottom.addWidget(self.aircraft_frame_graph)

        self.verticalLayout_2 = QVBoxLayout()
        self.label_frame_name = QLabel(self)
        self.label_frame_name.setStyleSheet(config_info.label_style)
        self.verticalLayout_2.addWidget(self.label_frame_name)
        self.cb_frame_name = QComboBox(self)
        self.cb_frame_name.setStyleSheet(config_info.combo_box_style)
        self.verticalLayout_2.addWidget(self.cb_frame_name)
        self.label_frame_pos_tag = QLabel(self)
        self.label_frame_pos_tag.setStyleSheet(config_info.label_style)
        self.verticalLayout_2.addWidget(self.label_frame_pos_tag)
        self.label_frame_pos = QLabel(self)
        self.label_frame_pos.setStyleSheet(config_info.display_value_label_style)
        self.verticalLayout_2.addWidget(self.label_frame_pos)
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacer_item)
        self.h_layout_bottom.addLayout(self.verticalLayout_2)

        self.verticalLayout_3.addLayout(self.h_layout_bottom)

        self.translate()

        self.display_aircraft_info()

        # 连接信号与槽
        self.btn_import_aircraft_ini.clicked.connect(self.sel_aircraft_info_file)

    # 显示飞机信息
    def display_aircraft_info(self):
        weight_cg_limit_content = '飞机重量重心限制'
        if aircraft.aircraft_type and aircraft.aircraft_id:
            weight_cg_limit_content = aircraft.aircraft_type + '(' + aircraft.aircraft_id + ')'\
                                      + weight_cg_limit_content
        self.label_weigh_cg_limit.setText(weight_cg_limit_content)
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
        self.btn_import_aircraft_ini.setText("选择机型")
        self.label_frame_name.setText("框号")
        self.label_frame_pos_tag.setText("框位mm")
        self.label_frame_pos.setText("0")
        self.label_trim_value.setText('起飞水平安定面配平')
        self.label_major_stowage.setText('部件重量重心')
