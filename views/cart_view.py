from flask import Blueprint, request, jsonify

from dao.cart_dao import CartDao
from dao.good_dao import GoodDao
from libs.cache import check_token, set_cart, cart_all, save_cart

cart_blue = Blueprint("cart_blue", __name__)
dao = CartDao()

"""给redis存储数据"""

@cart_blue.route("/api/cart/add/", methods=("POST", ))
def update_cart():
    if request.method == "POST":
        data = eval(request.get_data())
        token = data.get("token")
        user_id = data.get("user_id")
        good_id = data.get("good_id")
        shop_id = data.get("shop_id")
        good_num = data.get("good_num")
        if not check_token(token):
            if all((bool(user_id), bool(good_id), bool(shop_id), bool(good_num))):
                set_cart(str(user_id) + "-" + str(shop_id), good_id, good_num)
                return jsonify({
                    "code": 200,
                    "msg": "ok"
                })
            else:
                return jsonify({
                    "code": 207,
                    "msg": "缺少参数"
                })
        else:
            return jsonify({
                "code": 207,
                "msg": "请登陆在后访问"
            })

    else:
        return jsonify({
            "code": 207,
            "msg": "该方法需要POST请求"
        })


"""展示购物车"""


@cart_blue.route("/api/cart/show/", methods=("POST",))
def show_cart():
    data = eval(request.get_data())
    token = data.get("token")
    if token:
        return jsonify({
            "code": 207,
            "msg": "当前用户已过期"
        })
    shop_id = data.get("shop_id")
    user_id = data.get("user_id")
    if not all((bool(shop_id), bool(user_id))):
        return jsonify({
            "code": 207,
            "msg": "缺少相关参数"
        })
    good_data = cart_all(str(user_id) + "-" + str(shop_id))
    print(good_data)
    """获取商品信息"""
    ls = []
    if good_data:
        dao = GoodDao()
        for key, value in good_data.items():
            data = dao.list(key)
            print(data)
            ls.append({
                "goods": dao.list(key),
                "good_num": value
            })
        return jsonify({
            "code": 200,
            "msg": "ok",
            "data": {
                "user_id": user_id,
                "shop": shop_id,
                "data": ls
            }
        })
    else:
        return jsonify({
            "code": 207,
            "msg": "当前购物车为空"
        })

@cart_blue.route("/api/cart/buy/", methods=("POST", ))
def go_buy():
    if request.method == "POST":
        data = eval(request.get_data())
        user_id = data.get("user_id")
        shop_id = data.get("shop_id")
        if all((bool(user_id), bool(shop_id))):
            good_data = cart_all(str(user_id) + "-" + str(shop_id))
            ls = []
            if good_data:
                dao = GoodDao()
                for key, value in good_data.items():
                    ls.append({
                        "goods": dao.list(key)
                    })
                return jsonify({
                    "code": 200,
                    "msg": "ok",
                    "data": {
                        "user_id": user_id,
                        "shop": shop_id,
                        "data": ls
                    }
                })
            else:
                return jsonify({
                    "code": 380,
                    "msg": "没有相关数据"
                })
            # return show_cart()
        return jsonify({
                "code": 207,
                "msg": "没有找到相关参数"
            })
    else:
        return jsonify({
            "code": 207,
            "msg": "请求参数错误"
        })


@cart_blue.route("/api/cart/all/", methods=("POST",))
def order_view():
    if request.method == "POST":
        data = eval(request.get_data())
        if not data.get("token"):
            user_id = data.get("user_id")
            save_cart(user_id)
            datas = dao.search_all(user_id)
            if datas:
                return jsonify({
                    "code": 200,
                    "msg": "ok",
                    "data": datas
                })
            else:
                return jsonify({
                    "code": 207,
                    "msg": "当前购物车为空"
                })

        else:
            return jsonify({
                "code": 207,
                "msg": "当前用户没有登录"
            })
    else:
        return jsonify({
            "code": 207,
            "msg": "请求方法错误，不支持post请求"
        })


@cart_blue.route("/api/cart/select/", methods=("POST",))
def sel_update():
    args = eval(request.get_data())
    status = args.get("is_select")
    id = args.get("order_id")
    dao.update("cart_good_select", status, id)


@cart_blue.route("/api/cart/num/", methods=("POST",))
def num_update():
    args = eval(request.get_data())
    num = args.get("num")
    id = args.get("order_id")
    dao.update("cart_good_num", num, id)