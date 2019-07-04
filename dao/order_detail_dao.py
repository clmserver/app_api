from dao import BaseDao


class OrderDetailDao(BaseDao):

    def save(self, **values):
        super(OrderDetailDao, self).save("order_detail", **values)

    def search_all(self, order_num):
        return super(OrderDetailDao, self).search_all("order_detail", where="order_num", args=order_num)
