# -*- coding: utf-8 -*-

import sys
import re

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QStackedWidget, QDialog, QSplitter)

from data_models import config_info, data_collector
from widgets.menu_bar import MenuBar
from widgets.aircraft_fuel_tank_widget import AircraftFuelTankWidget
from widgets.aircraft_weigh_widget import AircraftWeighWidget
from widgets.aircraft_info_widget import AircraftInfoWidget
from widgets.aircraft_use_item import AircraftUseItemWidget
from widgets.aircraft_reports_widget import AircraftReportsWidget
from widgets.aircraft_stowage import AircraftStowageWidget
from widgets.result_info_show_widget import ResultInfoShowWidget
from widgets.login_dialog import LoginDialog


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
        self.work_flow_stacked_widget = QStackedWidget(self.central_widget)
        # 飞机信息
        self.page_aircraft_info = AircraftInfoWidget()
        self.work_flow_stacked_widget.addWidget(self.page_aircraft_info)
        # 称重
        self.page_weigh = AircraftWeighWidget()
        self.work_flow_stacked_widget.addWidget(self.page_weigh)
        # 配载
        self.page_stowage = AircraftStowageWidget()
        self.work_flow_stacked_widget.addWidget(self.page_stowage)
        # 二级控件
        # self.result_stack_widget = QWidget()
        # self.v_layout = QVBoxLayout(self.result_stack_widget)
        self.splitter_result = QSplitter(self)
        self.splitter_result.setOrientation(Qt.Vertical)
        self.work_flow_stacked_widget_second = QStackedWidget()
        # 使用项目
        self.page_use_item = AircraftUseItemWidget()
        self.page_use_item.display_items()
        self.work_flow_stacked_widget_second.addWidget(self.page_use_item)
        # 燃油
        self.page_fuel = AircraftFuelTankWidget()
        self.work_flow_stacked_widget_second.addWidget(self.page_fuel)
        self.splitter_result.addWidget(self.work_flow_stacked_widget_second)
        self.show_result_info_widget = ResultInfoShowWidget()
        self.splitter_result.addWidget(self.show_result_info_widget)
        self.splitter_result.setStretchFactor(0, 2)
        self.splitter_result.setStretchFactor(1, 3)
        self.work_flow_stacked_widget.addWidget(self.splitter_result)
        # 报告
        self.page_report = AircraftReportsWidget()
        self.work_flow_stacked_widget.addWidget(self.page_report)
        self.verticalLayout.addWidget(self.work_flow_stacked_widget)
        self.setCentralWidget(self.central_widget)

        self.menu_bar.signal_selected_item_change.connect(self.change_page)

        # 称重信息改变时重量重心结果也改变
        self.page_weigh.signal_weigh_info_change.connect(self.weigh_info_changed)

        # 油量改变时重量重心结果也改变
        self.page_fuel.fuel_tank_control.signal_fuel_change.connect(self.fuel_info_changed)

        # 提交使用项目时重量重心结果也改变
        self.page_use_item.btn_submit.clicked.connect(self.use_item_changed)

        # 保存重量平衡表

        self.translate()

        # 设置启动时显示的机型信息界面
        self.work_flow_stacked_widget.setCurrentIndex(0)

    # 改变页面
    def change_page(self, index):
        if index in [0, 1, 2, 5]:
            if index == 5:
                index -= 1
            self.work_flow_stacked_widget.setCurrentIndex(index)
        else:
            self.work_flow_stacked_widget.setCurrentIndex(3)
            self.work_flow_stacked_widget_second.setCurrentIndex(index - 3)

    # 燃油信息改变时更新结果并显示
    def fuel_info_changed(self):
        fuel_consumption_sum, cg_real_time = data_collector.aircraft.get_fuel_consume_data()
        aircraft_weight_info = data_collector.aircraft.get_aircraft_weight_info()
        # 导出相应的燃油数据
        data_collector.aircraft.export_stowage_load_fuel_info_to_json(file_dir='')
        self.show_result_info_widget.update_display_result(
            fuel_consumption_sum, cg_real_time, aircraft_weight_info)

    def translate(self):
        self.setWindowTitle(config_info.soft_name)

    # 使用项目信息改变时更新结果并显示
    def use_item_changed(self):
        fuel_consumption_sum, cg_real_time = data_collector.aircraft.get_fuel_consume_data()
        aircraft_weight_info = data_collector.aircraft.get_aircraft_weight_info()
        # 导出相应的项目数据
        data_collector.aircraft.export_stowage_load_fuel_info_to_json(file_dir='')
        self.show_result_info_widget.update_display_result(
            fuel_consumption_sum, cg_real_time, aircraft_weight_info)

    # 称重信息改变时更新结果并显示
    def weigh_info_changed(self):
        fuel_consumption_sum, cg_real_time = data_collector.aircraft.get_fuel_consume_data()
        aircraft_weight_info = data_collector.aircraft.get_aircraft_weight_info()
        self.show_result_info_widget.update_display_result(
            fuel_consumption_sum, cg_real_time, aircraft_weight_info)


if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    app = QApplication(sys.argv)
    # w = MainWindow()
    # w.show()
    # sys.exit(app.exec_())
    # 先弹出登录界面
    login_dialog = LoginDialog()
    result = login_dialog.exec_()
    if result == QDialog.Accepted:
        w = MainWindow()
        w.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)
