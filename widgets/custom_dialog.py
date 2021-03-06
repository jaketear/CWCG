# -*- coding: utf-8 -*-

from PyQt5.QtCore import QSize, QDateTime, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QDialog, QGridLayout, QLabel, QAbstractSpinBox, QGroupBox,
                             QDoubleSpinBox, QPushButton, QLineEdit, QSpinBox,
                             QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy,
                             QMessageBox, QComboBox, QDateEdit, QTreeWidgetItem)

# from data_models import data_collector
# from widgets.custom_tree_view_widget import UnitInfoList


# 部件编辑对话框
class UnitEditDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 部件信息
        self.unit_name = ''
        self.unit_weigh = 0.0
        self.unit_loc = 0.0

        font = QFont()
        font.setFamily('微软雅黑')
        self.setFont(font)
        self.resize(350, 140)
        self.verticalLayout = QVBoxLayout(self)
        self.gridLayout = QGridLayout()
        self.label_unit_name = QLabel(self)
        self.label_unit_name.setMinimumSize(QSize(120, 0))
        self.label_unit_name.setMaximumSize(QSize(120, 16777215))
        self.gridLayout.addWidget(self.label_unit_name, 0, 0, 1, 1)
        self.line_edit_unit_name = QLineEdit(self)
        self.gridLayout.addWidget(self.line_edit_unit_name, 0, 1, 1, 1)
        self.label_unit_weigh = QLabel(self)
        self.label_unit_weigh.setMinimumSize(QSize(120, 0))
        self.label_unit_weigh.setMaximumSize(QSize(120, 16777215))
        self.gridLayout.addWidget(self.label_unit_weigh, 1, 0, 1, 1)
        self.double_spin_box_unit_weigh = QDoubleSpinBox(self)
        self.double_spin_box_unit_weigh.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.double_spin_box_unit_weigh.setMaximum(20000.0)
        self.double_spin_box_unit_weigh.setSingleStep(0.01)
        self.gridLayout.addWidget(self.double_spin_box_unit_weigh, 1, 1, 1, 1)
        self.label_unit_loc = QLabel(self)
        self.label_unit_loc.setMinimumSize(QSize(120, 0))
        self.label_unit_loc.setMaximumSize(QSize(120, 16777215))
        self.gridLayout.addWidget(self.label_unit_loc, 2, 0, 1, 1)
        self.double_spin_box_unit_loc = QDoubleSpinBox(self)
        self.double_spin_box_unit_loc.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.double_spin_box_unit_loc.setMaximum(20000.0)
        self.double_spin_box_unit_loc.setSingleStep(0.01)
        self.gridLayout.addWidget(self.double_spin_box_unit_loc, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QHBoxLayout()
        spacer_item = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacer_item)
        self.btn_confirm = QPushButton(self)
        self.horizontalLayout.addWidget(self.btn_confirm)
        self.btn_cancel = QPushButton(self)
        self.horizontalLayout.addWidget(self.btn_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.translate()

        self.btn_confirm.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

    def accept(self):
        if self.line_edit_unit_name.text():
            self.unit_name = self.line_edit_unit_name.text()
            self.unit_weigh = self.double_spin_box_unit_weigh.value()
            self.unit_loc = self.double_spin_box_unit_loc.value()
            QDialog.accept(self)
        else:
            QMessageBox.information(self, '部件编辑', '部件名称不能为空')

    def translate(self):
        self.setWindowTitle("编辑部件")
        self.label_unit_name.setText("部件名称")
        self.label_unit_weigh.setText("部件重量（kg）")
        self.label_unit_loc.setText("部件位置（mm）")
        self.btn_confirm.setText("确定")
        self.btn_cancel.setText("取消")


# class WeighDialog(QDialog):
#     signal_refresh_fuel_consume_line = pyqtSignal()
#
#     def __init__(self, parent=None):
#         super().__init__(parent)
#
#         font = QFont()
#         font.setFamily('微软雅黑')
#         self.setFont(font)
#         self.resize(980, 890)
#         self.gridLayout_5 = QGridLayout(self)
#         self.gb_result = QGroupBox(self)
#         self.gridLayout = QGridLayout(self.gb_result)
#         self.label_actual_cg = QLabel(self.gb_result)
#         self.gridLayout.addWidget(self.label_actual_cg, 1, 0, 1, 1)
#         self.spin_box_actual_weight = QSpinBox(self.gb_result)
#         self.spin_box_actual_weight.setButtonSymbols(QAbstractSpinBox.NoButtons)
#         self.spin_box_actual_weight.setMinimum(0)
#         self.spin_box_actual_weight.setMaximum(999999)
#         self.gridLayout.addWidget(self.spin_box_actual_weight, 0, 1, 1, 1)
#         self.label_empty_weight = QLabel(self.gb_result)
#         self.gridLayout.addWidget(self.label_empty_weight, 2, 0, 1, 1)
#         self.double_spin_box_actual_cg = QDoubleSpinBox(self.gb_result)
#         self.double_spin_box_actual_cg.setButtonSymbols(QAbstractSpinBox.NoButtons)
#         self.double_spin_box_actual_cg.setSingleStep(0.01)
#         self.gridLayout.addWidget(self.double_spin_box_actual_cg, 1, 1, 1, 1)
#         self.spin_box_empty_weight = QSpinBox(self.gb_result)
#         self.spin_box_empty_weight.setButtonSymbols(QAbstractSpinBox.NoButtons)
#         self.spin_box_empty_weight.setMaximum(999999)
#         self.gridLayout.addWidget(self.spin_box_empty_weight, 2, 1, 1, 1)
#         self.label_empty_cg = QLabel(self.gb_result)
#         self.gridLayout.addWidget(self.label_empty_cg, 3, 0, 1, 1)
#         self.label_actual_weight = QLabel(self.gb_result)
#         self.gridLayout.addWidget(self.label_actual_weight, 0, 0, 1, 1)
#         self.double_spin_box_empty_cg = QDoubleSpinBox(self.gb_result)
#         self.double_spin_box_empty_cg.setButtonSymbols(QAbstractSpinBox.NoButtons)
#         self.gridLayout.addWidget(self.double_spin_box_empty_cg, 3, 1, 1, 1)
#         self.btn_re_cal = QPushButton(self.gb_result)
#         self.btn_re_cal.setMinimumSize(QSize(0, 22))
#         self.btn_re_cal.setMaximumSize(QSize(16777215, 22))
#         self.gridLayout.addWidget(self.btn_re_cal, 4, 1, 1, 1)
#         self.gridLayout.setColumnStretch(0, 1)
#         self.gridLayout.setColumnStretch(1, 1)
#         self.gridLayout_5.addWidget(self.gb_result, 0, 0, 1, 1)
#         self.gb_general_info = QGroupBox(self)
#         self.gridLayout_2 = QGridLayout(self.gb_general_info)
#         self.label_aircraft_type = QLabel(self.gb_general_info)
#         self.gridLayout_2.addWidget(self.label_aircraft_type, 0, 0, 1, 1)
#         self.combo_box_aircraft_type = QComboBox(self.gb_general_info)
#         self.combo_box_aircraft_type.setEditable(True)
#         self.combo_box_aircraft_type.addItem("")
#         self.combo_box_aircraft_type.addItem("")
#         self.gridLayout_2.addWidget(self.combo_box_aircraft_type, 0, 1, 1, 1)
#         self.label_aircraft_num = QLabel(self.gb_general_info)
#         self.gridLayout_2.addWidget(self.label_aircraft_num, 1, 0, 1, 1)
#         self.combo_box_aircraft_num = QComboBox(self.gb_general_info)
#         self.combo_box_aircraft_num.setEditable(True)
#         self.combo_box_aircraft_num.addItem("")
#         self.combo_box_aircraft_num.addItem("")
#         self.combo_box_aircraft_num.addItem("")
#         self.gridLayout_2.addWidget(self.combo_box_aircraft_num, 1, 1, 1, 1)
#         self.label_weigh_method = QLabel(self.gb_general_info)
#         self.gridLayout_2.addWidget(self.label_weigh_method, 2, 0, 1, 1)
#         self.combo_box_weigh_method = QComboBox(self.gb_general_info)
#         self.combo_box_weigh_method.setEditable(True)
#         self.combo_box_weigh_method.addItem("")
#         self.gridLayout_2.addWidget(self.combo_box_weigh_method, 2, 1, 1, 1)
#         self.label_weigh_loc = QLabel(self.gb_general_info)
#         self.gridLayout_2.addWidget(self.label_weigh_loc, 3, 0, 1, 1)
#         self.line_edit_loc = QLineEdit(self.gb_general_info)
#         self.gridLayout_2.addWidget(self.line_edit_loc, 3, 1, 1, 1)
#         self.label_weigh_date = QLabel(self.gb_general_info)
#         self.gridLayout_2.addWidget(self.label_weigh_date, 4, 0, 1, 1)
#         self.date_edit_weigh_date = QDateEdit(self.gb_general_info)
#         self.date_edit_weigh_date.setButtonSymbols(QAbstractSpinBox.NoButtons)
#         self.gridLayout_2.addWidget(self.date_edit_weigh_date, 4, 1, 1, 1)
#         self.gridLayout_2.setColumnStretch(0, 1)
#         self.gridLayout_2.setColumnStretch(1, 1)
#         self.gridLayout_5.addWidget(self.gb_general_info, 0, 1, 1, 1)
#         self.group_box_weigh_first = QGroupBox(self)
#         self.gridLayout_3 = QGridLayout(self.group_box_weigh_first)
#         self.label_nose_right = QLabel(self.group_box_weigh_first)
#         self.gridLayout_3.addWidget(self.label_nose_right, 0, 0, 1, 1)
#         self.spin_box_nose_right = QSpinBox(self.group_box_weigh_first)
#         self.spin_box_nose_right.setButtonSymbols(QAbstractSpinBox.NoButtons)
#         self.spin_box_nose_right.setMaximum(999999)
#         self.gridLayout_3.addWidget(self.spin_box_nose_right, 0, 1, 1, 1)
#         self.label_nose_left = QLabel(self.group_box_weigh_first)
#         self.gridLayout_3.addWidget(self.label_nose_left, 1, 0, 1, 1)
#         self.spin_box_nose_left = QSpinBox(self.group_box_weigh_first)
#         self.spin_box_nose_left.setButtonSymbols(QAbstractSpinBox.NoButtons)
#         self.spin_box_nose_left.setMaximum(999999)
#         self.gridLayout_3.addWidget(self.spin_box_nose_left, 1, 1, 1, 1)
#         self.label_left_out = QLabel(self.group_box_weigh_first)
#         self.gridLayout_3.addWidget(self.label_left_out, 2, 0, 1, 1)
#         self.spin_box_left_out = QSpinBox(self.group_box_weigh_first)
#         self.spin_box_left_out.setButtonSymbols(QAbstractSpinBox.NoButtons)
#         self.spin_box_left_out.setMaximum(999999)
#         self.gridLayout_3.addWidget(self.spin_box_left_out, 2, 1, 1, 1)
#         self.label_left_in = QLabel(self.group_box_weigh_first)
#         self.gridLayout_3.addWidget(self.label_left_in, 3, 0, 1, 1)
#         self.spin_box_left_in = QSpinBox(self.group_box_weigh_first)
#         self.spin_box_left_in.setButtonSymbols(QAbstractSpinBox.NoButtons)
#         self.spin_box_left_in.setMaximum(999999)
#         self.gridLayout_3.addWidget(self.spin_box_left_in, 3, 1, 1, 1)
#         self.label_right_in = QLabel(self.group_box_weigh_first)
#         self.gridLayout_3.addWidget(self.label_right_in, 4, 0, 1, 1)
#         self.spin_box_right_in = QSpinBox(self.group_box_weigh_first)
#         self.spin_box_right_in.setButtonSymbols(QAbstractSpinBox.NoButtons)
#         self.spin_box_right_in.setMaximum(999999)
#         self.gridLayout_3.addWidget(self.spin_box_right_in, 4, 1, 1, 1)
#         self.label_right_out = QLabel(self.group_box_weigh_first)
#         self.gridLayout_3.addWidget(self.label_right_out, 5, 0, 1, 1)
#         self.spin_box_right_out = QSpinBox(self.group_box_weigh_first)
#         self.spin_box_right_out.setButtonSymbols(QAbstractSpinBox.NoButtons)
#         self.spin_box_right_out.setMaximum(999999)
#         self.gridLayout_3.addWidget(self.spin_box_right_out, 5, 1, 1, 1)
#         self.gridLayout_5.addWidget(self.group_box_weigh_first, 1, 0, 1, 1)
#         self.group_box_weigh_second = QGroupBox(self)
#         self.gridLayout_4 = QGridLayout(self.group_box_weigh_second)
#         self.label_nose_right_2 = QLabel(self.group_box_weigh_second)
#         self.gridLayout_4.addWidget(self.label_nose_right_2, 0, 0, 1, 1)
#         self.spin_box_nose_right_2 = QSpinBox(self.group_box_weigh_second)
#         self.spin_box_nose_right_2.setButtonSymbols(QAbstractSpinBox.NoButtons)
#         self.spin_box_nose_right_2.setMaximum(999999)
#         self.gridLayout_4.addWidget(self.spin_box_nose_right_2, 0, 1, 1, 1)
#         self.label_nose_left_2 = QLabel(self.group_box_weigh_second)
#         self.gridLayout_4.addWidget(self.label_nose_left_2, 1, 0, 1, 1)
#         self.spin_box_nose_left_2 = QSpinBox(self.group_box_weigh_second)
#         self.spin_box_nose_left_2.setButtonSymbols(QAbstractSpinBox.NoButtons)
#         self.spin_box_nose_left_2.setMaximum(999999)
#         self.gridLayout_4.addWidget(self.spin_box_nose_left_2, 1, 1, 1, 1)
#         self.label_left_out_2 = QLabel(self.group_box_weigh_second)
#         self.gridLayout_4.addWidget(self.label_left_out_2, 2, 0, 1, 1)
#         self.spin_box_left_out_2 = QSpinBox(self.group_box_weigh_second)
#         self.spin_box_left_out_2.setButtonSymbols(QAbstractSpinBox.NoButtons)
#         self.spin_box_left_out_2.setMaximum(999999)
#         self.gridLayout_4.addWidget(self.spin_box_left_out_2, 2, 1, 1, 1)
#         self.label_left_in_2 = QLabel(self.group_box_weigh_second)
#         self.gridLayout_4.addWidget(self.label_left_in_2, 3, 0, 1, 1)
#         self.spin_box_left_in_2 = QSpinBox(self.group_box_weigh_second)
#         self.spin_box_left_in_2.setButtonSymbols(QAbstractSpinBox.NoButtons)
#         self.spin_box_left_in_2.setMaximum(999999)
#         self.gridLayout_4.addWidget(self.spin_box_left_in_2, 3, 1, 1, 1)
#         self.label_right_in_2 = QLabel(self.group_box_weigh_second)
#         self.gridLayout_4.addWidget(self.label_right_in_2, 4, 0, 1, 1)
#         self.spin_box_right_in_2 = QSpinBox(self.group_box_weigh_second)
#         self.spin_box_right_in_2.setButtonSymbols(QAbstractSpinBox.NoButtons)
#         self.spin_box_right_in_2.setMaximum(999999)
#         self.gridLayout_4.addWidget(self.spin_box_right_in_2, 4, 1, 1, 1)
#         self.label_right_out_2 = QLabel(self.group_box_weigh_second)
#         self.gridLayout_4.addWidget(self.label_right_out_2, 5, 0, 1, 1)
#         self.spin_box_right_out_2 = QSpinBox(self.group_box_weigh_second)
#         self.spin_box_right_out_2.setButtonSymbols(QAbstractSpinBox.NoButtons)
#         self.spin_box_right_out_2.setMaximum(999999)
#         self.gridLayout_4.addWidget(self.spin_box_right_out_2, 5, 1, 1, 1)
#         self.gridLayout_5.addWidget(self.group_box_weigh_second, 1, 1, 1, 1)
#         self.group_box_pillar = QGroupBox(self)
#         self.horizontalLayout = QHBoxLayout(self.group_box_pillar)
#         self.label_ln = QLabel(self.group_box_pillar)
#         self.horizontalLayout.addWidget(self.label_ln)
#         self.spin_box_ln = QSpinBox(self.group_box_pillar)
#         self.spin_box_ln.setButtonSymbols(QAbstractSpinBox.NoButtons)
#         self.spin_box_ln.setMaximum(9999)
#         self.horizontalLayout.addWidget(self.spin_box_ln)
#         self.label_lml = QLabel(self.group_box_pillar)
#         self.horizontalLayout.addWidget(self.label_lml)
#         self.spin_box_lml = QSpinBox(self.group_box_pillar)
#         self.spin_box_lml.setButtonSymbols(QAbstractSpinBox.NoButtons)
#         self.spin_box_lml.setMaximum(9999)
#         self.horizontalLayout.addWidget(self.spin_box_lml)
#         self.label_lmr = QLabel(self.group_box_pillar)
#         self.horizontalLayout.addWidget(self.label_lmr)
#         self.spin_box_lmr = QSpinBox(self.group_box_pillar)
#         self.spin_box_lmr.setButtonSymbols(QAbstractSpinBox.NoButtons)
#         self.spin_box_lmr.setMaximum(9999)
#         self.horizontalLayout.addWidget(self.spin_box_lmr)
#         self.gridLayout_5.addWidget(self.group_box_pillar, 2, 0, 1, 2)
#         self.group_box_pitch = QGroupBox(self)
#         self.verticalLayout_pitch = QVBoxLayout(self.group_box_pitch)
#         self.double_spin_box_pitch_angle = QDoubleSpinBox(self.group_box_pitch)
#         self.double_spin_box_pitch_angle.setButtonSymbols(QAbstractSpinBox.NoButtons)
#         self.double_spin_box_pitch_angle.setMinimum(-100)
#         self.double_spin_box_pitch_angle.setMaximum(100)
#         self.verticalLayout_pitch.addWidget(self.double_spin_box_pitch_angle)
#         self.gridLayout_5.addWidget(self.group_box_pitch, 3, 0, 1, 2)
#         self.group_box_surplus = QGroupBox(self)
#         self.verticalLayout = QVBoxLayout(self.group_box_surplus)
#         self.table_view_surplus = UnitInfoList(self.group_box_surplus)
#         self.verticalLayout.addWidget(self.table_view_surplus)
#         self.gridLayout_5.addWidget(self.group_box_surplus, 4, 0, 1, 1)
#         self.group_box_lack = QGroupBox(self)
#         self.verticalLayout_2 = QVBoxLayout(self.group_box_lack)
#         self.table_view_lack = UnitInfoList(self.group_box_lack)
#         self.verticalLayout_2.addWidget(self.table_view_lack)
#         self.gridLayout_5.addWidget(self.group_box_lack, 4, 1, 1, 1)
#
#         self.translate()
#
#         self.btn_re_cal.clicked.connect(self.calculate_weight_cg)
#
#     # 计算重量重心
#     def calculate_weight_cg(self):
#         if self.is_satisfied_weigh_condition():
#             # 更新称重数据
#             self.update_weigh_info()
#             # 计算称重的重量重心
#             data_collector.weigh_data_calculate_object.recalculate_weight_cg()
#             # 显示称重结果
#             self.display_calculate_result()
#
#     # 显示计算结果
#     def display_calculate_result(self):
#         self.spin_box_actual_weight.setValue(int(data_collector.weigh_data_calculate_object.Wr))
#         self.spin_box_empty_weight.setValue(int(data_collector.weigh_data_calculate_object.Wt))
#
#         self.double_spin_box_actual_cg.setValue(data_collector.weigh_data_calculate_object.Xr_)
#         self.double_spin_box_empty_cg.setValue(data_collector.weigh_data_calculate_object.Xt_)
#
#         # 发出更新燃油消耗曲线信息
#         self.signal_refresh_fuel_consume_line.emit()
#
#     # 加载算例时，显示称重数据
#     def display_weigh_info(self):
#         self.combo_box_aircraft_type.setCurrentText(data_collector.weigh_info['aircraft_type'])
#         self.combo_box_aircraft_num.setCurrentText(data_collector.weigh_info['aircraft'])
#         self.combo_box_weigh_method.setCurrentText(data_collector.weigh_info['weigh_method'])
#         self.line_edit_loc.setText(data_collector.weigh_info['weigh_location'])
#         self.date_edit_weigh_date.setDateTime(QDateTime().fromString(
#             data_collector.weigh_info['weigh_date'], 'yyyy/MM/dd'))
#         self.spin_box_nose_right.setValue(data_collector.weigh_info['weigh_tyre_nr'][0])
#         self.spin_box_nose_right_2.setValue(data_collector.weigh_info['weigh_tyre_nr'][1])
#         self.spin_box_nose_left.setValue(data_collector.weigh_info['weigh_tyre_nl'][0])
#         self.spin_box_nose_left_2.setValue(data_collector.weigh_info['weigh_tyre_nl'][1])
#         self.spin_box_left_out.setValue(data_collector.weigh_info['weigh_tyre_lo'][0])
#         self.spin_box_left_out_2.setValue(data_collector.weigh_info['weigh_tyre_lo'][1])
#         self.spin_box_left_in.setValue(data_collector.weigh_info['weigh_tyre_li'][0])
#         self.spin_box_left_in_2.setValue(data_collector.weigh_info['weigh_tyre_li'][1])
#         self.spin_box_right_in.setValue(data_collector.weigh_info['weigh_tyre_ri'][0])
#         self.spin_box_right_in_2.setValue(data_collector.weigh_info['weigh_tyre_ri'][1])
#         self.spin_box_right_out.setValue(data_collector.weigh_info['weigh_tyre_ro'][0])
#         self.spin_box_right_out_2.setValue(data_collector.weigh_info['weigh_tyre_ro'][1])
#         self.spin_box_ln.setValue(data_collector.weigh_info['weigh_pillar_ln'])
#         self.spin_box_lmr.setValue(data_collector.weigh_info['weigh_pillar_lmr'])
#         self.spin_box_lml.setValue(data_collector.weigh_info['weigh_pillar_lml'])
#         self.double_spin_box_pitch_angle.setValue(data_collector.weigh_info['pitch_angle'])
#
#         # 显示多装件
#         self.table_view_surplus.clear()
#         for unit in data_collector.weigh_info['redundant_unit']:
#             item = QTreeWidgetItem()
#             item.setText(0, unit[0])
#             item.setText(1, '%.2f' % unit[1])
#             item.setText(2, '%.2f' % unit[2])
#             self.table_view_surplus.addTopLevelItem(item)
#
#         # 显示多装件
#         self.table_view_lack.clear()
#         for unit in data_collector.weigh_info['absence_unit']:
#             item = QTreeWidgetItem()
#             item.setText(0, unit[0])
#             item.setText(1, '%.2f' % unit[1])
#             item.setText(2, '%.2f' % unit[2])
#             self.table_view_lack.addTopLevelItem(item)
#
#         # 计算称重的重量重心
#         data_collector.weigh_data_calculate_object.recalculate_weight_cg()
#
#         self.display_calculate_result()
#
#     # 判断输入的数据是否满足称重要求
#     def is_satisfied_weigh_condition(self):
#         weight_first = self.spin_box_nose_right.value() + self.spin_box_nose_left.value() + \
#                        self.spin_box_right_out.value() + self.spin_box_right_in.value() + \
#                        self.spin_box_left_in.value() + self.spin_box_left_out.value()
#         weight_second = self.spin_box_nose_right_2.value() + self.spin_box_nose_left_2.value() + \
#                         self.spin_box_right_out_2.value() + self.spin_box_right_in_2.value() + \
#                         self.spin_box_left_in_2.value() + self.spin_box_left_out_2.value()
#         if (weight_first + weight_second) == 0:
#             weigh_error = 0
#         else:
#             weigh_error = abs((weight_first - weight_second) * 1.0 / (weight_first + weight_second) * 2.0 * 100)
#         # 两次称重的重量差值不得大于飞机重量的0.1%
#         if weigh_error <= 0.1:
#             return True
#         else:
#             QMessageBox.warning(self, '不满足称重要求',
#                                 '两次称重的误差：%.2f%%。\n大于飞机重量的0.1%%！' % weigh_error)
#         return False
#
#     def translate(self):
#         self.setWindowTitle("空机数据")
#         self.gb_result.setTitle("称重结果")
#         self.label_actual_cg.setText("实测重心（%MAC）")
#         self.label_empty_weight.setText("空机重量（kg）")
#         self.label_empty_cg.setText("空机重心（%MAC）")
#         self.label_actual_weight.setText("实测重量（kg）")
#         self.btn_re_cal.setText("计算重量重心")
#         self.gb_general_info.setTitle("基本信息")
#         self.label_aircraft_type.setText("飞机型号")
#         self.combo_box_aircraft_type.setItemText(0, "C919")
#         self.combo_box_aircraft_type.setItemText(1, "ARJ21-700")
#         self.label_aircraft_num.setText("架机号")
#         self.combo_box_aircraft_num.setItemText(0, "10102")
#         self.combo_box_aircraft_num.setItemText(1, "10105")
#         self.combo_box_aircraft_num.setItemText(2, "10106")
#         self.label_weigh_method.setText("称重方式")
#         self.combo_box_weigh_method.setItemText(0, "地秤称重法")
#         self.label_weigh_loc.setText("称重地点")
#         self.label_weigh_date.setText("称重日期")
#         self.group_box_weigh_first.setTitle("第一次称重(kg)")
#         self.label_nose_right.setText("前起右侧-NR")
#         self.label_nose_left.setText("前起左侧-NL")
#         self.label_left_out.setText("左主起外侧-LO")
#         self.label_left_in.setText("左主起内侧-LI")
#         self.label_right_in.setText("右主起内侧-RI")
#         self.label_right_out.setText("右主起外侧-RO")
#         self.group_box_weigh_second.setTitle("第二次称重(kg)")
#         self.label_nose_right_2.setText("前起右侧-NR")
#         self.label_nose_left_2.setText("前起左侧-NL")
#         self.label_left_out_2.setText("左主起外侧-LO")
#         self.label_left_in_2.setText("左主起内侧-LI")
#         self.label_right_in_2.setText("右主起内侧-RI")
#         self.label_right_out_2.setText("右主起外侧-RO")
#         self.group_box_pillar.setTitle("支柱行程")
#         self.label_ln.setText("前起支柱行程（mm）")
#         self.label_lml.setText("左主起支柱行程（mm）")
#         self.label_lmr.setText("左主起支柱行程（mm）")
#         self.group_box_pitch.setTitle("俯仰角")
#         self.group_box_surplus.setTitle("多装件")
#         self.group_box_lack.setTitle("缺装件")
#
#     # 更新称重信息
#     def update_weigh_info(self):
#         data_collector.weigh_info['aircraft_type'] = self.combo_box_aircraft_type.currentText()
#         data_collector.weigh_info['aircraft'] = self.combo_box_aircraft_num.currentText()
#         data_collector.weigh_info['weigh_method'] = self.combo_box_weigh_method.currentText()
#         data_collector.weigh_info['weigh_location'] = self.line_edit_loc.text()
#         data_collector.weigh_info['weigh_date'] = self.date_edit_weigh_date.dateTime().toString('yyyy/MM/dd')
#         data_collector.weigh_info['weigh_tyre_nr'] = [self.spin_box_nose_right.value(),
#                                                       self.spin_box_nose_right_2.value()]
#         data_collector.weigh_info['weigh_tyre_nl'] = [self.spin_box_nose_left.value(),
#                                                       self.spin_box_nose_left_2.value()]
#         data_collector.weigh_info['weigh_tyre_lo'] = [self.spin_box_left_out.value(),
#                                                       self.spin_box_left_out_2.value()]
#         data_collector.weigh_info['weigh_tyre_li'] = [self.spin_box_left_in.value(),
#                                                       self.spin_box_left_in_2.value()]
#         data_collector.weigh_info['weigh_tyre_ri'] = [self.spin_box_right_in.value(),
#                                                       self.spin_box_right_in_2.value()]
#         data_collector.weigh_info['weigh_tyre_ro'] = [self.spin_box_right_out.value(),
#                                                       self.spin_box_right_out_2.value()]
#         data_collector.weigh_info['weigh_pillar_ln'] = self.spin_box_ln.value()
#         data_collector.weigh_info['weigh_pillar_lmr'] = self.spin_box_lmr.value()
#         data_collector.weigh_info['weigh_pillar_lml'] = self.spin_box_lml.value()
#         data_collector.weigh_info['pitch_angle'] = self.double_spin_box_pitch_angle.value()
#         # 计算多装件
#         data_collector.weigh_info['redundant_unit'] = list()
#         for i in range(self.table_view_surplus.topLevelItemCount()):
#             unit_item = self.table_view_surplus.topLevelItem(i)
#             unit_info = [unit_item.text(0), float(unit_item.text(1)), float(unit_item.text(2))]
#             data_collector.weigh_info['redundant_unit'].append(unit_info)
#         # 计算缺装件
#         data_collector.weigh_info['absence_unit'] = list()
#         for i in range(self.table_view_lack.topLevelItemCount()):
#             unit_item = self.table_view_lack.topLevelItem(i)
#             unit_info = [unit_item.text(0), float(unit_item.text(1)), float(unit_item.text(2))]
#             data_collector.weigh_info['absence_unit'].append(unit_info)
