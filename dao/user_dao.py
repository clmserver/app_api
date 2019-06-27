from dao import BaseDao


class UserDao(BaseDao):

    def save(self, **values):   #插入或者更新
        return super(UserDao, self).save('users', **values)

    def get_id(self,where,args):     #获取用户用户id
        user = super(UserDao, self).list("users", "id", where=where,args=args)
        if user:
            return user['id']

    def get_pwd(self,where,args):       #获取用户的密码
        user = super(UserDao, self).list("users", "u_password", where=where,args=args)
        if user:
            print(user['u_password'])
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
        sql = "select * from users " \
              "where user_id=%s"
        user_profile = self.query(sql, user_id)
        if user_profile:
            return user_profile[0]

    def set_userinfo(self,key,value,where,args):
        return super(UserDao, self).update('users',key,value,where,args)

    def del_userinfo(self,id):
        return super(UserDao,self).delete('users',id)

if __name__ == '__main__':
    dao = UserDao()
    print(dao.set_userinfo('u_username','KMP18309182914','xx','xxxx'))