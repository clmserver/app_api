from dao import BaseDao


class UserDao(BaseDao):

    def save(self, **values):   #插入或者更新
        return super(UserDao, self).save('users', **values)

    def get_id(self,where,args):     #获取用户用户id
        user = super(UserDao, self).list("users", ("id",), where=where,args=args)
        if user:
            return user['id']

    def get_pwd(self,where,args):       #获取用户的密码
        user = super(UserDao, self).list("users", ("u_password",), where=where,args=args)
        if user:
            return user['u_password']


    def check_phone(self, u_tel):
        # 检查电话是否已存在
        result = self.query('select id  from users where u_tel=%s', u_tel)
        return not bool(result)

    def check_username(self, u_username):
        # 检查电话是否已存在
        result = self.query('select u_username  from users where u_username=%s', u_username)
        return not bool(result)

    def get_profile(self, user_id):
        # 获取用户的详细信息
        return super(UserDao, self).list(table_name='users',where='id',args=user_id)

    def set_userinfo(self,key,value,where,args):
        return super(UserDao, self).update('users',key,value,where,args)

    def del_userinfo(self,id):
        return super(UserDao,self).delete('users',id)

    def get_wallet(self,user_id):    # lb
        # 获取银行卡信息
        sql = "select * from bank_card where card_user_id=%s"
        card_num = self.query(sql,user_id)
        if card_num:
            return card_num

    def get_burse(self,user_id):    #lb
        # 获取我的余额信息
        sql_user_id = "select u_burse_balance from users where id=%s"
        u_burse_balance = self.query(sql_user_id,user_id)
        print(sql_user_id)
        if u_burse_balance:
            return u_burse_balance

    def burse_change(self,user_id,burse_balance):    #lb
        # 修改数据库余额
        sql_burse = "update users set u_burse_balance=%s where id=%s"
        self.query(sql_burse,burse_balance,user_id)


if __name__ == '__main__':
    dao = UserDao()
    print(dao.set_userinfo('u_username','KMP18309182914','xx','xxxx'))