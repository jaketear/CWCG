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
if config_parser.get('general', 'default_weigh_info_export_dir') == '.':
    default_weigh_info_export_dir = current_dir
else:
    default_weigh_info_export_dir = config_parser.get('general', 'default_weigh_info_export_dir')
# 称重信息导入文件的默认路径
if config_parser.get('general', 'default_weigh_info_import_dir') == '.':
    default_weigh_info_import_dir = current_dir
else:
    default_weigh_info_import_dir = config_parser.get('general', 'default_weigh_info_import_dir')


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
