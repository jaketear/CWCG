# -*- coding: utf-8 -*-

import os
import xlrd


aircraft_fuel_out_frame = None
aircraft_center_fuel_frame = None
aircraft_left_fuel_frame = None
aircraft_right_fuel_frame = None
ratio_w_h = 1612 / 580


# 从excel文件中读取飞机油箱外形数据
def load_fuel_bank_frame_data_from_excel(file_dir='.\\data\\飞机外形数据.xlsx'):
    result_tip = ''
    if os.path.isfile(file_dir):
        try:
            global aircraft_fuel_out_frame
            global aircraft_center_fuel_frame
            global aircraft_left_fuel_frame
            global aircraft_right_fuel_frame
            # 打开文件
            xl_data = xlrd.open_workbook(file_dir)
            # 选择第一个sheet
            table = xl_data.sheet_by_index(0)
            if table.ncols >= 8:
                # 读取油箱外轮廓数据
                aircraft_fuel_out_frame = zip(table.col_values(0)[1:], table.col_values(1)[1:])
                aircraft_fuel_out_frame = [(x, y) for x, y in aircraft_fuel_out_frame if x]

                aircraft_center_fuel_frame = zip(table.col_values(2)[1:], table.col_values(3)[1:])
                aircraft_center_fuel_frame = [(x, y) for x, y in aircraft_center_fuel_frame if x]

                aircraft_left_fuel_frame = zip(table.col_values(4)[1:], table.col_values(5)[1:])
                aircraft_left_fuel_frame = [(x, y) for x, y in aircraft_left_fuel_frame if x]

                aircraft_right_fuel_frame = zip(table.col_values(6)[1:], table.col_values(7)[1:])
                aircraft_right_fuel_frame = [(x, y) for x, y in aircraft_right_fuel_frame if x]
        except:
            result_tip = '读取失败！'
    return result_tip
