# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QVBoxLayout, QGroupBox, QHBoxLayout, QToolButton, QSpacerItem,
                             QSizePolicy, QMessageBox)

from data_models import config_info, data_collector
from widgets.custom_tree_view_widget import UseItemTreeView, UseItemTreeDelegate
from widgets.custom_tree_view_model import UseItemTreeModel


# 飞机使用项目控件
class AircraftUseItemWidget(QGroupBox):

    def __init__(self, parent=None):
        super().__init__(parent)

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
        position = self.tree_model_use_item_list.rowCount()
        status = self.tree_model_use_item_list.insertRows(position, 1)
        if status:
            widget_index = self.tree_model_use_item_list.index(position, 0)
            item = self.tree_model_use_item_list.getItem(widget_index)
            item.set_data(0, '项目')
            item.set_data(1, '0')
            item.set_data(2, '0')
            item.set_data(3, '0')
            data_collector.aircraft.operation_item_add(['项目', 0, 0, 0, 0])

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
                data_collector.aircraft.operation_item_del(cur_index.row())

    # 项目编辑完成
    def edit_use_item_signal(self, index):
        item = self.tree_model_use_item_list.getItem(index)
        data_collector.aircraft.operation_item_edit(index.row(), [item.data(0), float(item.data(1)),
                                                                  float(item.data(2)), float(item.data(3)), 0])

    def translate_ui(self):
        self.setTitle('使用项目（双击可编辑）')
        self.btn_add_item.setText('   添加   ')
        self.btn_del_item.setText('   删除   ')
        self.btn_submit.setText('   提交   ')
