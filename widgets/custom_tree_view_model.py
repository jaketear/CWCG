# -*- coding: utf-8 -*-

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


# 树模型的基类
class BaseTreeModel(QAbstractItemModel):

    # column表示需要设置几列，header是表头名列表，若有表头名就按表头取列数
    def __init__(self, data=None, parent=None, column=2, header: list = None):
        super().__init__(parent)

        # 设置表头数据
        if header:
            self.root_data = header
        else:
            self.root_data = [str(i + 1) for i in range(column)]

        self.root_item = TreeItemBase(self.root_data)
        self.setup_model_data(data, self.root_item)

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

    def getItem(self, index: QModelIndex):
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
    def setup_model_data(data, root_item):
        raise ValueError('function: setup_model_data , must override.')


# 重量信息树控件对应的模型
class WeightInfoTreeModel(BaseTreeModel):

    # column表示需要设置几列，header是表头名列表，若有表头名就按表头取列数
    def __init__(self, data=None, parent=None, column=2, header: list = None):
        super().__init__(data=data, parent=parent, column=2, header=header)

    @staticmethod
    def setup_model_data(data, root_item):
        if not isinstance(data, dict):
            data = dict()
        if 'major_aircraft_weight' in data:
            for weight_key, weight_value in data['major_aircraft_weight'].items():
                if weight_key == 'operation_item' and 'operation_items' in data and data['operation_items']:
                    operation_item = TreeItemBase(weight_value, root_item)
                    root_item.append_child(operation_item)
                    for item_weight_value in data['operation_item']:
                        operation_item.append_child(TreeItemBase(item_weight_value, operation_item))
                if weight_key == 'stowage_item' and 'stowage_items' in data and data['stowage_items']:
                    stowage_item = TreeItemBase(weight_value, root_item)
                    root_item.append_child(stowage_item)
                    for item_weight_value in data['stowage_item']:
                        stowage_item.append_child(TreeItemBase(item_weight_value, stowage_item))
                if weight_key == 'fuel_item' and 'fuel_items' in data and data['fuel_items']:
                    fuel_item = TreeItemBase(weight_value, root_item)
                    root_item.append_child(fuel_item)
                    for item_weight_value in data['fuel_items']:
                        fuel_item.append_child(TreeItemBase(item_weight_value, fuel_item))
                if weight_key in ['test_empty_weight', 'operation_empty_weight', 'zero_fuel_weight', 'total_weight']:
                    root_item.append_child(TreeItemBase(weight_value, root_item))
        # for data_item in data:
        #     data_list = [data for data in data_item]
        #     root_item.append_child(TreeItemBase(data_list, root_item))


# 矩阵类型数据的模型，如{'test1': [1, 2], 'test2': [2, 3]}
class MatrixDataTreeModel(BaseTreeModel):

    # column表示需要设置几列，header是表头名列表，若有表头名就按表头取列数
    def __init__(self, data=None, parent=None, column=2, header: list = None):
        super().__init__(data=data, parent=parent, column=column, header=header)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid():
            return None
        if role != Qt.DisplayRole:
            return None
        item = index.internalPointer()
        return item.data(index.column())

    @staticmethod
    def setup_model_data(data, root_item):
        if isinstance(data, dict):
            for key, value in data.items():
                if not isinstance(value, list):
                    root_item.append_child(TreeItemBase([key, value], root_item))
                else:
                    value.insert(0, key)
                    root_item.append_child(TreeItemBase(value, root_item))


# 多个矩阵的模型，如{'test1': [[2, 3], [2, 3]], 'test2': [[2, 3], [2, 3]]}
class MultiMatrixTreeModel(BaseTreeModel):

    # column表示需要设置几列，header是表头名列表，若有表头名就按表头取列数
    def __init__(self, data=None, parent=None, column=2, header: list = None):
        super().__init__(data=data, parent=parent, column=column, header=header)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid():
            return None
        if role != Qt.DisplayRole:
            return None
        item = index.internalPointer()
        return item.data(index.column())

    def setup_model_data(self, data, root_item):
        if not isinstance(data, dict):
            data = dict()
        if len(data) != 1:
            col_count = self.columnCount()
            for key, value in data.items():
                null_data_list = ['' for i in range(col_count)]
                null_data_list[0] = key
                parent_item = TreeItemBase(null_data_list, root_item)
                root_item.append_child(parent_item)
                for item_weight_value in data[key]:
                    parent_item.append_child(TreeItemBase(item_weight_value, parent_item))
        else:
            for key, value in data.items():
                for item_weight_value in data[key]:
                    root_item.append_child(TreeItemBase(item_weight_value, root_item))


# 使用项目树模型
class UseItemTreeModel(BaseTreeModel):

    def __init__(self, data_list: list, parent=None):
        super().__init__(data_list, parent, header=['使用项目', '重量(kg)', '力臂(mm)', '力矩(kg*mm)'])

    # 让item可编辑
    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsSelectable | Qt.ItemIsEnabled

    # 重载函数，让item可编辑
    def setData(self, index, value, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                item = index.internalPointer()
                item.set_data(index.column(), value)
                return True

        return False

    @staticmethod
    def setup_model_data(data: list, root_item):
        for data_item in data:
            data_list = [data for data in data_item]
            root_item.append_child(TreeItemBase(data_list, root_item))
