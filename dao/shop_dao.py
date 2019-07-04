from dao import BaseDao

"""店铺"""


class ShopDao(BaseDao):

    """根据分类获取店铺信息"""
    def all_shop(self, small_type_id):
        return super(ShopDao, self).search_all("shops", where="shop_small_type_id", args=small_type_id, page=1, page_size=10)
    """根据id获取店铺信息"""
    def get_shop(self, shop_id):
        return super(ShopDao, self).list("shops", where="id", args=shop_id, page=1,
                                               page_size=20)
    """根据id获取食品信息"""
    def get_good(self, good_id):
        return super(ShopDao, self).list("goods", where="id", args=good_id, page=1,
                                               page_size=10)

    """根据店铺id获取店铺商品"""
    def get_shop_goods(self,shop_id):
        return super(ShopDao,self).search_all("goods",where="g_shop_id", args=shop_id, page=1,
                                        page_size=10)

    """根据id获取店铺评价信息"""
    def get_discounts2(self, type_name_shops_id):
        return super(ShopDao, self).search_all("discounts2", where="type_name_shops_id", args=type_name_shops_id,page=1,
                                               page_size=10)
    def get_poi_env(self, shop_id):
        return super(ShopDao, self).search_all("poi_env", where="shop_id", args=shop_id,page=1,
                                               page_size=10)
    def get_poi_service(self,shop_id):
        return super(ShopDao, self).search_all("poi_service", where="shop_id", args=shop_id,page=1,
                                               page_size=10)
