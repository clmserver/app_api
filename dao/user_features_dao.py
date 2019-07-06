# -*- coding: utf-8 -*- 
# @Time : 2019/7/2 10:04

# 添加地址
from dao import BaseDao
from dao.user_dao import UserDao



class User_Featuare_Dao(BaseDao):

    def saves(self, **values):
            return super(User_Featuare_Dao, self).save('user_address', **values)

    # 显示地址
    def se_address(self,user_id):
        sql = 'select * from user_address where user_id = %s'
        user_profile = self.query(sql, user_id)
        return user_profile


    # 修改地址

    def up_address(self, **data):
        sql = "UPDATE user_address set address='%(address)s' ,bottom='%(bottom)s' ,name='%(name)s' ,phone=%(phone)s,sex='%(sex)s' ,tag='%(tag)s',user_id=%(user_id)s where id=%(id)s " % (
            data)
        print(sql)
        updata_address = self.query(sql)
        print(updata_address)
        return updata_address

    # 删除地址
    def del_address(self, id,user_id):
        sql = "delete from user_address where id=%s and user_id=%s"
        updata_address = self.query(sql, id, user_id)


    # 评价
    def user_comment(self,user_id):
        return super(User_Featuare_Dao, self).search_all("valuetion", where="v_user_id", args=user_id, page=1,
                                               page_size=10)

    # 获取商铺评论
    def shop_pl(self,v_shop_id):
        yt_gp_sql = 'select *  from valuetion where is_url=1 and good_or_bad=0 and v_shop_id=%s;'
        wt_gp_sql = 'select *  from valuetion where is_url=0 and good_or_bad=0 and v_shop_id=%s;'
        yt_bp_sql = 'select *  from valuetion where is_url=1 and good_or_bad=1 and v_shop_id=%s;'
        wt_bp_sql = 'select *  from valuetion where is_url=0 and good_or_bad=1 and v_shop_id=%s;'
        good_is_num = self.query(yt_gp_sql, v_shop_id)
        good_no_num = self.query(wt_gp_sql, v_shop_id)
        bad_is_num = self.query(yt_bp_sql, v_shop_id)
        bad_no_num = self.query(wt_bp_sql, v_shop_id)
        data = {
            "goodp_num":{
                "good_is_num":good_is_num,
                "good_no_num":good_no_num,
            },
            "badp_num":{
                "bad_is_num":bad_is_num,
                "bad_no_num":bad_no_num

            }
        }
        return data


    # 用户余额
    def user_balance(self,user_id):
        sql = "select u_burse_balance from users where id=%s"
        burse_balance = self.query(sql, user_id)
        #num = burse_balance[0].get('u_burse_balance')
        return burse_balance
    # 用户所有银行卡
    def user_cards(self,user_id):
        sql = "select count(card_num) as card_num from bank_card where card_user_id=%s"
        burse_balance = self.query(sql, user_id)
        return burse_balance

    # 店铺中满减的活动
    def discount2_des(self):
        sql = "select info from discounts2 where type_name='减'"
        discounts2 = self.query(sql)
        return discounts2

    def user_complaint(self,**values):
        return super(User_Featuare_Dao, self).save('complaint', **values)

    def user_suggest(self,**values):
        return super(User_Featuare_Dao, self).save('suggest', **values)

if __name__ == '__main__':
    data = User_Featuare_Dao().shop_pl(3)
    print(data)