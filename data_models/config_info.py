# -*- coding: utf-8 -*-

import os
import configparser

# 当前工作路径
current_dir = os.path.abspath('.')
# 配置文件所在的路径
config_file_path = current_dir + os.sep + 'data\\aircraft_stowage_soft_config.ini'
# 加载软件配置文件
with open(config_file_path, 'r') as config_file_obj:
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file_path)

# 软件名称
soft_name = config_parser.get('general', 'soft_name')

# 称重信息导出文件的默认路径
default_weigh_info_export_dir = config_parser.get('general', 'default_weigh_info_export_dir')
# 称重信息导入文件的默认路径
default_weigh_info_import_dir = config_parser.get('general', 'default_weigh_info_import_dir')

# 图标
icon_main_window = config_parser.get('icon_path', 'icon_main_window')
icon_arrow_close = config_parser.get('icon_path', 'icon_arrow_close')
icon_arrow_open = config_parser.get('icon_path', 'icon_arrow_open')
icon_select_aircraft = config_parser.get('icon_path', 'icon_select_aircraft')

# 微软雅黑字体路径
font_dir = current_dir + os.sep + 'data\\msyh.ttf'

# ui样式
# 通用提示字体大小
general_tip_font_size = int(config_parser.get('ui_style', 'general_tip_font_size'))
# 树控件中项的大小
tree_review_item_height = int(config_parser.get('ui_style', 'tree_review_item_height'))
# 按钮选中的颜色
button_selected_color = config_parser.get('ui_style', 'button_selected_color')
# 按钮未选中的颜色
button_un_selected_color = config_parser.get('ui_style', 'button_un_selected_color')
# 按钮选中的阴影颜色
button_selected_shadow_color = config_parser.get('ui_style', 'button_selected_shadow_color')
# 按钮未选中的阴影颜色
button_un_selected_shadow_color = config_parser.get('ui_style', 'button_un_selected_shadow_color')
# 工具按钮高度
button_height = int(config_parser.get('ui_style', 'button_height'))
# 工具按钮字体大小
button_font_size = int(config_parser.get('ui_style', 'button_font_size'))
# 标签的高度与宽度
label_height = int(config_parser.get('ui_style', 'label_height'))
label_width = int(config_parser.get('ui_style', 'label_width'))

# 树控件样式
tree_view_style = 'QTreeView { font-family: \'Microsoft YaHei UI\'; font-weight: bold;' +\
                  'font-size: %dpx;' % general_tip_font_size +\
                  'color: white; background-color: transparent; border: none}' \
                  'QHeaderView::section {font-family: \'Microsoft YaHei UI\';' \
                  'color: white; background-color: #3A3E5B; font-weight: bold; padding-left: 2px;' +\
                  'font-size: %dpx; height: %dpx; border: none}' % (general_tip_font_size, tree_review_item_height) +\
                  'QTreeView::item { height: %dpx; background-color: #9E9E9E;}' % tree_review_item_height +\
                  'QTreeView::branch {background-color: #9E9E9E}' \
                  'QTreeView::branch:open:has-children:!has-siblings,' \
                  'QTreeView::branch:open:has-children:has-siblings' +\
                  '{image: url(\'%s\');}' % icon_arrow_open +\
                  'QTreeView::branch:has-children:!has-siblings:closed,' \
                  'QTreeView::branch:closed:has-children:has-siblings' \
                  '{image: url(\'%s\');}' % icon_arrow_close
# 按钮风格
button_style = 'QToolButton { max-height: %dpx; min-height: %dpx;' % (button_height, button_height) +\
               'background-color: #4CAF50;'\
               'border-radius: 6px;' \
               'font-family: \'Microsoft YaHei UI\';' +\
               'font-size: %dpx;' % button_font_size +\
               'font-weight: bold;'\
               'color: white }'

# 标签样式
label_style = 'QLabel { background-color: transparent;' +\
              'min-height: %dpx; max-height: %dpx;' % (label_height, label_height) +\
              'min-width: %dpx; max-width: %dpx;' % (label_width, label_width) +\
              'font-family: \'Microsoft YaHei UI\';' +\
              'font-size: %dpx;' % general_tip_font_size +\
              'color: black; padding-left: 2px }'

# 数值显示标签样式
display_value_label_style = 'QLabel { background-color: #9E9E9E;' +\
                            'min-height: %dpx; max-height: %dpx;' % (label_height, label_height) +\
                            'min-width: %dpx; max-width: %dpx;' % (label_width, label_width) +\
                            'border-radius: 4px;' \
                            'font-family: \'Microsoft YaHei UI\';' \
                            'font-weight: bold;' +\
                            'font-size: %dpx;' % general_tip_font_size +\
                            'color: white; padding-left: 2px }'

# 机型信息界面中标题样式
aircraft_title_label_style = 'QLabel { background-color: #3A3E5B; font-family: \'Microsoft YaHei UI\';' +\
                             'min-height: %dpx; max-height: %dpx; padding-left: 2px;' % (label_height, label_height) +\
                             'font-weight: bold; font-size: %dpx; color: white}' % general_tip_font_size

# 复选框样式
combo_box_style = 'QAbstractItemView { background-color: white; }' \
                  'QComboBox { background-color: #03A9F4;'\
                  'border-radius: 4px;' +\
                  'min-height: %dpx; max-height: %dpx;' % (label_height, label_height) +\
                  'min-width: %dpx; max-width: %dpx;' % (label_width, label_width) +\
                  'font-family: \'Microsoft YaHei UI\';' +\
                  'font-size: %dpx;' % general_tip_font_size +\
                  'color: white }' \
                  'QComboBox::drop-down { border: 0px;}'\
                  'QComboBox::down-arrow { image: url(\'./icon/arrow.png\');'\
                  'height: 14px; width: 14px; }' \
                  'QComboBox:disabled { color: gray }'


# 设置配置信息
def set_config_info(**kwargs):
    # 打开配置文件，修改配置
    with open(config_file_path, 'r+') as f:
        set_config_parser = configparser.ConfigParser()
        set_config_parser.read(config_file_path)
        for key in kwargs:
            if set_config_parser.has_option('general', key):
                set_config_parser.set('general', key, kwargs[key])
            if key == 'default_weigh_info_export_dir':
                global default_weigh_info_export_dir
                default_weigh_info_export_dir = kwargs[key]
            if key == 'default_weigh_info_import_dir':
                global default_weigh_info_import_dir
                default_weigh_info_import_dir = kwargs[key]

        set_config_parser.write(f)
