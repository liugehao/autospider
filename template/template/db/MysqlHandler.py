#!/usr/bin/env python
#coding:utf-8

import MySQLdb as mysqldb
import MySQLdb.cursors
from warnings import filterwarnings

filterwarnings('ignore', category=mysqldb.Warning)

class MysqlHandler(object):
    
    def __init__(self, conf, usedict=True):
        try:
            self.conf    = conf
            self.usedict = usedict

            if usedict:
                self.conn = mysqldb.connect(cursorclass=MySQLdb.cursors.DictCursor, **conf)
            else:
                self.conn = mysqldb.connect(**conf)

            self.conn.autocommit(True)
            self.cursor = self.conn.cursor()
        except Exception,e:
            print str(e)
            raise Exception('MysqlHandler init failed.')


    def __del__(self):
        try:
            self.cursor.close()
            self.conn.close()
        except:
            pass


    def exe(self, sql, params=()):
        try:
            self.cursor.execute(sql, params)
            if self.conn.affected_rows():
                return True
        except Exception,e:
            if str(e).lower().find('gone away')!=-1:
                self.__init__(self.conf)
                return self.exe(sql, params)
            print 'Error executing:\n  '+sql, '\n  params:', params, '\n  err info:', str(e)
        return False


    def close(self):
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    """用于测试"""
    confs = {
        'host': 'localhost',
        'user': 'user',
        'passwd': 'passwd',
        'db': 'db',
        }
    db = MysqlHandler(confs)

    sql = "SELECT id FROM sites WHERE name=%s"
    db.exe(sql, ('amazon', ))
    print db.cursor.fetchone()['id']