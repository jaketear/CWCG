# -*- coding: utf-8 -*-

import sys
import re

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QStackedWidget, QDialog)

from data_models import config_info
from widgets.menu_bar import MenuBar
from widgets.aircraft_fuel_tank_widget import AircraftFuelTankPage
from widgets.aircraft_weigh_widget import AircraftWeighWidget
from widgets.aircraft_info_widget import AircraftInfoWidget
from widgets.aircraft_use_item import AircraftUseItemPage
from widgets.aircraft_reports_widget import AircraftReportsPage
from widgets.aircraft_stowage import AircraftStowageWidget
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
        # 使用项目
        self.page_use_item = AircraftUseItemPage()
        self.work_flow_stacked_widget.addWidget(self.page_use_item)
        # 燃油
        self.page_fuel = AircraftFuelTankPage()
        self.work_flow_stacked_widget.addWidget(self.page_fuel)
        # 报告
        self.page_report = AircraftReportsPage()
        self.work_flow_stacked_widget.addWidget(self.page_report)

        self.verticalLayout.addWidget(self.work_flow_stacked_widget)
        self.setCentralWidget(self.central_widget)

        self.menu_bar.signal_selected_item_change.connect(self.work_flow_stacked_widget.setCurrentIndex)

        self.page_fuel.aircraft_fuel_tank.fuel_tank_control.signal_fuel_change.connect(
            self.page_fuel.show_result_info_widget.fuel_consumption_canvas.refresh_fuel_consume_line_data)
        self.page_fuel.aircraft_fuel_tank.fuel_tank_control.signal_fuel_change.connect(
            self.page_report.show_result_info_widget.fuel_consumption_canvas.refresh_fuel_consume_line_data)
        self.page_fuel.aircraft_fuel_tank.fuel_tank_control.signal_fuel_change.connect(
            self.page_use_item.show_result_info_widget.fuel_consumption_canvas.refresh_fuel_consume_line_data)

        self.translate()

        # 设置启动时显示的机型信息界面
        self.work_flow_stacked_widget.setCurrentIndex(0)

    def translate(self):
        self.setWindowTitle(config_info.soft_name)


if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
    # 先弹出登录界面
    # login_dialog = LoginDialog()
    # result = login_dialog.exec_()
    # if result == QDialog.Accepted:
    #     w = MainWindow()
    #     w.show()
    #     sys.exit(app.exec_())
    # else:
    #     sys.exit(0)
