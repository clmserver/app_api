from flask import Blueprint, request, jsonify

from dao.shop_dao import ShopDao

shop_blue = Blueprint("shop_blue", __name__)
dao = ShopDao()

# 点击小分类
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

# 点击店铺
@shop_blue.route("/api/shop/",methods=["GET",])
def get_shopinfo():
    shop_id = request.args.get('shop_id')
    shop_data = dao.get_shop(shop_id)
    print(shop_data)
    shop_discounts2 = dao.get_discounts2(shop_id)
    shop_poi_env = dao.get_poi_env(shop_id)
    shop_poi_service = dao.get_poi_service(shop_id)
    return jsonify({
        'code':200,
        'msg':'店铺信息查询成功',
        'data':{
            'data': shop_data,
            'discounts':shop_discounts2,
            'poi_env':shop_poi_env,
            'poi_service':shop_poi_service
        }

    })

# 进入店铺点击点菜
@shop_blue.route("/api/shop/goods/",methods=["GET",])
def get_shop_goodsinfo():
    shop_id = request.args.get('shop_id')
    shop_goods_data = dao.get_shop_goods(shop_id)
    return jsonify({
        'code':200,
        'msg':'店铺信息查询成功',
        'data':{
            'data': shop_goods_data,
        }

    })

# 进入店铺点击商家
@shop_blue.route("/api/shop/store/",methods=["GET",])
def get_shop_storeinfo():
    shop_id = request.args.get('shop_id')
    shop_address = dao.get_shop(shop_id)['shop_address']
    shop_time = dao.get_shop(shop_id)['shop_time']
    shop_discounts2 = dao.get_discounts2(shop_id)
    shop_poi_env = dao.get_poi_env(shop_id)
    shop_poi_service = dao.get_poi_service(shop_id)
    return jsonify({
        'code':200,
        'msg':'店铺信息查询成功',
        'data':{
            'data': {'shop_address':shop_address,'shop_time':shop_time},
            'discounts':shop_discounts2,
            'poi_env':shop_poi_env,
            'poi_service':shop_poi_service
        }
    })

# 点击食品
@shop_blue.route("/api/good/")
def get_good_info():
    good_id = request.args.get('good_id')
    data = dao.get_good(good_id)
    return jsonify({
        'code':200,
        'msg':'数据查询成功',
        'data':data
    })