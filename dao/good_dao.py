from dao import BaseDao


class GoodDao(BaseDao):
    def list(self, id):
        return super(GoodDao, self).list("goods", ("id", "goods_name", "goods_picture", "goods_min_price"), where="id", args=id)