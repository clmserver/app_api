from dao import BaseDao

"""店铺"""


class ShopDao(BaseDao):

    """根据分类获取店铺信息"""
    def all_shop(self, small_type_id):
        return super(ShopDao, self).search_all("shops", where="shop_small_type_id", args=small_type_id, page=1, page_size=10)
    """根据id获取店铺信息"""
    def get_shop(self, shop_id):
        return super(ShopDao, self).search_all("shops", where="id", args=shop_id, page=1,
                                               page_size=10)