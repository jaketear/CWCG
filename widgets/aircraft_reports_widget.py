# -*- coding: utf-8 -*-

import os

from PyQt5.QtCore import Qt, QDate, pyqtSignal
from PyQt5.QtWidgets import (QGroupBox, QToolButton, QVBoxLayout, QSizePolicy, QSpacerItem,
                             QFileDialog, QGridLayout, QLabel, QLineEdit, QDateEdit,
                             QAbstractSpinBox, QDoubleSpinBox, QMessageBox)

from data_models import config_info, data_collector, weightBalanceSheet


# 重量重心报告
class WeighReport(QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setTitle('重量重心报告')
        self.setStyleSheet(config_info.group_box_style)
        self.v_layout = QVBoxLayout(self)
        self.btn_weigh_report = QToolButton(self)
        self.btn_weigh_report.setText('生成重量重心报告')
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.btn_weigh_report.setSizePolicy(size_policy)
        self.btn_weigh_report.setStyleSheet(config_info.button_style)
        self.v_layout.addWidget(self.btn_weigh_report)


# 配载单
class ALSReport(QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setTitle('配载单')
        self.setStyleSheet(config_info.group_box_style)
        self.v_layout = QVBoxLayout(self)
        self.btn_als_report = QToolButton(self)
        self.btn_als_report.setText('生成配载单')
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.btn_als_report.setSizePolicy(size_policy)
        self.btn_als_report.setStyleSheet(config_info.button_style)
        self.v_layout.addWidget(self.btn_als_report)


# 自定义文本控件
class CustomLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet(config_info.label_style)
        self.setAlignment(Qt.AlignRight | Qt.AlignVCenter)


# 自定义文本输入控件
class CustomLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet(config_info.line_edit_style)


# 自定义的数值输入框
class CustomDoubleSpinBox(QDoubleSpinBox):
    def __init__(self, parent=None, decimals=0, minimum=0, maximum=100, suffix=' 人'):
        super().__init__(parent)

        self.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.setDecimals(decimals)
        self.setMaximum(maximum)
        self.setMinimum(minimum)
        self.setSuffix(suffix)
        self.setStyleSheet(config_info.double_spin_style)


# 重量平衡表
class WABSheet(QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setTitle('重量平衡表')
        self.setStyleSheet(config_info.group_box_style)
        self.v_layout = QVBoxLayout(self)

        self.gb_base_info = QGroupBox(self)
        self.gridLayout = QGridLayout(self.gb_base_info)
        self.label_aircraft = CustomLabel(self.gb_base_info)
        self.gridLayout.addWidget(self.label_aircraft, 0, 0, 1, 1)
        self.line_edit_aircraft = CustomLineEdit(self.gb_base_info)
        self.gridLayout.addWidget(self.line_edit_aircraft, 0, 1, 1, 1)
        self.label_task_id = CustomLabel(self.gb_base_info)
        self.gridLayout.addWidget(self.label_task_id, 0, 2, 1, 1)
        self.line_edit_task_id = CustomLineEdit(self.gb_base_info)
        self.gridLayout.addWidget(self.line_edit_task_id, 0, 3, 1, 1)
        self.label_test_type = CustomLabel(self.gb_base_info)
        self.gridLayout.addWidget(self.label_test_type, 0, 4, 1, 1)
        self.line_edit_test_type = CustomLineEdit(self.gb_base_info)
        self.gridLayout.addWidget(self.line_edit_test_type, 0, 5, 1, 1)
        self.label_wab_id = CustomLabel(self.gb_base_info)
        self.gridLayout.addWidget(self.label_wab_id, 1, 0, 1, 1)
        self.line_edit_wab_id = CustomLineEdit(self.gb_base_info)
        self.gridLayout.addWidget(self.line_edit_wab_id, 1, 1, 1, 1)
        self.label_weigh_basis = CustomLabel(self.gb_base_info)
        self.gridLayout.addWidget(self.label_weigh_basis, 1, 2, 1, 1)
        self.line_edit_weigh_basis = CustomLineEdit(self.gb_base_info)
        self.gridLayout.addWidget(self.line_edit_weigh_basis, 1, 3, 1, 1)
        self.label_crew_num = CustomLabel(self.gb_base_info)
        self.gridLayout.addWidget(self.label_crew_num, 1, 4, 1, 1)
        self.dsb_crew_num = CustomDoubleSpinBox(self.gb_base_info)
        self.gridLayout.addWidget(self.dsb_crew_num, 1, 5, 1, 1)
        self.label_wab_version = CustomLabel(self.gb_base_info)
        self.gridLayout.addWidget(self.label_wab_version, 2, 0, 1, 1)
        self.line_edit_wab_version = CustomLineEdit(self.gb_base_info)
        self.gridLayout.addWidget(self.line_edit_wab_version, 2, 1, 1, 1)
        self.label_als_basis = CustomLabel(self.gb_base_info)
        self.gridLayout.addWidget(self.label_als_basis, 2, 2, 1, 1)
        self.line_edit_als_basis = CustomLineEdit(self.gb_base_info)
        self.gridLayout.addWidget(self.line_edit_als_basis, 2, 3, 1, 1)
        self.label_write_date = CustomLabel(self.gb_base_info)
        self.gridLayout.addWidget(self.label_write_date, 2, 4, 1, 1)
        self.date_edit_weigh_date = QDateEdit(self.gb_base_info)
        self.date_edit_weigh_date.setStyleSheet(config_info.date_edit_style)
        self.date_edit_weigh_date.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.gridLayout.addWidget(self.date_edit_weigh_date, 2, 5, 1, 1)
        self.v_layout.addWidget(self.gb_base_info)

        self.btn_wab_sheet = QToolButton(self)
        self.btn_wab_sheet.setText('生成重量平衡表')
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.btn_wab_sheet.setSizePolicy(size_policy)
        self.btn_wab_sheet.setStyleSheet(config_info.button_style)
        self.v_layout.addWidget(self.btn_wab_sheet)

        self.translate_ui()

        self.init_display()

    def init_display(self):
        self.line_edit_aircraft.setText(data_collector.aircraft.aircraft_type + '/' +
                                        data_collector.aircraft.aircraft_id)
        self.line_edit_weigh_basis.setText(data_collector.aircraft.weigh_info['weigh_report_id'])
        self.date_edit_weigh_date.setDate(QDate().currentDate())
        self.line_edit_wab_version.setText('A')

    def translate_ui(self):
        self.gb_base_info.setTitle("基本信息")
        self.label_aircraft.setText("机型/架机")
        self.label_task_id.setText("任务单编号")
        self.label_test_type.setText("试验内容")
        self.label_wab_id.setText("重量平衡表编号")
        self.label_weigh_basis.setText("称重依据")
        self.label_crew_num.setText("上机人数")
        self.label_wab_version.setText("重量平衡表版本")
        self.label_als_basis.setText("配载数据依据")
        self.label_write_date.setText("编制日期")


# 报告控件
class AircraftReportsWidget(QGroupBox):
    signal_export_wab_sheet = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet(config_info.group_box_style)
        self.v_layout = QVBoxLayout(self)
        self.weigh_report = WeighReport()
        self.v_layout.addWidget(self.weigh_report)
        self.als_report = ALSReport()
        self.v_layout.addWidget(self.als_report)
        self.wab_sheet = WABSheet()
        self.v_layout.addWidget(self.wab_sheet)
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.v_layout.addItem(spacer_item)

        self.translate_ui()
        self.weigh_report.btn_weigh_report.clicked.connect(self.select_save_dir)
        self.wab_sheet.btn_wab_sheet.clicked.connect(self.select_save_dir)
        self.als_report.btn_als_report.clicked.connect(self.select_save_dir)

    def get_wab_sheet_info(self):
        aircraft = self.wab_sheet.line_edit_aircraft.text()
        wab_id = self.wab_sheet.line_edit_wab_id.text()
        wab_version = self.wab_sheet.line_edit_wab_version.text()
        task_id = self.wab_sheet.line_edit_task_id.text()
        weigh_basis = self.wab_sheet.line_edit_weigh_basis.text()
        als_basis = self.wab_sheet.line_edit_als_basis.text()
        test_type = self.wab_sheet.line_edit_test_type.text()
        crew_num = self.wab_sheet.dsb_crew_num.text()
        date = self.wab_sheet.date_edit_weigh_date.date().toString('yyyy/MM/dd')

        return save_dir, aircraft, wab_id, wab_version, task_id, weigh_basis, als_basis, test_type, crew_num, date

    # 选择保存路径
    def select_save_dir(self):
        sender = self.sender()
        open_dir = config_info.current_dir
        if sender == self.weigh_report.btn_weigh_report and os.path.isdir(config_info.weigh_report_save_dir):
            open_dir = config_info.weigh_report_save_dir
        if sender == self.als_report.btn_als_report and os.path.isdir(config_info.als_report_save_dir):
            open_dir = config_info.als_report_save_dir
        if sender == self.wab_sheet.btn_wab_sheet and os.path.isdir(config_info.wab_sheet_save_dir):
            open_dir = config_info.wab_sheet_save_dir
        save_dir = QFileDialog.getExistingDirectory(self, "保存文件", open_dir)
        if os.path.isdir(save_dir):
            if sender == self.weigh_report.btn_weigh_report:
                config_info.set_config_info(weigh_report_save_dir=save_dir)
            if sender == self.als_report.btn_als_report:
                config_info.set_config_info(als_report_save_dir=save_dir)
            if sender == self.wab_sheet.btn_wab_sheet:
                config_info.set_config_info(wab_sheet_save_dir=save_dir)
                self.signal_export_wab_sheet.emit()

                result_tip = weightBalanceSheet.export_wab_sheet(save_dir, aircraft, wab_id, wab_version,
                                                                 task_id, weigh_basis, als_basis, test_type,
                                                                 crew_num, date)
                if result_tip:
                    QMessageBox.information(self, '提示', result_tip)
                else:
                    QMessageBox.information(self, '提示', '生成重量平衡表成功！')

    def translate_ui(self):
        self.setTitle('生成报告')
