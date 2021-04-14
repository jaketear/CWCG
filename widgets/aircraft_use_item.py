# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QVBoxLayout, QGroupBox, QHBoxLayout, QToolButton, QSpacerItem,
                             QSizePolicy, QMessageBox, QFrame)

from data_models import config_info, data_collector
from widgets.custom_tree_view_widget import UseItemTreeView, UseItemTreeDelegate
from widgets.custom_tree_view_model import UseItemTreeModel
from widgets.result_info_show_widget import ResultInfoShowWidget


# 飞机使用项目控件
class AircraftUseItemWidget(QGroupBox):

    def __init__(self, parent=None, item_type='operation item'):
        super().__init__(parent)

        self.item_type = item_type

        self.setStyleSheet(config_info.group_box_style)

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(4, 6, 2, 2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(4)
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
        self.btn_submit = QToolButton(self)
        self.btn_submit.setToolButtonStyle(Qt.ToolButtonTextOnly)
        self.btn_submit.setStyleSheet(config_info.button_style)
        self.btn_submit.setFocusPolicy(Qt.NoFocus)
        self.horizontalLayout.addWidget(self.btn_submit)
        spacer_item = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacer_item)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tree_view_use_item_list = UseItemTreeView(self)
        self.verticalLayout.addWidget(self.tree_view_use_item_list)
        self.tree_model_use_item_list = UseItemTreeModel(list(), self.tree_view_use_item_list)
        self.tree_view_use_item_list.setModel(self.tree_model_use_item_list)
        self.tree_delegate = UseItemTreeDelegate()
        self.tree_view_use_item_list.setItemDelegate(self.tree_delegate)

        self.translate_ui()

        # 连接信号与槽
        self.btn_add_item.clicked.connect(self.add_use_item)
        self.btn_del_item.clicked.connect(self.del_use_item)
        # self.btn_submit.clicked.connect(self.submit_use_item_info)
        self.tree_delegate.signal_edit_finished.connect(self.edit_use_item_signal)

    # 增加使用项目
    def add_use_item(self):
        self.add_use_item_with_data()

    # 增加明确了数据的使用项目
    def add_use_item_with_data(self, item_name='项目', weight=0, arm=0, moment=0):
        position = self.tree_model_use_item_list.rowCount()
        status = self.tree_model_use_item_list.insertRows(position, 1)
        if status:
            widget_index = self.tree_model_use_item_list.index(position, 0)
            item = self.tree_model_use_item_list.getItem(widget_index)
            item.set_data(0, item_name)
            item.set_data(1, weight)
            item.set_data(2, arm)
            item.set_data(3, moment)
            data_collector.aircraft.item_add([item_name, weight, arm, moment], self.item_type)

    # 删除使用项目
    def del_use_item(self):
        cur_index = self.tree_view_use_item_list.currentIndex()
        if cur_index.row() != -1:
            item = self.tree_model_use_item_list.getItem(cur_index)
            item_name = item.data(0)
            message = QMessageBox.warning(self, '删除使用项目', '确定要删除使用项目：' + item_name + ' 吗?',
                                          QMessageBox.Yes | QMessageBox.No)
            if message == QMessageBox.Yes:
                self.tree_model_use_item_list.removeRow(cur_index.row())
                data_collector.aircraft.item_del(cur_index.row(), self.item_type)

    # 删除所有使用项目
    def del_all_use_item(self):
        row_count = self.tree_model_use_item_list.rowCount()
        for i in range(row_count):
            self.tree_model_use_item_list.removeRow(row_count - i - 1)
            data_collector.aircraft.item_del(row_count - i - 1, self.item_type)

    # 删除所有项目并显示最新的项目
    def display_items(self):
        items = list()
        if self.item_type == 'operation item':
            items = data_collector.aircraft.stowage_info['operation_items']
        if self.item_type == 'redundant item':
            items = data_collector.aircraft.weigh_info['redundant_unit']
        if self.item_type == 'absence item':
            items = data_collector.aircraft.weigh_info['absence_unit']
        if items:
            self.del_all_use_item()
            for aircraft_item in items:
                position = self.tree_model_use_item_list.rowCount()
                status = self.tree_model_use_item_list.insertRows(position, 1)
                if status:
                    widget_index = self.tree_model_use_item_list.index(position, 0)
                    item = self.tree_model_use_item_list.getItem(widget_index)
                    item.set_data(0, aircraft_item[0])
                    item.set_data(1, aircraft_item[1])
                    item.set_data(2, aircraft_item[2])
                    item.set_data(3, aircraft_item[3])

    # 项目编辑完成
    def edit_use_item_signal(self, index):
        item = self.tree_model_use_item_list.getItem(index)
        data_collector.aircraft.item_edit(index.row(),
                                          [item.data(0), item.data(1), item.data(2), item.data(3)],
                                          self.item_type)

    def translate_ui(self):
        self.setTitle('使用项目（双击可编辑）')
        self.btn_add_item.setText('   添加   ')
        self.btn_del_item.setText('   删除   ')
        self.btn_submit.setText('   提交   ')


class AircraftUseItemPage(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.aircraft_use_item = AircraftUseItemWidget(self)
        self.verticalLayout.addWidget(self.aircraft_use_item)
        self.show_result_info_widget = ResultInfoShowWidget()
        self.verticalLayout.addWidget(self.show_result_info_widget)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
