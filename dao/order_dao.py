from dao import BaseDao



class OrderDao(BaseDao):
    def search_all(self, *args):
        sql = "select * from carts where cart_good_select = 1 and cart_user_id = %s  and cart_shop_id = %s"
        print(sql)
        data = super(OrderDao, self).query(sql, *args)
        return data

    def save(self, **value):
        super(OrderDao, self).save("orders", **value)

    def list(self,args):
        return super(OrderDao, self).search_all("orders")

    def update(self,key,value,where,args):
        super(OrderDao, self).update("orders", key, value, where=where, args=args)





if __name__ == '__main__':
    print(OrderDao().search_all(4, 4))