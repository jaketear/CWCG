# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QGroupBox, QFrame, QVBoxLayout

from data_models import config_info
from widgets.result_info_show_widget import ResultInfoShowWidget


# 飞机使用项目控件
class AircraftReportsWidget(QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet(config_info.group_box_style)

        self.translate_ui()

    def translate_ui(self):
        self.setTitle('生成报告')


class AircraftReportsPage(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.aircraft_use_item = AircraftReportsWidget(self)
        self.verticalLayout.addWidget(self.aircraft_use_item)
        self.show_result_info_widget = ResultInfoShowWidget()
        self.verticalLayout.addWidget(self.show_result_info_widget)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)

