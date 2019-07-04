import pymysql
from pymysql.cursors import DictCursor

# DB_CONFIG = {
#     'host': 'localhost',
#     'port': 3306,
#     'user': 'mtadmin',
#     'password': 'mt9900',
#     'db': 'mt_api_db',
#     'charset': 'utf8'
# }
from logger import api_logger

DB_CONFIG = {
    'host': '10.35.162.134',
    'port': 3306,
    'user': 'root',
    'password': '710043oooo',
    'db': 'navmore',
    'charset': 'utf8'
}


class DB:
    def __init__(self):
        self.conn = pymysql.Connect(**DB_CONFIG)
        # api_logger.info("上下文",self.conn)
        # 如果上传的code中包含更新sql语句，如何自动创建(在服务器端)

    def __enter__(self):
        if self.conn is None:
            # 考虑数据库连接是断开的情况
            self.conn = pymysql.Connect(**DB_CONFIG)

        return self.conn.cursor(cursor=DictCursor)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()

        return True  # 异常不会继续向外抛出


class BaseDao():
    def __init__(self):
        self.db = DB()

    # 保存数据
    def save(self, table_name, **values):
        sql = 'insert into %s(%s) values(%s)' % \
              (table_name,
               ','.join(values.keys()),
               ','.join([ '%%(%s)s' % key for key in values.keys() ])
               )
        success = False
        with self.db as c:
            print(sql)
            c.execute(sql,args=values)
            success = True
        print(success)
        return success

    # 查询数据
    def list(self,table_name,*fileds, where=None,args=None,page=1,page_size=20):
        if not fileds:
            fileds = '*'
        sql = "select {} from {} where {}={} limit {},{}".format\
            (','.join(*fileds),table_name,where,args,(page-1)*page_size,page_size)
        with self.db as c:
            c.execute(sql)
            result = c.fetchone()
            return result


    """获取指定的数据"""

    def search_all(self, table_name, *fileds, where=None, args=None, page=1, page_size=20):
        if not fileds:
            fileds = '*'
        if where:
            sql = "select {} from {} where {}={} limit {},{}".format\
                (','.join(*fileds), table_name, where, args, (page-1)*page_size, page_size)
        else:
            sql = "select {} from {} limit {},{}".format\
                (','.join(*fileds), table_name, (page-1)*page_size, page_size)

        print(sql)
        with self.db as c:
            c.execute(sql)
            result = c.fetchall()
            return result

    """获取随机的数据"""

    def rand_all(self, table_name, *fileds, where=None, args=None, page=1, page_size=20):
        if not fileds:
            fileds = '*'
        if where:
            sql = "select {} from {} where {}={} order by rand() limit {},{}".format \
                (','.join(*fileds), table_name, where, args, (page - 1) * page_size, page_size)
        else:
            sql = "select {} from {} order by rand() limit {},{}".format \
                (','.join(*fileds), table_name, (page - 1) * page_size, page_size)

        with self.db as c:
            c.execute(sql)
            result = c.fetchall()
            return result

    # 更新数据
    def update(self,table_name,key,value,where=None,args=None):
        sql = "update {} set {}='{}' where {}='{}'".format(table_name,key,value,where,args)
        succuss = False
        with self.db as c:
            c.execute(sql)
            succuss = True
        return succuss

    # 删除数据
    def delete(self, table_name,where=None, args=None):
        if not where:
            sql = "delete from {} where id = {}"
        else:
            sql = "delete from {} where {}='{}'".format(table_name, where, args)
        success = False
        with self.db as c:
            c.execute(sql)
            success = True
        return success

    # 执行特定的sql语句
    def query(self, sql, *args):
        data = None
        sql = sql % args
        print(sql)
        with self.db as c:
            c.execute(sql)
            data = c.fetchall()
            if data:
                data = list(data)
        return data

    def count(self, table_name):
        pass



if __name__ == '__main__':
    conn = pymysql.Connect(**DB_CONFIG)