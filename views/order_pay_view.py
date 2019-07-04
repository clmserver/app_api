import uuid
from datetime import datetime

from flask import Blueprint, request, jsonify

from dao.cart_dao import CartDao
from dao.good_dao import GoodDao
from dao.order_dao import OrderDao
from dao.order_detail_dao import OrderDetailDao
from dao.user_dao import UserDao
from libs import r, r2

pay_blue = Blueprint("pay_blue", __name__)
dao = OrderDao()
gooddao = GoodDao()
userdao = UserDao()
cartdao = CartDao()

@pay_blue.route("/api/order/pay/", methods=("POST", ))
def pay_go():
    args = eval(request.get_data())
    user_id = args.get("user_id")
    shop_id = args.get("shop_id")
    sql = "select * from carts left join goods on carts.cart_goods_id = goods.id where cart_good_select = 1 and cart_user_id = %s and cart_shop_id = %s"
    data = OrderDao().query(sql, user_id, shop_id)
    if not data:
        return jsonify({
            "code": 300,
            "msg": "当前购物车为空"
        })
    sum = 0
    order_num = datetime.now().strftime("%Y%m%d%H%M%S") + uuid.uuid4().hex[-10:]
    for good in data:
        dic = {
            "order_num": order_num,
            "cart_card": good.get("cart_card"),
            "order_goods_id": good.get("cart_goods_id"),
            "order_goods_num": good.get("cart_good_num"),
            "order_shop_id": good.get("cart_shop_id"),
            "order_user_id": good.get("cart_user_id"),
            "order_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        sum += float(good.get("goods_min_price")) * int(good.get("cart_good_num"))
        dao.save(**dic)
    r.setex(order_num, sum, 900)
    r2.delete(str(user_id) + "-" + str(shop_id))
    sql = "delete from carts where (cart_user_id, cart_shop_id) = (%s, %s)"
    cartdao.query(sql, user_id, shop_id)
    return jsonify({
        "code": 200,
        "msg": "ok",
        "data": {
            "u_tel": UserDao().get_profile(user_id).get("u_tel"),
            "addr": "北京",
            "data": data
        }
    })


@pay_blue.route("/api/order/is_ok/", methods=("POST", ))
def is_ok():
    args = eval(request.get_data())
    user_id = args.get("user_id")
    shop_id = args.get("shop_id")
    order_num = args.get("order_num")
    if r.exists(order_num):
        print(r.get(order_num).decode())
        user = userdao.get_profile(user_id)
        u_burse = user.get("u_burse_balance")
        total = float(r.get(order_num).decode())
        if u_burse < total:
            return jsonify({
                "code": 302,
                "msg": "您的余额不足，请先充值"
            })
        dic = {
            "order_detail_shop_id": shop_id,
            "order_detail_tel":  user.get("u_tel"),
            "order_detail_addr": "abc",
            "order_detail_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "order_price": total,
            "order_num": order_num
        }
        sql = "update users set u_burse_balance = %s where id = %s"
        userdao.query(sql, u_burse - total, user_id)
        dao.update("order_status", 1, "order_num", order_num)
        OrderDetailDao().save(**dic)
        r.delete(order_num)
        return jsonify({
            "code": 200,
            "msg": "ok"
        })
    else:
        return jsonify({
            "code": 300,
            "msg": "该订单已失效"
        })
