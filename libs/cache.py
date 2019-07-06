from dao.cart_dao import CartDao
from libs import r, r2
import uuid

cart_dao = CartDao()
def new_token():
    return uuid.uuid4().hex


def save_token(token, user_id):
    # 保存token
    r.set(token, user_id)
    r.expire(token, 12*3600)  # 有效时间： 12小时


def check_token(token):
    # 验证token
    return r.exists(token)


def get_token_user_id(token):
    # 通过token获取user_id
    if check_token(token):
        return r.get(token).decode()


def set_cart(id, key, value):
    """购物车记录写入到redis中，通过用户"""
    r2.hmset(id, {key: value})

def cart_all(ssid):
    """获取购物车记录"""
    key_value = r2.hgetall(ssid)
    if not key_value:
        ls = ssid.split("-")
        data = CartDao().show_cart(ls[0], ls[1])
        if data:
            for good in data:
                r2.hset(good.get("cart_goods_id"), good.get("cart_good_num"))
    else:
        data = {key.decode(): value.decode() for key, value in key_value.items()}
    return data


"""将用户的所有redis里购物车保存到数据库"""


def save_cart(user_id):
    data = r2.keys(str(user_id) + "-*")
    if data:
        for key in data:
            key = key.decode()
            datas = r2.hgetall(key)
            for i, j in datas.items():
                cart_dao.add_cart(key, int(i.decode()), int(j.decode()))

