# -*- coding: utf-8 -*-

import sys
import re

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QStackedWidget, QHBoxLayout, QTreeView)

from data_models import config_info
from widgets.menu_bar import MenuBar
from widgets.fuel_consumption_canvas import FuelConsumptionCanvas
from widgets.aircraft_fuel_tank import AircraftFuelTankWidget
from widgets.weigh_widget import AircraftSketch
from widgets.custom_tree_view_widget import WeightInfoTree


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        font = QFont()
        font.setFamily('微软雅黑')
        self.setFont(font)
        self.resize(1050, 600)
        self.setWindowState(Qt.WindowMaximized)
        self.setMinimumSize(QSize(1050, 600))
        self.setWindowIcon(QIcon(config_info.icon_main_window))

        self.central_widget = QWidget(self)
        self.verticalLayout = QVBoxLayout(self.central_widget)
        self.menu_bar = MenuBar(self.central_widget)
        self.verticalLayout.addWidget(self.menu_bar)
        self.verticalLayout_1 = QVBoxLayout(self.central_widget)
        self.work_flow_stacked_widget = QStackedWidget(self.central_widget)
        # 飞机信息
        self.page_aircraft_info = QWidget()
        self.work_flow_stacked_widget.addWidget(self.page_aircraft_info)
        # 称重
        self.page_weigh = AircraftSketch()
        self.work_flow_stacked_widget.addWidget(self.page_weigh)
        # 配载
        self.page_stowage = QWidget()
        self.work_flow_stacked_widget.addWidget(self.page_stowage)
        # 使用项目
        self.page_use_item = QWidget()
        self.work_flow_stacked_widget.addWidget(self.page_use_item)
        # 燃油
        self.page_fuel = AircraftFuelTankWidget()
        self.work_flow_stacked_widget.addWidget(self.page_fuel)
        # 报告
        self.page_report = QWidget()
        self.work_flow_stacked_widget.addWidget(self.page_report)
        self.verticalLayout_1.addWidget(self.work_flow_stacked_widget)
        self.horizontalLayout = QHBoxLayout()
        self.fuel_consumption_canvas = FuelConsumptionCanvas(self.central_widget)
        self.horizontalLayout.addWidget(self.fuel_consumption_canvas)
        self.weight_info = WeightInfoTree(self.central_widget)
        # self.weight_info.display_weight_info([['test1', '1', 'test2', '2', '3'], ['test2', '2', 'test2', '2', '3']])
        self.horizontalLayout.addWidget(self.weight_info)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)
        self.verticalLayout_1.addLayout(self.horizontalLayout)
        self.verticalLayout_1.setStretch(0, 1)
        self.verticalLayout_1.setStretch(1, 1)
        self.verticalLayout.addLayout(self.verticalLayout_1)
        self.setCentralWidget(self.central_widget)

        self.menu_bar.signal_selected_item_change.connect(self.change_work_flow_stack_widget)

        self.translate()

        # 设置启动时显示的机型信息界面
        self.change_work_flow_stack_widget(0)

    # 改变工作流中的界面
    def change_work_flow_stack_widget(self, page_no):
        # 当选择机型和称重界面时不显示燃油消耗曲线和基本重量信息
        if page_no in [0, 1]:
            self.weight_info.setHidden(True)
            self.fuel_consumption_canvas.setHidden(True)
        else:
            self.weight_info.setHidden(False)
            self.fuel_consumption_canvas.setHidden(False)
        self.work_flow_stacked_widget.setCurrentIndex(page_no)

    def translate(self):
        self.setWindowTitle(config_info.soft_name)


if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    app = QApplication(sys.argv)
    # w = AircraftFuelTankWidget()
    # w = WeighDialog()
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
