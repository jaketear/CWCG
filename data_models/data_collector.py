# -*- coding: utf-8 -*-

import os
import os.path as path
import xlrd
import json

from data_models import config_info, CGmethod, ZFWmethod, fuelConsumptionMethod

# 飞机重量重心相关数据
# --称重信息--
# --aircraft_type-飞机型号, aircraft-飞机架机号, weigh_method-称重方法,
# --weigh_location-称重地点, weigh_date-称重时间, weigh_tyre-轮子承重,
# --weigh_pillar-支柱行程, redundant_unit-多装件(列表型列表，[多装件名称, 重量, 力臂]),
# --absence_unit-缺装件(列表型列表，[缺装件名称, 重量, 力臂])
weigh_info = dict(aircraft_type='', aircraft='', weigh_method='地磅称重法',
                  weigh_location='', weigh_date='',
                  weigh_tyre_nr=[0, 0], weigh_tyre_nl=[0, 0],
                  weigh_tyre_lo=[0, 0], weigh_tyre_li=[0, 0],
                  weigh_tyre_ri=[0, 0], weigh_tyre_ro=[0, 0],
                  weigh_pillar_ln=0, weigh_pillar_lmr=0, weigh_pillar_lml=0,
                  pitch_angle=0,
                  redundant_unit=list(), absence_unit=list())

# --配载和装载信息--
# --service_item-标准项目,operation_item-使用项目,load-配重(列表型列表，[名称, 重量, 力臂])
stowage_info = dict(service_item=list(), operation_item=list(), load=list())
# --燃油信息
fuel_info = dict(left_fuel_bank=0, center_fuel_bank=0, right_fuel_bank=0)

# --称重计算对象--
weigh_data_calculate_object = CGmethod.CG()

# --零油重量重心计算方法--
# zero_fuel_status_calculate_object = ZFWmethod.ZFW()

# 飞机油箱外形数据
aircraft_fuel_out_frame = None
aircraft_center_fuel_frame = None
aircraft_left_fuel_frame = None
aircraft_right_fuel_frame = None
ratio_w_h = 1612 / 580


# 导出称重信息到json文件中
def export_weight_info_to_json(file_dir):
    result_tip = ''
    if not file_dir:
        file_dir = config_info.default_weigh_info_export_dir + os.sep + 'weigh_info.json'
    if isinstance(weigh_info, dict):
        try:
            with open(file_dir, 'w') as f:
                json.dump(weigh_info, f, indent=4)
        except FileExistsError:
            result_tip = 'FileExistsError：数据文件已存在，无法创建!'
        except FileNotFoundError:
            result_tip = 'FileNotFoundError：数据文件不存在!'
        except OSError:
            result_tip = 'OSError：无法读取数据文件!'
    return result_tip


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


# 从json文件中读取称重信息
def load_weigh_info_from_json(file_dir):
    result_tip = ''
    if path.isfile(file_dir):
        try:
            with open(file_dir, 'r') as f:
                flight_info = json.load(f)
                if isinstance(flight_info, dict):
                    set_weigh_info(**flight_info)
                else:
                    result_tip = '数据文件无法解析！'
        except FileExistsError:
            result_tip = 'FileExistsError：数据文件已存在，无法创建!'
        except FileNotFoundError:
            result_tip = 'FileNotFoundError：数据文件不存在!'
        except OSError:
            result_tip = 'OSError：无法读取数据文件!'
        except TypeError:
            result_tip = 'TypeError：类型错误!'
    else:
        result_tip = '路径未对应一个文件!'
    return result_tip


# 设置称重信息
def set_weigh_info(**kwargs):
    for k in kwargs:
        if k in weigh_info:
            if isinstance(kwargs[k], type(weigh_info[k])):
                weigh_info[k] = kwargs[k]
