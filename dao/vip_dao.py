# -*- coding: utf-8 -*- 
# @Time : 2019/6/27 10:57


from dao import BaseDao

class VipDao(BaseDao):

    def get_shop(self):
        # 获取30条店铺的详细信息
        sql = 'SELECT id,shop_name,img_url FROM shops ORDER BY RAND() LIMIT 30;'
        with self.db as c:
            c.execute(sql)
            data = c.fetchall()
            if data:
                data = list(data)
                ids = data[0].get('id')
                print(ids)
        return data

    def get_username(self, user_id):
        # 获取用户的姓名
        sql = "select u_username from users where id=%s"
        user_profile = self.query(sql, user_id)
        if user_profile:
            return user_profile[0]
