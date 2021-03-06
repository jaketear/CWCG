# -*- coding: utf-8 -*-

import pymysql
import sqlite3
import os

class sql_information():

    def query_data(self,sql):
        # connection = pymysql.connect('localhost', 'root', 'root', "weight_balance")
        connection = sqlite3.connect(os.path.abspath('.') + os.sep + 'data\\stowage.db')
        cursor = connection.cursor()
        query_data = None
        try:
            # cursor.execute('pragma table_info([cg_correction])')
            # print(cursor.fetchall())
            cursor.execute(sql)
            query_data = cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            if connection:
                cursor.close()
            if cursor:
                connection.close()

        return query_data
