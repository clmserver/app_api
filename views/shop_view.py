from flask import Blueprint, request, jsonify

from dao.shop_dao import ShopDao

shop_blue = Blueprint("shop_blue", __name__)
dao = ShopDao()


@shop_blue.route("/api/shop/", methods=["POST", ])
def get_shop_type():
    if request.method == "POST":
        type = request.get_json()
        type_id = type.get("type_id")
        if type_id:
            data = dao.all_shop(type_id)
            return jsonify({
                "code": 200,
                "msg": "ok",
                "data": data
            })
    return jsonify({
        "code": 300,
        "msg": "请求参数错误",
    })

