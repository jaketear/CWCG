# -*- coding: utf-8 -*-

import matplotlib
from cycler import cycler
from matplotlib import font_manager as ftm
from matplotlib.lines import Line2D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.ticker import AutoMinorLocator, PercentFormatter

from data_models import data_collector, config_info


class FuelConsumptionCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.figure_style_config()
        self.fig = Figure(figsize=(5, 4))
        # 初始化父类
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        self.toolbar = NavigationToolbar(self, parent=None)
        self.toolbar.hide()

        # 燃油消耗曲线对象
        self.line_gear_down = None
        self.line_gear_up = None

        self.plot_curve()

    # 根据燃油消耗数据自适应坐标
    def adjust_fuel_change_range(self, fuel_consumption_sum, cg_real_time):
        self.line_gear_down.set_data(cg_real_time['LG_down'], fuel_consumption_sum["weight"])
        self.line_gear_up.set_data(cg_real_time['LG_up'], fuel_consumption_sum["weight"])
        lg_down_max = max(cg_real_time['LG_down'])
        lg_down_min = min(cg_real_time['LG_down'])
        lg_up_max = max(cg_real_time['LG_up'])
        lg_up_min = min(cg_real_time['LG_up'])
        x_max = max([lg_down_max, lg_up_max])
        x_min = min([lg_down_min, lg_up_min])
        delta = x_max - x_min
        if delta != 0:
            x_max += delta / 10
            x_min -= delta / 10

        y_max = max(fuel_consumption_sum["weight"])
        y_min = min(fuel_consumption_sum["weight"])
        delta = y_max - y_min
        if delta != 0:
            y_max += delta / 10
            y_min -= delta / 10

        self.fig.axes[0].set_xlim([x_min, x_max])
        self.fig.axes[0].set_ylim([y_min, y_max])

    @staticmethod
    # 画布样式配置
    def figure_style_config():
        # 画布的背景色和边框色
        matplotlib.rcParams['figure.facecolor'] = 'white'
        matplotlib.rcParams['figure.edgecolor'] = 'white'
        # 坐标的背景色
        matplotlib.rcParams['axes.facecolor'] = 'white'
        # 坐标的边框色
        matplotlib.rcParams['axes.edgecolor'] = 'black'
        # 坐标的边框线宽
        matplotlib.rcParams['axes.linewidth'] = 1.0
        # 坐标文字的颜色
        matplotlib.rcParams['axes.labelcolor'] = 'black'
        # 设置标题颜色
        # matplotlib.rcParams['axes.titlecolor'] = 'white'
        # 设置曲线颜色
        matplotlib.rcParams['axes.prop_cycle'] = cycler('color', ['blue', 'red', '#00FFFF'])
        # 支持中文显示
        # matplotlib.rcParams['font.sans-serif'] = ['SimHei']
        matplotlib.rcParams['axes.unicode_minus'] = False
        # 设置刻度线向内
        matplotlib.rcParams['xtick.direction'] = 'in'
        matplotlib.rcParams['ytick.direction'] = 'in'
        # 设置刻度值颜色
        matplotlib.rcParams['xtick.color'] = 'black'
        matplotlib.rcParams['ytick.color'] = 'black'
        # 字体默认颜色
        matplotlib.rcParams['text.color'] = 'black'

    def plot_curve(self):
        self.fig.clf()
        ax = self.fig.add_subplot(1, 1, 1)

        fuel_consumption_sum, cg_real_time = data_collector.get_fuel_consume_data()

        self.line_gear_down, = ax.plot(cg_real_time['LG_down'], fuel_consumption_sum["weight"], lw=2)
        self.line_gear_up, = ax.plot(cg_real_time['LG_up'], fuel_consumption_sum["weight"], lw=2)

        ax.legend((self.line_gear_down, self.line_gear_up), ('起落架放下', '起落架收上'),
                  prop=ftm.FontProperties(fname=config_info.font_dir, size=15),
                  frameon=False)
        ax.xaxis.set_major_formatter(PercentFormatter(xmax=1))
        ax.xaxis.set_minor_locator(AutoMinorLocator(n=5))
        ax.yaxis.set_minor_locator(AutoMinorLocator(n=2))
        ax.grid(which='major', linestyle='-', color='0.45')
        ax.grid(which='minor', linestyle='-', color='0.75')

        # ax.plot([0, 1], [0, 1])
        # ax.plot([0, 1], [1, 0])

    # 更新燃油消耗曲线
    def refresh_fuel_consume_line_data(self):
        if isinstance(self.line_gear_down, Line2D) and isinstance(self.line_gear_up, Line2D):
            fuel_consumption_sum, cg_real_time = data_collector.get_fuel_consume_data()
            self.line_gear_down.set_data(cg_real_time['LG_down'], fuel_consumption_sum["weight"])
            self.line_gear_up.set_data(cg_real_time['LG_up'], fuel_consumption_sum["weight"])

            self.adjust_fuel_change_range(fuel_consumption_sum, cg_real_time)

            self.draw()
