from dao import BaseDao

from libs.crypt import make_password, check_password

class UserDao(BaseDao):

    def save(self, **values):
        return super(UserDao, self).save('users', **values)

    def check_phone(self,phone):
        #检查电话号码是否存在
        result = self.query('select id from users where u_username=%s ','KMP'+phone)
        return not bool(result)

    def login(self, login_name, login_auth_str):
        sql = 'select id, login_auth_str from app_user_2 ' \
              'where login_name=%s and activated=%s'
        user_data = self.query(sql, login_name, 1)

        if user_data:
            user_id, auth_str = (user_data[0].get('id'),
                                 user_data[0].get('login_auth_str'))

            if check_password(login_auth_str, auth_str):
                # 验证成功
                user_profile = self.get_profile(user_id)
                if user_profile is None:
                    return {
                        'user_id': user_id,
                        'nick_name': login_name
                    }

                return user_profile
            # api_logger.warn('用户 %s 的口令不正确' % login_name)
            raise Exception('用户 %s 的口令不正确' % login_name)
        else:
            # api_logger.warn('查无此用户 %s' % login_name)
            raise Exception('查无此用户 %s' % login_name)
    def get_id(self,u_tel):
        #获取用户的id
        sql = 'select id from users where u_tel=%s'
        user_id = self.query(sql,u_tel)
        if user_id:
            return user_id[0]

    def get_profile(self, user_id):
        # 获取用户的详细信息
        sql = "select id, u_username, u_tel, u_headpic,u_nickname from users " \
              "where user_id=%s"
        user_profile = self.query(sql, user_id)
        if user_profile:
            return user_profile[0]
