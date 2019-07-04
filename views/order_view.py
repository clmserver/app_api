from flask import Blueprint, request, jsonify

from dao.order_dao import OrderDao
from dao.order_detail_dao import OrderDetailDao

order_blue = Blueprint("order_blue", __name__)
order_dao = OrderDao()
order_detail = OrderDetailDao()


@order_blue.route("/api/order/all/", methods=("POST",))
def order_all():
    user_id = eval(request.get_data()).get("user_id")
    sql = "select * from orders where order_user_id = %s group by order_num"
    sql2 = "select * from orders where order_num = '%s' "
    all = order_dao.query(sql, user_id)
    for data in all:
        data["good"] = order_dao.query(sql2, data.get("order_num"))
    return jsonify({
        "code": 200,
        "msg": "ok",
        "data": all
    })

@order_blue.route("/api/order/detail/", methods=("POST",))
def order_detail():
    order_num = eval(request.get_data()).get("order_num")
    sql = "select * from order_detail where order_num = '%s'"
    sql2 = "select * from orders where order_num = '%s' "
    all = OrderDetailDao().query(sql, order_num)
    for key in all:
        key["goods"] = order_dao.query(sql2, key.get("order_num"))

    return jsonify({
        "code": 200,
        "msg": "ok",
        "data": all
    })


