# -*- coding: utf-8 -*-

# 飞机零油重量重心计算
from data_models.stowageSQL import sql_information

class ZFW():
    def __init__(self,Wt,Wf):
        self.Wt = Wt
        self.Wf = Wf

    def caculate_ZFW(self, ballast, OI):
        ZFW_weight = self.Wt + OI['weight']+ballast['weight']
        ZFW_force = self.Wf + OI['force']+ballast['force']
        ZFW = {"weight": ZFW_weight ,"force": ZFW_force}

        return ZFW

    def caculate_ballast(self, frame_ballast_dic):
        ballast_weight = []
        ballast_force = []
        sql = sql_information()
        for k in frame_ballast_dic.keys():
            ballast_coordinate = sql.query_data(
                 'SELECT id,coordinate FROM aircraft_frame where frame = "'+k+'" ')
            frame_id = str(ballast_coordinate[0][0]+1)
            next_ballast_coordinate = sql.query_data(
                'SELECT coordinate FROM aircraft_frame where id = "'+frame_id+'" ')

            frame_ballast_arm = ballast_coordinate[0][1] + (next_ballast_coordinate[0][0] - ballast_coordinate[0][1]) / 2

            frame_ballast_force = frame_ballast_dic[k] * frame_ballast_arm
            ballast_weight.append(frame_ballast_dic[k])

            ballast_force.append(frame_ballast_force)

        ballast = {'weight': sum(ballast_weight), 'force': sum(ballast_force)}
        return ballast


#######测试############
# frame_ballast_dic={'FR60':350,'FR61':350,'FR62':350,'FR63':250,'FR64':200}
# Wt=42308
# Wf=871166747.8
# OI = {"weight":446.5,"force":4615475.8} #使用项目
#
# t=ZFW(Wt,Wf)
# ballast = t.caculate_ballast(frame_ballast_dic) #配重
# ZFW = t.caculate_ZFW(ballast,OI) #零油重量
# print(ZFW)
