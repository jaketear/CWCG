# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import (QTreeWidget, QTreeWidgetItem, QMenu, QAction, QDialog,
                             QMessageBox, QTreeView, QAbstractItemView, QHeaderView,
                             QStyleOptionViewItem)

from widgets.custom_dialog import UnitEditDialog
from data_models import config_info
from widgets.custom_tree_view_model import TreeModelBase
from data_models.data_collector import aircraft_weight_info


class UnitInfoList(QTreeWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # 选择的部件
        self.sel_item = None

        # 添加部件
        self.action_edit_unit = QAction(self)
        self.action_edit_unit.setText('编辑部件')
        self.action_add_unit = QAction(self)
        self.action_add_unit.setText('添加部件')
        self.action_delete_unit = QAction(self)
        self.action_delete_unit.setText('删除部件')
        # 设置三列
        self.setColumnCount(3)
        # 不显示箭头
        self.setRootIsDecorated(False)
        # 设置题头
        header_item = self.headerItem()
        header_item.setText(0, '名称')
        header_item.setText(1, '重量（kg）')
        header_item.setText(2, '力臂（mm）')
        # 让树可支持右键菜单(step 1)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        # 使右键时能弹出菜单(step 2)
        self.customContextMenuRequested.connect(self.on_tree_context_menu)

        self.action_add_unit.triggered.connect(self.add_unit)
        self.action_edit_unit.triggered.connect(self.edit_unit)
        self.action_delete_unit.triggered.connect(self.delete_unit)

    # 添加部件
    def add_unit(self):
        dialog = UnitEditDialog(self)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            item = QTreeWidgetItem()
            item.setText(0, dialog.unit_name)
            item.setText(1, '%.2f' % dialog.unit_weigh)
            item.setText(2, '%.2f' % dialog.unit_loc)
            self.addTopLevelItem(item)

    # 删除部件
    def delete_unit(self):
        if self.sel_item:
            message = QMessageBox.warning(
                self, '删除文件', '确定要删除部件吗？',
                QMessageBox.Yes | QMessageBox.No)
            if message == QMessageBox.Yes:
                self.takeTopLevelItem(self.indexOfTopLevelItem(self.sel_item))

    # 编辑部件
    def edit_unit(self):
        if self.sel_item:
            dialog = UnitEditDialog(self)
            dialog.line_edit_unit_name.setText(self.sel_item.text(0))
            dialog.double_spin_box_unit_weigh.setValue(float(self.sel_item.text(1)))
            dialog.double_spin_box_unit_loc.setValue(float(self.sel_item.text(2)))
            result = dialog.exec_()
            if result == QDialog.Accepted:
                self.sel_item.setText(0, dialog.unit_name)
                self.sel_item.setText(1, '%.2f' % dialog.unit_weigh)
                self.sel_item.setText(2, '%.2f' % dialog.unit_loc)

    # 右键菜单的事件处理(step 3)
    def on_tree_context_menu(self, pos):
        menu = QMenu(self)
        menu.addActions([self.action_edit_unit,
                         self.action_add_unit,
                         self.action_delete_unit])
        self.sel_item = self.itemAt(pos)
        if self.sel_item:
            self.action_edit_unit.setDisabled(False)
            self.action_delete_unit.setDisabled(False)
        else:
            self.action_edit_unit.setDisabled(True)
            self.action_delete_unit.setDisabled(True)
        menu.exec_(self.mapToGlobal(pos))


class WeightInfoTree(QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.tree_model = None

        self.setSelectionMode(QAbstractItemView.SingleSelection)

        # 不显示箭头
        # self.setRootIsDecorated(False)
        # 设置表头
        self.header().setSectionResizeMode(QHeaderView.Stretch)
        self.header().setDefaultAlignment(Qt.AlignCenter)
        # 设置样式
        self.setStyleSheet(config_info.tree_view_style)
        # self.setAlternatingRowColors(True)

        self.display_weight_info()

    # 重载绘制行的函数
    def drawRow(self, painter: QPainter, options: QStyleOptionViewItem, index: QModelIndex):
        opt = QStyleOptionViewItem(options)
        opt.rect.adjust(0, 0, 0, -5)
        QTreeView.drawRow(self, painter, opt, index)

    def display_weight_info(self):
        self.tree_model = TreeModelBase(aircraft_weight_info, self,
                                        header=['项目', '重量(kg)', '力臂(mm)', '力矩(kg*mm)', '重心'])
        self.setModel(self.tree_model)
