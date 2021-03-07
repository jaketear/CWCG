# -*- coding: utf-8 -*-

import sys
import re
import os

from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QToolButton, QSpacerItem, QSizePolicy, QGroupBox,
                             QTabWidget, QMenuBar, QMenu, QAction, QMessageBox, QFileDialog)

from widgets.aircraft_fuel_tank_widget import AircraftFuelTankWidget
from widgets.weigh_widget import AircraftSketch
# from widgets.menu_bar import MenuBar
from widgets.custom_dialog import WeighDialog
from widgets.custom_tree_view_widget import UnitInfoList
from widgets.custom_canvas import FuelConsumptionCanvas
from data_models import config_info, data_collector


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        font = QFont()
        font.setFamily('微软雅黑')
        self.setFont(font)
        self.resize(1050, 600)
        self.setWindowState(Qt.WindowMaximized)
        self.setMinimumSize(QSize(1050, 600))
        self.central_widget = QWidget(self)
        self.verticalLayout_2 = QVBoxLayout(self.central_widget)
        self.horizontalLayout_2 = QHBoxLayout()
        self.fuel_consumption_canvas = FuelConsumptionCanvas(self.central_widget)
        self.horizontalLayout_2.addWidget(self.fuel_consumption_canvas)
        self.widget = QWidget(self.central_widget)
        self.verticalLayout = QVBoxLayout(self.widget)
        self.horizontalLayout = QHBoxLayout()
        self.btn_dow = QToolButton(self.widget)
        self.btn_dow.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.horizontalLayout.addWidget(self.btn_dow)
        spacer_item = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacer_item)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gb_general_info = QGroupBox(self.widget)
        self.verticalLayout_3 = QVBoxLayout(self.gb_general_info)
        # self.widget_2 = QWidget(self.gb_general_info)
        self.widget_2 = AircraftSketch(self.gb_general_info)
        self.verticalLayout_3.addWidget(self.widget_2)
        self.verticalLayout.addWidget(self.gb_general_info)
        self.horizontalLayout_2.addWidget(self.widget)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.tabWidget = QTabWidget(self.central_widget)
        self.tab_pay_load = UnitInfoList()
        # self.verticalLayout_4 = QVBoxLayout(self.tab_pay_load)
        # self.widget_3 = UnitInfoList(self.tab_pay_load)
        # self.verticalLayout_4.addWidget(self.widget_3)
        self.tabWidget.addTab(self.tab_pay_load, "")
        self.tab_trim_load = UnitInfoList()
        # self.verticalLayout_5 = QVBoxLayout(self.tab_trim_load)
        # self.widget_4 = UnitInfoList(self.tab_trim_load)
        # self.verticalLayout_5.addWidget(self.widget_4)
        self.tabWidget.addTab(self.tab_trim_load, "")
        self.tab_fuel = AircraftFuelTankWidget()
        # self.verticalLayout_6 = QVBoxLayout(self.tab_fuel)
        # self.widget_5 = QWidget(self.tab_fuel)
        # self.verticalLayout_6.addWidget(self.widget_5)
        self.tabWidget.addTab(self.tab_fuel, "")
        self.verticalLayout_2.addWidget(self.tabWidget)

        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 1)

        self.setCentralWidget(self.central_widget)
        self.menuBar = QMenuBar(self)
        self.menuBar.setGeometry(QRect(0, 0, 944, 26))
        self.menu_file = QMenu(self.menuBar)
        self.menu_view = QMenu(self.menuBar)
        self.menu_envelop = QMenu(self.menu_view)
        self.menu_tool = QMenu(self.menuBar)
        self.setMenuBar(self.menuBar)
        self.action_save_case = QAction(self)
        self.action_load_case = QAction(self)
        self.action_quit = QAction(self)
        self.action_print_report = QAction(self)
        self.action_print_table = QAction(self)
        self.action_zfw_envelop = QAction(self)
        self.action_take_off_limit = QAction(self)
        self.action_in_flight_limit = QAction(self)
        self.action_landing_limit = QAction(self)
        self.action_fuel_vector = QAction(self)
        self.action_show_grid = QAction(self)
        self.action_dow = QAction(self)
        self.action_trim_sheet = QAction(self)
        self.menu_file.addAction(self.action_save_case)
        self.menu_file.addAction(self.action_load_case)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_print_report)
        self.menu_file.addAction(self.action_print_table)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_quit)
        self.menu_envelop.addAction(self.action_zfw_envelop)
        self.menu_envelop.addAction(self.action_take_off_limit)
        self.menu_envelop.addAction(self.action_in_flight_limit)
        self.menu_envelop.addAction(self.action_landing_limit)
        self.menu_envelop.addAction(self.action_fuel_vector)
        self.menu_view.addAction(self.menu_envelop.menuAction())
        self.menu_view.addSeparator()
        self.menu_view.addAction(self.action_show_grid)
        self.menu_tool.addAction(self.action_dow)
        self.menu_tool.addAction(self.action_trim_sheet)
        self.menuBar.addAction(self.menu_file.menuAction())
        self.menuBar.addAction(self.menu_view.menuAction())
        self.menuBar.addAction(self.menu_tool.menuAction())

        self.translate()
        self.tabWidget.setCurrentIndex(0)

        self.weigh_dialog = WeighDialog(self)
        self.weigh_dialog.setModal(False)
        self.weigh_dialog.hide()

        self.btn_dow.clicked.connect(self.show_weigh_dialog)

        self.action_save_case.triggered.connect(self.save_case)
        self.action_load_case.triggered.connect(self.load_case)

        self.tab_fuel.fuel_tank_control.signal_fuel_change.connect(
            self.fuel_consumption_canvas.refresh_fuel_consume_line_data)
        self.weigh_dialog.signal_refresh_fuel_consume_line.connect(
            self.fuel_consumption_canvas.refresh_fuel_consume_line_data)

    # 导入算例
    def load_case(self):
        tag_dir = config_info.default_weigh_info_import_dir
        case_path, name = QFileDialog.getOpenFileName(self, '导入算例', tag_dir, '算例文件 (*.json)')
        if case_path:
            result_tip = data_collector.load_weigh_info_from_json(case_path)
            # 如果路径改变就对配置信息进行修改保存
            if os.path.dirname(case_path) != config_info.default_weigh_info_import_dir:
                config_info.set_config_info(default_weigh_info_import_dir=os.path.dirname(case_path))
            if result_tip:
                QMessageBox.warning(self, '导入算例', result_tip)
            else:
                self.weigh_dialog.display_weigh_info()
                QMessageBox.information(self, '导入算例',  '导入算例成功！')

    # 保存算例
    def save_case(self):
        tag_path = config_info.default_weigh_info_export_dir + os.sep + 'untitled.json'
        case_path, name = QFileDialog.getSaveFileName(self, '保存算例', tag_path, '算例文件 (*.json)')
        if case_path:
            result_tip = data_collector.export_weight_info_to_json(case_path)
            # 如果路径改变就对配置信息进行修改保存
            if os.path.dirname(case_path) != config_info.default_weigh_info_export_dir:
                config_info.set_config_info(default_weigh_info_export_dir=os.path.dirname(case_path))
            if result_tip:
                QMessageBox.warning(self, '保存算例', result_tip)
            else:
                QMessageBox.information(self, '保存算例',  '保存算例成功！')

    def show_weigh_dialog(self):
        self.weigh_dialog.show()

    def translate(self):
        self.setWindowTitle(config_info.soft_name)
        self.btn_dow.setText("空机数据")
        self.gb_general_info.setTitle("基本信息")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_pay_load), "使用项目")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_trim_load), "配载")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_fuel), "燃油")
        self.menu_file.setTitle("文件")
        self.menu_view.setTitle("视图")
        self.menu_envelop.setTitle("重量重心包线")
        self.menu_tool.setTitle("工具")
        self.action_save_case.setText("保存算例")
        self.action_load_case.setText("导入算例")
        self.action_quit.setText("退出")
        self.action_print_report.setText("打印重量重心报告")
        self.action_print_table.setText("打印重量平衡表")
        self.action_zfw_envelop.setText("零油重量")
        self.action_take_off_limit.setText("起飞限制")
        self.action_in_flight_limit.setText("飞行限制")
        self.action_landing_limit.setText("着陆限制")
        self.action_fuel_vector.setText("燃油消耗曲线")
        self.action_show_grid.setText("网格线")
        self.action_dow.setText("空机重量")
        self.action_trim_sheet.setText("配平表")


if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    app = QApplication(sys.argv)
    # w = AircraftFuelTankWidget()
    # w = WeighDialog()
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
