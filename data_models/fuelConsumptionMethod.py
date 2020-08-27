# -*- coding: utf-8 -*-

# 燃油消耗曲线计算
import math
from data_models.stowageSQL import sql_information
import numpy as np
from scipy import interpolate
import numpy as np
from matplotlib import pyplot as plt


class FuleConsumption():
    def __init__(self):
        self.LG_up_force = 940000
        self.Xe = 19837

    def fuel_display_deviation(self, fuel_display, position):
        sql = sql_information()
        fuel = sql.query_data(
            'SELECT fuel_display,actual_fuel FROM fuel_display_deviation where wing_fuel_tank="' + position + '"')

        l = len(fuel)
        list = []
        for i in range(l):
            list.append(float(fuel[i][0]))

        boundary = self.search(list, float(fuel_display))

        if type(boundary) == int:
            result = float(fuel[boundary][1])
        else:
            x = [float(fuel[boundary[0]][0]), float(fuel[boundary[1]][0])]
            y = [float(fuel[boundary[0]][1]), float(fuel[boundary[1]][1])]
            f = interpolate.interp1d(x, y, kind='linear')
            result = f(fuel_display)

        return result

    def fuel_and_arm(self, actual_fuel, position):
        sql = sql_information()
        fuel = sql.query_data(
            'SELECT actual_fuel,balance_arm FROM fuel_and_arm where ﻿wing_fuel_tank="' + position + '"')

        l = len(fuel)
        list = []
        for i in range(l):
            list.append(float(fuel[i][0]))

        boundary = self.search(list, float(actual_fuel))

        if type(boundary) == int:
            result = float(fuel[boundary][1])
        else:
            x = [float(fuel[boundary[0]][0]), float(fuel[boundary[1]][0])]
            y = [float(fuel[boundary[0]][1]), float(fuel[boundary[1]][1])]
            f = interpolate.interp1d(x, y, kind='linear')
            result = f(actual_fuel)

        return result

    def search(self, list, key):
        left = 0  # 左边界
        right = len(list) - 1  # 右边界
        while left <= right:
            mid = round((left + right) / 2)  # 取得中数
            if key > list[mid]:
                left = mid + 1
            elif key < list[mid]:
                right = mid - 1
            else:
                return mid
        if left > right:
            boundary = [right, left]
            return boundary

    def fuel_consumption_force_caculate(self, display_fuel):
        fuel_consumption_sum = {'weight': [], 'force': []}
        sum_fuel = sum(display_fuel.values())
        wing_consumption_flag = 225
        actual_fuel = {'left': self.fuel_display_deviation(display_fuel['left'], 'left'),
                       'right': self.fuel_display_deviation(display_fuel['right'], 'right'),
                       'central': self.fuel_display_deviation(display_fuel['central'], 'central')}
        actual_fuel_arm = {'left': self.fuel_and_arm(actual_fuel['left'], 'left'),
                           'right': self.fuel_and_arm(actual_fuel['right'], 'right'),
                           'central': self.fuel_and_arm(actual_fuel['central'], 'central')}

        while (sum_fuel > 0):
            if display_fuel['central'] == 0:
                actual_fuel['left'] = self.fuel_display_deviation(display_fuel['left'], 'left')
                actual_fuel['right'] = self.fuel_display_deviation(display_fuel['right'], 'right')
                actual_fuel_arm['left'] = self.fuel_and_arm(actual_fuel['left'], 'left')
                actual_fuel_arm['right'] = self.fuel_and_arm(actual_fuel['right'], 'right')
                if display_fuel['left'] > 500:
                    display_fuel['left'] = display_fuel['left'] - 500
                    display_fuel['right'] = display_fuel['right'] - 500
                else:
                    display_fuel['left'] = 0
                    display_fuel['right'] = 0

            if wing_consumption_flag == 0 and display_fuel['central'] > 1:
                actual_fuel['central'] = self.fuel_display_deviation(display_fuel['central'], 'central')
                actual_fuel_arm['central'] = self.fuel_and_arm(display_fuel['central'], 'central')
                if display_fuel['central'] > 800:
                    display_fuel['central'] = display_fuel['central'] - 800
                else:
                    display_fuel['central'] = 0

            if wing_consumption_flag > 0:
                actual_fuel['left'] = self.fuel_display_deviation(display_fuel['left'], 'left')
                actual_fuel['right'] = self.fuel_display_deviation(display_fuel['right'], 'right')
                actual_fuel_arm['left'] = self.fuel_and_arm(actual_fuel['left'], 'left')
                actual_fuel_arm['right'] = self.fuel_and_arm(actual_fuel['right'], 'right')

                display_fuel['left'] = display_fuel['left'] - 45
                display_fuel['right'] = display_fuel['right'] - 45
                wing_consumption_flag = wing_consumption_flag - 45

            sum_fuel = sum(display_fuel.values())
            sum_fuel_actual = sum(actual_fuel.values())
            fuel_consumption_sum['weight'].append(sum_fuel_actual)
            sum_fuel_force = actual_fuel['left'] * actual_fuel_arm['left'] + actual_fuel['right'] * actual_fuel_arm[
                'right'] + actual_fuel['central'] * actual_fuel_arm['central']
            fuel_consumption_sum['force'].append(sum_fuel_force)

        return fuel_consumption_sum

    def fuel_consumption_CG_caculate(self, ZFW, fuel_consumption_sum):
        l = len(fuel_consumption_sum['weight'])
        CG_list = {"LG_up": [], "LG_down": []}

        for i in range(l):
            CG_LG_down = ((ZFW['force'] + fuel_consumption_sum['force'][i]) / (
                        ZFW['weight'] + fuel_consumption_sum['weight'][i]) - self.Xe) / 4268
            CG_LG_up = ((ZFW['force'] + fuel_consumption_sum['force'][i] - self.LG_up_force) / (
                        ZFW['weight'] + fuel_consumption_sum['weight'][i]) - self.Xe) / 4268
            CG_list["LG_up"].append(CG_LG_up)
            CG_list["LG_down"].append(CG_LG_down)

        return CG_list


#######测试############
# display_fuel = {"left": 2749.0, "right": 2749.0, "central": 11804.0}
# ZFW = {"weight": 44254, "force": 922128723.6}
#
# fuel = FuleConsumption()
# fuel_consumption_sum = fuel.fuel_consumption_force_caculate(display_fuel)
# CG_real_time = fuel.fuel_consumption_CG_caculate(ZFW, fuel_consumption_sum)
#
# plt.plot(CG_real_time['LG_up'], fuel_consumption_sum["weight"])
# plt.plot(CG_real_time['LG_down'], fuel_consumption_sum["weight"])
# plt.show()
