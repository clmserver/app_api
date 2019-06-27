from dao import BaseDao


class MainDao(BaseDao):
    """获取轮播图"""
    def wheel(self):
        return super(MainDao, self).list("wheel")
    """获取首页分类图标"""
    def main_type(self):
        return super(MainDao, self).list("shop_type", page_size=5)
    """获取首页小图标"""
    def main_small_img(self):
        return super(MainDao, self).list("shop_small_type",\
                                         where="shop_small_type_shoptype_id",
                                         args=16)
    """模糊查询商家"""
    def search(self, args):
        sql = "select * from shops where shop_name like '%%%s%%' or shop_s_name like '%%%s%%' "\
               "or shop_full_name like '%%%s%%' limit 0,8"

        return super(MainDao, self).query(sql, args, args, args)

    """返回优选商家"""

