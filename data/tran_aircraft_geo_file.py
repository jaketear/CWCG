# -*- coding: utf-8 -*-

# 用于将存储在excel中的飞机几何数据转换到json文件中
import os
import xlrd
import json


if __name__ == '__main__':
    aircraft_geo_data = dict(fuel_geo_out_frame=None, fuel_geo_center_tank=None, fuel_geo_left_tank=None,
                             fuel_geo_right_tank=None, aircraft_geo_frame=None)
    file_dir = r'.\\飞机外形数据 - 副本.xls'
    if os.path.isfile(file_dir):
        aircraft_frame = None
        # 打开文件
        xl_data = xlrd.open_workbook(file_dir)
        # 选择第一个sheet
        table = xl_data.sheet_by_index(0)
        if table.ncols >= 8:
            # 读取飞机外轮廓数据
            aircraft_frame = zip(table.col_values(8)[1:], table.col_values(9)[1:])
            aircraft_geo_data['aircraft_geo_frame'] = [(x, y) for x, y in aircraft_frame if x]

            # 读取油箱外轮廓数据
            aircraft_fuel_out_frame = zip(table.col_values(0)[1:], table.col_values(1)[1:])
            aircraft_geo_data['fuel_geo_out_frame'] = [(x, y) for x, y in aircraft_fuel_out_frame if x]

            aircraft_center_fuel_frame = zip(table.col_values(2)[1:], table.col_values(3)[1:])
            aircraft_geo_data['fuel_geo_center_tank'] = [(x, y) for x, y in aircraft_center_fuel_frame if x]

            aircraft_left_fuel_frame = zip(table.col_values(4)[1:], table.col_values(5)[1:])
            aircraft_geo_data['fuel_geo_left_tank'] = [(x, y) for x, y in aircraft_left_fuel_frame if x]

            aircraft_right_fuel_frame = zip(table.col_values(6)[1:], table.col_values(7)[1:])
            aircraft_geo_data['fuel_geo_right_tank'] = [(x, y) for x, y in aircraft_right_fuel_frame if x]

            with open(r'aircraft_geo_data.json', 'w') as f:
                json.dump(aircraft_geo_data, f, indent=4)
