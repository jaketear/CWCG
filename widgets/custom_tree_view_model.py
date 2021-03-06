# -*- coding: utf-8 -*-

import re

from PyQt5.QtCore import (Qt, QAbstractItemModel, QModelIndex)


# 树控件的基类
class TreeItemBase(object):

    def __init__(self, data: list, parent_item=None):
        self.child_items = list()
        self.item_data = data
        self.parent_item = parent_item
        # 每列的缺省值
        self.column_value_default = ''

    def append_child(self, item):
        self.child_items.append(item)

    def child(self, row):
        return self.child_items[row]

    def child_count(self):
        return len(self.child_items)

    def column_count(self):
        return len(self.item_data)

    def data(self, column):
        return self.item_data[column]

    def insert_children(self, position, count, columns):
        if position < 0 or position > self.child_count():
            return False
        for row in range(count):
            # 创建的行的数据均为空字符
            data = [self.column_value_default] * columns
            item = TreeItemBase(data, self)
            self.child_items.insert(position, item)
        return True

    def parent(self):
        return self.parent_item

    def remove_children(self, position, count):
        if position < 0 or position + count > self.child_count():
            return False
        for row in range(count):
            self.child_items.pop(position)
        return True

    def row(self):
        if self.parent_item:
            return self.parent_item.child_items.index(self)

    def set_data(self, column, data):
        if column < len(self.item_data):
            self.item_data[column] = data


# tree view模型
class TreeModelBase(QAbstractItemModel):

    # column表示需要设置几列，header是表头名列表，若有表头名就按表头取列数
    def __init__(self, data: dict, parent=None, column=2, header: list = None):
        super().__init__(parent)

        if isinstance(data, dict):
            self.item_data = data
        else:
            self.item_data = dict()

        # 设置表头数据
        if header:
            self.root_data = header
        else:
            self.root_data = [str(i + 1) for i in range(column)]

        self.root_item = TreeItemBase(self.root_data)
        self.setup_model_data(self.item_data, self.root_item)

    def index(self, row: int, column: int, parent: QModelIndex = QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()

        child_item = parent_item.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        else:
            return QModelIndex()

    def columnCount(self, parent: QModelIndex = QModelIndex()):
        if parent.isValid():
            return parent.internalPointer().column_count()
        else:
            return self.root_item.column_count()

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        if role != Qt.DisplayRole:
            return None
        item = index.internalPointer()
        return item.data(index.column())

    def flags(self, index: QModelIndex):
        if not index.isValid():
            return 0
        return QAbstractItemModel.flags(self, index)

    def getItem(self, index):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item
        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.root_item.data(section)
        return None

    def insertRows(self, row: int, count: int, parent: QModelIndex = QModelIndex()):
        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()
        self.beginInsertRows(parent, row, row + count - 1)
        success = parent_item.insert_children(row, count, self.root_item.column_count())
        self.endInsertRows()

        return success

    def parent(self, child: QModelIndex):
        if not child.isValid():
            return QModelIndex()

        child_item = child.internalPointer()
        parent_item = child_item.parent()
        if parent_item == self.root_item:
            return QModelIndex()

        return self.createIndex(parent_item.row(), 0, parent_item)

    def removeRows(self, row: int, count: int, parent: QModelIndex = QModelIndex()):
        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()

        self.beginRemoveRows(parent, row, row + count - 1)
        success = parent_item.remove_children(row, count)
        self.endRemoveRows()

        return success

    def rowCount(self, parent: QModelIndex = QModelIndex()):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()

        return parent_item.child_count()

    @staticmethod
    def setup_model_data(data: dict, root_item):
        if 'major_aircraft_weight' in data:
            for weight_key, weight_value in data['major_aircraft_weight'].items():
                if weight_key == 'operation_item' and 'operation_item' in data and data['operation_item']:
                    operation_item = TreeItemBase(weight_value, root_item)
                    root_item.append_child(operation_item)
                    for item_weight_value in data['operation_item']:
                        operation_item.append_child(TreeItemBase(item_weight_value, operation_item))
                if weight_key == 'stowage_item' and 'stowage_item' in data and data['stowage_item']:
                    stowage_item = TreeItemBase(weight_value, root_item)
                    root_item.append_child(stowage_item)
                    for item_weight_value in data['stowage_item']:
                        stowage_item.append_child(TreeItemBase(item_weight_value, stowage_item))
                if weight_key == 'fuel_item' and 'fuel_item' in data and data['fuel_item']:
                    fuel_item = TreeItemBase(weight_value, root_item)
                    root_item.append_child(fuel_item)
                    for item_weight_value in data['fuel_item']:
                        fuel_item.append_child(TreeItemBase(item_weight_value, fuel_item))
                if weight_key in ['test_empty_weight', 'operation_empty_weight', 'zero_fuel_weight', 'total_weight']:
                    root_item.append_child(TreeItemBase(weight_value, root_item))
        # for data_item in data:
        #     data_list = [data for data in data_item]
        #     root_item.append_child(TreeItemBase(data_list, root_item))
