# -*- coding: utf-8 -*-

import configparser


def create_config_file():
    with open('aircraft_stowage_soft_config.ini', 'w') as f:
        conf = configparser.ConfigParser()
        conf.read('aircraft_stowage_soft_config.ini')

        conf.add_section('general')
        conf.set('general', 'soft_name', '飞机配载设计软件')
        conf.set('general', 'default_weigh_info_export_dir', '.')
        conf.set('general', 'default_weigh_info_import_dir', '.')

        conf.write(f)


if __name__ == '__main__':
    create_config_file()
