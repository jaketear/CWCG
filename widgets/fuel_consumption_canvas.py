# -*- coding: utf-8 -*-

import matplotlib
from cycler import cycler
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class FuelConsumptionCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.figure_style_config()
        self.fig = Figure(figsize=(5, 4))
        # 初始化父类
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        self.toolbar = NavigationToolbar(self, parent=None)
        self.toolbar.hide()

    @staticmethod
    # 画布样式配置
    def figure_style_config():
        # 画布的背景色和边框色
        matplotlib.rcParams['figure.facecolor'] = '#041328'
        matplotlib.rcParams['figure.edgecolor'] = '#041328'
        # 坐标的背景色
        matplotlib.rcParams['axes.facecolor'] = '#041328'
        # 坐标的边框色
        matplotlib.rcParams['axes.edgecolor'] = '#35a5f1'
        # 坐标的边框线宽
        matplotlib.rcParams['axes.linewidth'] = 1.0
        # 坐标文字的颜色
        matplotlib.rcParams['axes.labelcolor'] = 'white'
        # 设置标题颜色
        # matplotlib.rcParams['axes.titlecolor'] = 'white'
        # 设置曲线颜色
        matplotlib.rcParams['axes.prop_cycle'] = cycler('color', ['#FCF123', '#FF0090', '#00FFFF'])
        # 支持中文显示
        # matplotlib.rcParams['font.sans-serif'] = ['SimHei']
        matplotlib.rcParams['axes.unicode_minus'] = False
        # 设置刻度线向内
        matplotlib.rcParams['xtick.direction'] = 'in'
        matplotlib.rcParams['ytick.direction'] = 'in'
        # 设置刻度值颜色
        matplotlib.rcParams['xtick.color'] = 'white'
        matplotlib.rcParams['ytick.color'] = 'white'
        # 字体默认颜色
        matplotlib.rcParams['text.color'] = 'white'

