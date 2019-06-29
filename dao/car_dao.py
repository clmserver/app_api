from dao import BaseDao


class CarDao(BaseDao):
    """购物车"""
    """添加购物车"""
    def add_cart(self, user_id, goods_id, shop_id):
        pass


if __name__ == '__main__':
    CarDao().check_goods(1)


