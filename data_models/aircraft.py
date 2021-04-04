# -*- coding: utf-8 -*-

import configparser

from data_models import config_info, CGmethod, ZFWmethod, fuelConsumptionMethod


# 定义一个飞机基类
class AircraftBaseClass(object):
    def __init__(self):
        # 长度单位取mm，重量单位取kg，力矩单位取kg * mm
        # ---基本信息---
        # 飞机型号
        self.aircraft_type = ''
        # 飞机编号
        self.aircraft_id = ''

        # ---外形数据---
        # 平均气动弦长
        self.mean_aero_chord = None
        # 机翼平均气动力弦长前缘点航向位置
        self.mac_front_distance = None

        # 起飞水平安定面配平设置，重心与配平值的一维关系，构型作为键
        self.take_off_trim_value = dict()

        # 活动部件对飞机重心的影响，部件状态和力矩的对应关系表
        self.mobilize_unit_cg_influence = dict()

        # 飞机框位数据，框名和站位的对应关系表
        self.frame_pos = dict()
        # 飞机框位图路径
        self.aircraft_frame_pic_path = ''

        # ---限制---
        # 重量限制，重量限制和限制值的对应关系表
        self.weight_limit = dict()
        # 重心限制，不同构型下飞机重量对应的重心前后限
        self.cg_limit = dict()
        # 强度限制，飞机不同位置的装载强度限制
        self.strength_limit = dict()
        # 装载限制，飞机客舱货舱处的装载能力限制
        self.stowage_limit = dict()
        # 后翻限制
        self.roll_back_limit = None

        # ---燃油数据---
        # 燃油限制
        self.fuel_limit = dict()
        # 燃油重量和重心关系对照表
        self.fuel_weight_cg_relation = dict()
        # 燃油偏差对照表，显示和实际关系
        self.fuel_weight_bias_relation = dict()
        # 不可用燃油
        self.disable_fuel_weight = dict()

        # ---典型部件和载荷数据---
        self.major_stowage_data = dict()

        # ---称重信息---
        # --aircraft_type-飞机型号, aircraft-飞机架机号, weigh_method-称重方法,
        # --weigh_location-称重地点, weigh_date-称重时间, weigh_tyre-轮子承重,
        # --weigh_pillar-支柱行程, redundant_unit-多装件(列表型列表，[多装件名称, 重量, 力臂]),
        # --absence_unit-缺装件(列表型列表，[缺装件名称, 重量, 力臂])
        self.weigh_info = dict(aircraft_type='', aircraft='', weigh_method='地磅称重法',
                               weigh_location='', weigh_date='',
                               weigh_tyre_nr=[0, 0], weigh_tyre_nl=[0, 0],
                               weigh_tyre_lo=[0, 0], weigh_tyre_li=[0, 0],
                               weigh_tyre_ri=[0, 0], weigh_tyre_ro=[0, 0],
                               weigh_pillar_ln=0, weigh_pillar_lmr=0, weigh_pillar_lml=0,
                               pitch_angle=0.0,
                               redundant_unit=list(), absence_unit=list())

        # ---配载和装载信息---
        # --operation_item-使用项目,load-配重(列表型列表，[名称, 重量, 力臂])
        self.stowage_info = dict(operation_items=list(), loads=list())

        # ---燃油信息---
        self.fuel_info = dict(left=2749.0, central=11804.0, right=2749.0,
                              left_limit=3050.9, center_limit=11976.5, right_limit=3050.9)

        # --称重计算对象--
        self.weigh_data_calculate_object = CGmethod.CG()
        # --零油重量重心计算方法--
        # self.zero_fuel_status_calculate_object = ZFWmethod.ZFW()
        # --燃油消耗曲线计算方法--
        self.fuel_consumption_calculate_object = fuelConsumptionMethod.FuleConsumption()

        self.init_aircraft_by_file(r'D:\CWCG\C919_10106.ini')

    # 计算空机重量及力矩
    def calculate_zfw_and_moment(self):
        item_weight = self.weigh_data_calculate_object.Wt
        item_arm = self.weigh_data_calculate_object.Xt_ * self.mean_aero_chord / 100 + self.mac_front_distance
        item_moment = self.weigh_data_calculate_object.Wt * item_arm
        for item_key in self.stowage_info:
            for unit in self.stowage_info[item_key]:
                weight = unit[1]
                arm = unit[2]
                item_weight += weight
                item_moment += weight * arm

        return item_weight, item_moment

    # 获取飞机基本信息
    def get_aircraft_base_info(self):
        base_info = dict()
        base_info['飞机型号'] = self.aircraft_type
        base_info['飞机编号'] = self.aircraft_id
        for key, value in self.fuel_limit.items():
            base_info[key] = str(value) + ' kg'
        for key, value in self.weight_limit.items():
            base_info[key] = str(value) + ' kg'
        return base_info

    # 获取飞机重量重心信息
    def get_aircraft_weight_info(self):
        # 飞机重量重心信息
        aircraft_weight_info = dict(major_aircraft_weight=dict(test_empty_weight=['试验空机重量', 0, 0, 0, 0],
                                                               operation_item=['使用项目', 0, 0, 0, 0],
                                                               operation_empty_weight=['使用空机重量', 0, 0, 0, 0],
                                                               stowage_item=['配载', 0, 0, 0, 0],
                                                               zero_fuel_weight=['零油重量', 0, 0, 0, 0],
                                                               fuel_item=['燃油', 0, 0, 0, 0],
                                                               total_weight=['总重', 0, 0, 0, 0]),
                                    operation_items=self.stowage_info['operation_items'],
                                    stowage_items=list(),
                                    fuel_items=list())
        aircraft_weight_info['major_aircraft_weight']['test_empty_weight'] = ['试验空机重量',
                                                                              46593, 20825.7, 970329720.4, 23.2]
        aircraft_weight_info['major_aircraft_weight']['stowage_item'] = ['配载', 350, 29979, 10492650, 0]
        aircraft_weight_info['major_aircraft_weight']['operation_item'] = ['使用项目', 753, 13954.4, 10507648, 0]
        aircraft_weight_info['major_aircraft_weight']['operation_empty_weight'] = ['使用空机重量',
                                                                                   47346, 20716.2, 980837368.9, 20.6]
        aircraft_weight_info['major_aircraft_weight']['zero_fuel_weight'] = ['零油重量',
                                                                             47696, 20784.2, 991330018.9, 22.2]
        aircraft_weight_info['major_aircraft_weight']['total_weight'] = ['总重',
                                                                         62696, 20709.2, 1298395711.7, 20.4]
        return aircraft_weight_info

    # 获取燃油消耗数据
    def get_fuel_consume_data(self):
        w, m = self.calculate_zfw_and_moment()
        zero_fuel_weight = {"weight": w, "force": m}

        temp_fuel_info = dict(left=self.fuel_info['left'],
                              central=self.fuel_info['central'],
                              right=self.fuel_info['right'])
        fuel_consumption_sum = self.fuel_consumption_calculate_object.fuel_consumption_force_caculate(temp_fuel_info)
        cg_real_time = self.fuel_consumption_calculate_object.fuel_consumption_CG_caculate(zero_fuel_weight,
                                                                                           fuel_consumption_sum)
        return fuel_consumption_sum, cg_real_time

    # 通过配置文件，初始化飞机信息
    def init_aircraft_by_file(self, aircraft_config_file_path):
        # 加载配置文件
        with open(aircraft_config_file_path, 'r') as config_file_obj:
            config_parser = configparser.ConfigParser()
            config_parser.read(aircraft_config_file_path, encoding='utf-8-sig')

        # 飞机型号
        self.aircraft_type = config_parser.get('general', 'aircraft_type')
        # 飞机编号
        self.aircraft_id = config_parser.get('general', 'aircraft_id')
        # 平均气动弦长
        self.mean_aero_chord = config_parser.get('configuration', 'mean_aero_chord')
        # 机翼平均气动力弦长前缘点航向位置
        self.mac_front_distance = config_parser.get('configuration', 'mac_front_distance')
        # 飞机框位图路径
        self.aircraft_frame_pic_path = config_parser.get('configuration', 'aircraft_frame_pic_path')

        # 活动部件对飞机重心的影响，部件状态和力矩的对应关系表
        units = config_parser.options('mobilize_unit_cg_influence')
        for unit_name in units:
            unit_value = config_parser.get('mobilize_unit_cg_influence', unit_name)
            self.mobilize_unit_cg_influence[unit_name] = unit_value

        # 重量限制，重量限制和限制值的对应关系表
        items = config_parser.options('weight_limit')
        for item_name in items:
            item_value = config_parser.get('weight_limit', item_name)
            self.weight_limit[item_name] = item_value

        # 重心限制
        items = config_parser.options('cg_limit')
        for item_name in items:
            item_value = config_parser.get('cg_limit', item_name)
            item_value = self.process_str_to_2d_list(item_value)
            self.cg_limit[item_name] = item_value

        # 燃油限制
        items = config_parser.options('fuel_limit')
        for item_name in items:
            item_value = config_parser.get('fuel_limit', item_name)
            self.fuel_limit[item_name] = item_value

        # 起飞安定面配平值
        items = config_parser.options('take_off_trim_value')
        for item_name in items:
            item_value = config_parser.get('take_off_trim_value', item_name)
            item_value = self.process_str_to_2d_list(item_value)
            self.take_off_trim_value[item_name] = item_value

        # 主要部件重量重心信息
        items = config_parser.options('major_stowage')
        for item_name in items:
            item_value = config_parser.get('major_stowage', item_name)
            item_value = item_value[1:-1]
            self.major_stowage_data[item_name] = [float(item_value.split(',')[0]), float(item_value.split(',')[1])]

    # 添加使用项目
    def operation_item_add(self, item_info):
        self.stowage_info['operation_items'].append(item_info)

    # 修改使用项目
    def operation_item_edit(self, index, item_info):
        if index < len(self.stowage_info['operation_items']):
            self.stowage_info['operation_items'][index] = item_info

    # 删除使用项目
    def operation_item_del(self, index):
        if index < len(self.stowage_info['operation_items']):
            self.stowage_info['operation_items'].pop(index)

    @staticmethod
    # 将字符串型2*n数组转成数值型数组，类型如：'[[12,34],[56,78]]'
    def process_str_to_2d_list(two_dim_list_str):
        two_dim_list_str = two_dim_list_str[2:-2]
        two_dim_list_str = two_dim_list_str.split('],[')
        result_2d_list = [[float(item.split(',')[0]), float(item.split(',')[1])] for item in two_dim_list_str]
        return result_2d_list

    # 设置称重信息
    def set_weigh_info(self, **kwargs):
        for k in kwargs:
            if k in self.weigh_info:
                if isinstance(kwargs[k], type(self.weigh_info[k])):
                    self.weigh_info[k] = kwargs[k]

    # 设置燃油信息
    def set_fuel_info(self, **kwargs):
        for k in kwargs:
            if k in self.fuel_info:
                if isinstance(kwargs[k], type(self.fuel_info[k])):
                    self.fuel_info[k] = kwargs[k]