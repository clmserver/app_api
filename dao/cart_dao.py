from dao import BaseDao
from dao.good_dao import GoodDao
from dao.shop_dao import ShopDao


class CartDao(BaseDao):
    """添加到购物车"""
    def add_cart(self, cart_card, cart_goods_id, cart_good_num):
        cartlist = cart_card.split("-")
        if self.list("carts", where="(cart_goods_id, cart_card)", args=(cart_goods_id,cart_card)):
            sql = "update carts set cart_good_num = %s where (cart_goods_id, cart_card) = (%s, '%s')"
            super(CartDao, self).query(sql, cart_good_num, cart_goods_id, cart_card)
        else:
            dic={
                "cart_card":cart_card,
                "cart_goods_id": cart_goods_id,
                "cart_good_num": cart_good_num,
                "cart_user_id": cartlist[0],
                "cart_shop_id": cartlist[1]
            }
            super(CartDao, self).save("carts", **dic)
    """展示购物车"""
    def show_cart(self, user_id, shop_id):
        return super(CartDao, self).search_all("carts", where="(cart_user_id, cart_shop_id)", args=(user_id, shop_id))
    """"""
    def search_all(self, user_id):
        sql = "select * from carts inner join users on carts.cart_user_id = users.id inner join shops on cart_shop_id = shops.id where users.id = %s"
        return super(CartDao, self).query(sql, user_id)


    def update(self, key, value,where, args):
        super(CartDao, self).update("carts", key, value, where=where, args=args)


if __name__ == '__main__':
    CartDao().show_cart(4, 2)