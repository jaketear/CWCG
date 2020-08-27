# -*- coding: utf-8 -*-

# 飞机实测、试验空机重量重心计算
import math
from data_models.stowageSQL import sql_information
from data_models import data_collector
from scipy import interpolate

class CG():
    def __init__(self):
        self.Xe = 19837 ##机翼平均气动力弦长前缘点航向位置
        self.CA = 4268  ##机翼平均气动力弦长
        self.Xo = 10201.20    ##多装件重量
        self.Wo = 21.5    ##多装件平衡力臂
        self.Xs = 0   ##缺装件重量
        self.Ws = 0   ##缺装件重量

        # 重量、缓冲支柱行程、俯仰角
        self.actual_weight = dict(Wn=0, Wmr=0, Wml=0)
        self.actual_arm = dict(Lm=0, Ln=0)
        self.alpha = 0

        # 飞机实测重量、重心
        self.Wr = 0
        self.Xr_ = 0

        # 飞机空机重量、飞机空机重心
        self.Wt = 0
        self.Xt_ = 0

    # 计算缺装件
    def calculate_absence_unit(self):
        self.Ws = 0
        moment = 0
        for unit in data_collector.weigh_info['redundant_unit']:
            weight = unit[1]
            arm = unit[2]
            self.Ws += weight
            moment += weight * arm
        if self.Ws == 0:
            self.Xs = 0
        else:
            self.Xs = moment / self.Ws

    # 计算支柱行程
    def calculate_pillar(self):
        weigh_info = data_collector.weigh_info
        self.actual_arm['Ln'] = weigh_info['weigh_pillar_ln']
        self.actual_arm['Lm'] = (weigh_info['weigh_pillar_lmr'] + weigh_info['weigh_pillar_lml']) / 2.0

    # 计算多装件
    def calculate_redundant_unit(self):
        self.Wo = 0
        moment = 0
        for unit in data_collector.weigh_info['redundant_unit']:
            weight = unit[1]
            arm = unit[2]
            self.Wo += weight
            moment += weight * arm
        if self.Wo == 0:
            self.Xo = 0
        else:
            self.Xo = moment / self.Wo

    # 计算各起落架的承重
    def calculate_tyre_weight(self):
        weigh_info = data_collector.weigh_info
        wn_1 = weigh_info['weigh_tyre_nr'][0] + weigh_info['weigh_tyre_nl'][0]
        wml_1 = weigh_info['weigh_tyre_lo'][0] + weigh_info['weigh_tyre_li'][0]
        wmr_1 = weigh_info['weigh_tyre_ro'][0] + weigh_info['weigh_tyre_ri'][0]

        wn_2 = weigh_info['weigh_tyre_nr'][1] + weigh_info['weigh_tyre_nl'][1]
        wml_2 = weigh_info['weigh_tyre_lo'][1] + weigh_info['weigh_tyre_li'][1]
        wmr_2 = weigh_info['weigh_tyre_ro'][1] + weigh_info['weigh_tyre_ri'][1]

        self.actual_weight['Wn'] = (wn_1 + wn_2) / 2.0
        self.actual_weight['Wmr'] = (wml_1 + wml_2) / 2.0
        self.actual_weight['Wml'] = (wmr_1 + wmr_2) / 2.0

    ##计算飞机实测重量
    def calculate_Wr(self):
        self.calculate_tyre_weight()
        self.Wr = self.actual_weight['Wn']+self.actual_weight['Wmr']+self.actual_weight['Wml']

    ##计算飞机实测相对重心
    def calculate_Xp_(self):
        self.calculate_pillar()
        Xm=22323+self.actual_arm['Lm']*math.tan(5.912*math.pi/180)
        Xn=8918-self.actual_arm['Ln']*math.tan(1.9*math.pi/180)
        if self.Wr:
            Xp=(Xn*self.actual_weight['Wn']+Xm*(self.actual_weight['Wmr']+self.actual_weight['Wml']))/self.Wr
            Xp_=(Xp-self.Xe)/self.CA*100
            self.Xr_=Xp_+self.caclulate_detaCG()
        else:
            self.Xr_ = 0

    ##计算重心修正量
    def caclulate_detaCG(self):
        sql=sql_information()
        gravity = sql.query_data(
            'SELECT pitch_angle,deta_CG FROM cg_correction')
        # 查询成功
        if gravity:
            l=len(gravity)
            list = []
            for i in range(l):
                list.append(gravity[i][0])
            boundary = self.search(list, self.alpha)

            x = [gravity[boundary[0]][0],gravity[boundary[1]][0]]
            y = [gravity[boundary[0]][1],gravity[boundary[1]][1]]

            f = interpolate.interp1d(x, y, kind='linear')
            result = f(self.alpha)

            return result
        # 查询失败
        else:
            print('查询失败')
            return 0

    ##计算试验空机重量
    def caclulate_Wt(self):
        self.calculate_Wr()
        self.calculate_redundant_unit()
        self.calculate_absence_unit()
        self.Wt=self.Wr+self.Ws-self.Wo

    ##计算试验空机相对重心
    def caclulate_Xt_(self):
        self.calculate_Xp_()
        Xr=self.Xr_*(self.CA/100)+self.Xe
        if self.Wt:
            Xt=(Xr*self.Wr+self.Xs*self.Ws-self.Xo*self.Wo)/self.Wt
            self.Xt_=(Xt-self.Xe)/self.CA*100
        else:
            self.Xt_ = 0

    # 获得称重结果信息
    def get_weigh_result(self, item_name: str = ''):
        if item_name:
            if item_name == '实测重量':
                return self.Wr
            if item_name == '实测重心':
                return self.Xr_
            if item_name == '空机重量':
                return self.Wt
            if item_name == '空机重心':
                return self.Xt_
        else:
            return None

    # 重新计算空机重量重心
    def recalculate_weight_cg(self):
        self.caclulate_Wt()
        self.caclulate_Xt_()

    def search(self,list,key):
        left=0  #左边界
        right=len(list)-1   #右边界
        while left<=right:
            mid=round((left+right)/2) #取得中数
            if key>list[mid]:
                left=mid+1
            elif key<list[mid]:
                right=mid-1
            else:
                return mid
        else:
            boundary=[right,left]
            return boundary

#######测试############

# actual_weight={'Wn':5654,'Wml':18335,'Wmr':18340}
# actual_arm={'Ln':154,'Lm':188}
# alpha=-0.8
#
# t = CG()
# Wr = t.calculate_Wr(actual_weight) #飞机实测重量
# Xr_ = t.calculate_Xp_(Wr,actual_arm,alpha)
#
# Wt = t.caclulate_Wt(Wr)
# Xt = t.caclulate_Xt_(Xr_,Wr,Wt)
#
#
# print(Wr)
# print(Xr_)
# print(Wt)
# print(Xt)
