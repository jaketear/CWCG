# -*- coding: utf-8 -*-

from socket import *

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtWidgets import (QHBoxLayout, QWidget, QVBoxLayout, QSpacerItem,
                             QSizePolicy, QToolButton, QLabel, QLineEdit, QPushButton,
                             QDialog, QMessageBox)

from data_models import config_info, data_collector


class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.resize(700, 400)
        self.setWindowFlag(Qt.FramelessWindowHint)
        palette = QPalette()
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap(config_info.login_pic_dir)))
        self.setPalette(palette)

        self.horizontalLayout_2 = QHBoxLayout(self)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.widget_picture = QWidget(self)
        self.horizontalLayout_2.addWidget(self.widget_picture)
        self.widget_login = QWidget(self)
        self.verticalLayout = QVBoxLayout(self.widget_login)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        spacer_item = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacer_item)
        self.btn_close = QToolButton(self.widget_login)
        self.btn_close.setStyleSheet('QToolButton {max-width: 42px; min-width: 42px;'
                                     'max-height: 24px; min-height: 24px;'
                                     'border-image:url(\'./icon/close_login_normal.ico\')}'
                                     'QToolButton:hover {border-image:url(\'./icon/close_login_hover.ico\')}'
                                     'QToolButton:pressed {border-image:url(\'./icon/close_login_press.ico\')}')
        self.horizontalLayout.addWidget(self.btn_close)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.v_layout = QVBoxLayout()
        self.v_layout.setContentsMargins(20, 0, 80, 40)
        self.v_layout.setSpacing(14)
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.v_layout.addItem(spacer_item)
        self.label_login = QLabel(self.widget_login)
        self.label_login.setAlignment(Qt.AlignCenter)
        self.label_login.setStyleSheet('QLabel { background-color: transparent;'
                                       'font-family: \'Microsoft YaHei UI\';'
                                       'font-weight: bold; font-size: 24px;'
                                       'color: white}')
        self.v_layout.addWidget(self.label_login)
        self.line_edit_user_name = QLineEdit(self.widget_login)
        self.line_edit_user_name.setStyleSheet('QLineEdit { background-color: transparent;'
                                               'max-height: 32px; min-height: 32px;'
                                               'font-family: \'Microsoft YaHei UI\';'
                                               'font-size: 20px; color: white; border-bottom: 2px solid white;'
                                               'border-top: none}')
        self.v_layout.addWidget(self.line_edit_user_name)
        self.line_edit_password = QLineEdit(self.widget_login)
        self.line_edit_password.setEchoMode(QLineEdit.Password)
        self.line_edit_password.setStyleSheet('QLineEdit { background-color: transparent;'
                                              'max-height: 32px; min-height: 32px;'
                                              'font-family: \'Microsoft YaHei UI\';'
                                              'font-size: 20px; color: white; border-bottom: 2px solid white;'
                                              'border-top: none}')
        self.v_layout.addWidget(self.line_edit_password)
        self.btn_login = QPushButton(self.widget_login)
        self.btn_login.setStyleSheet('QPushButton { max-height: 32px; min-height: 32px;'
                                     'background-color: #5397EF;'
                                     'border-radius: 4px;'
                                     'font-family: \'Microsoft YaHei UI\';'
                                     'font-size: 20px; font-weight: bold; color: white }'
                                     'QPushButton:pressed {padding-left: 3px; padding-top: 3px}')
        self.v_layout.addWidget(self.btn_login)
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.v_layout.addItem(spacer_item)
        self.verticalLayout.addLayout(self.v_layout)
        self.horizontalLayout_2.addWidget(self.widget_login)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)

        self.translate()

        self.line_edit_user_name.setFocus()

        self.btn_close.clicked.connect(self.reject)
        self.btn_login.clicked.connect(self.login_soft)

    # 验证用户登录信息
    @staticmethod
    def confirm_user_info(username, password):
        host = 'localhost'
        port = 21567
        buf_size = 1024
        address = (host, port)

        tcp_cli_sock = socket(AF_INET, SOCK_STREAM)
        try:
            tcp_cli_sock.connect(address)

            while True:
                data = 'confirm user info'
                tcp_cli_sock.send(bytes(data, encoding='utf-8'))
                data = tcp_cli_sock.recv(buf_size)
                if data.decode('utf-8') == 'get confirm user info':
                    data = username + ' ' + password
                    tcp_cli_sock.send(bytes(data, encoding='utf-8'))
                    data = tcp_cli_sock.recv(buf_size)
                    result = data.decode('utf-8')
                    authority_lever = result.split(' ')[0]
                    if result.split(' ')[0] == '1':
                        tcp_cli_sock.close()
                        return True, authority_lever
                    else:
                        tcp_cli_sock.close()
                        return False, authority_lever
        except OSError:
            tcp_cli_sock.close()
            return True, 'conn error'

    # 根据用户输入的登录信息判断是否允许登录
    def login_soft(self):
        username = self.line_edit_user_name.text()
        password = self.line_edit_password.text()
        if username and password:
            if username.isdigit():
                result, authority_lever = self.confirm_user_info(username, password)
                if result:
                    if authority_lever != 'conn error':
                        data_collector.user_authority = authority_lever
                        self.accept()
                    else:
                        QMessageBox.information(self, '提示', '无法连接服务器，请稍后重试！')
                else:
                    self.line_edit_user_name.clear()
                    self.line_edit_password.clear()
                    self.line_edit_user_name.setFocus()
                    QMessageBox.information(self, '提示', '用户名或密码错误！')
            else:
                self.line_edit_user_name.clear()
                self.line_edit_user_name.setFocus()
                QMessageBox.information(self, '提示', '用户名为工号，请输入正确的工号！')
        else:
            QMessageBox.information(self, '提示', '用户名或密码不能为空！')

    def translate(self):
        self.label_login.setText("登录配载设计软件")
        self.line_edit_user_name.setPlaceholderText("用户名")
        self.line_edit_password.setPlaceholderText("密码")
        self.btn_login.setText("登  录")