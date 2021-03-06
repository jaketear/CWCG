# -*- coding: utf-8 -*-

import os
import os.path as path
import xlrd
import json

from data_models import config_info, CGmethod, ZFWmethod, fuelConsumptionMethod

# 飞机重量重心相关数据
# --特征数据--
# 平均气动弦长
mean_aero_chord = 4268
# 机翼平均气动力弦长前缘点航向位置
mac_front_distance = 19837
# 飞机重量重心信息
aircraft_weight_info = dict(major_aircraft_weight=dict(test_empty_weight=['试验空机重量', 0, 0, 0, 0],
                                                       operation_item=['使用项目', 0, 0, 0, 0],
                                                       operation_empty_weight=['使用空机重量', 0, 0, 0, 0],
                                                       stowage_item=['配载', 0, 0, 0, 0],
                                                       zero_fuel_weight=['零油重量', 0, 0, 0, 0],
                                                       fuel_item=['燃油', 0, 0, 0, 0],
                                                       total_weight=['总重', 0, 0, 0, 0]),
                            operation_item=[['行李', 0, 0, 0, 0]],
                            stowage_item=list(),
                            fuel_item=list())
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
                  pitch_angle=0.0,
                  redundant_unit=list(), absence_unit=list())

# --配载和装载信息--
# --service_item-标准项目,operation_item-使用项目,load-配重(列表型列表，[名称, 重量, 力臂])
stowage_info = dict(service_item=list(), operation_item=list(), load=list())
# --燃油信息
fuel_info = dict(left=2749.0, central=11804.0, right=2749.0,
                 left_limit=3050.9, center_limit=11976.5, right_limit=3050.9)

# --称重计算对象--
weigh_data_calculate_object = CGmethod.CG()

# --零油重量重心计算方法--
# zero_fuel_status_calculate_object = ZFWmethod.ZFW()

# --燃油消耗曲线计算方法--
fuel_consumption_calculate_object = fuelConsumptionMethod.FuleConsumption()

# 飞机外形数据
aircraft_frame = None
aircraft_frame_ratio_w_h = 529 / 577

# 飞机油箱外形数据
aircraft_fuel_out_frame = None
aircraft_center_fuel_frame = None
aircraft_left_fuel_frame = None
aircraft_right_fuel_frame = None
ratio_w_h = 1612 / 580


# 计算空机重量重心
def calculate_zfw_and_moment():
    item_weight = weigh_data_calculate_object.Wt
    item_arm = weigh_data_calculate_object.Xt_ * mean_aero_chord / 100 + mac_front_distance
    item_moment = weigh_data_calculate_object.Wt * item_arm
    for item_key in stowage_info:
        for unit in stowage_info[item_key]:
            weight = unit[1]
            arm = unit[2]
            item_weight += weight
            item_moment += weight * arm

    return item_weight, item_moment


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


# 获取燃油消耗数据
def get_fuel_consume_data():
    w, m = calculate_zfw_and_moment()
    zero_fuel_weight = {"weight": w, "force": m}

    temp_fuel_info = dict(left=fuel_info['left'],
                          central=fuel_info['central'],
                          right=fuel_info['right'])
    fuel_consumption_sum = fuel_consumption_calculate_object.fuel_consumption_force_caculate(temp_fuel_info)
    cg_real_time = fuel_consumption_calculate_object.fuel_consumption_CG_caculate(zero_fuel_weight,
                                                                                  fuel_consumption_sum)
    return fuel_consumption_sum, cg_real_time


# 从excel文件中读取飞机油箱外形数据
def load_aircraft_frame_data_from_excel(file_dir='.\\data\\飞机外形数据.xlsx'):
    result_tip = ''
    if os.path.isfile(file_dir):
        try:
            global aircraft_frame
            # 打开文件
            xl_data = xlrd.open_workbook(file_dir)
            # 选择第一个sheet
            table = xl_data.sheet_by_index(0)
            if table.ncols >= 8:
                # 读取飞机外轮廓数据
                aircraft_frame = zip(table.col_values(8)[1:], table.col_values(9)[1:])
                aircraft_frame = [(x, y) for x, y in aircraft_frame if x]
        except:
            result_tip = '读取失败！'
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


# 设置燃油信息
def set_fuel_info(**kwargs):
    for k in kwargs:
        if k in fuel_info:
            if isinstance(kwargs[k], type(fuel_info[k])):
                fuel_info[k] = kwargs[k]
