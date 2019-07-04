from flask import Blueprint, request, jsonify, logging

from dao.main_dao import MainDao
from dao.shop_dao import ShopDao
from libs.dsq import wheels
from logger import api_logger


main_blue = Blueprint("mainblue", __name__)
dao = MainDao()


"""主页面显示"""


@main_blue.route("/api/home/", methods=["GET", "POST"])
def main_view():
    if request.method == "POST":
        # r_data = request.get_json()
        r_data = request.get_json()
        print(r_data)
        print(type(r_data))
        try:
            lat = r_data['lat']
            print(lat)
            lon = r_data['lon']
            if all((lat,lon)):
                wheel = dao.wheel()
                main_type_img = dao.main_type()
                main_small_img = dao.main_small_img()
                shops = dao.youxuan_shops()
                foodlists = []
                for shop in shops:
                    food_data = {}
                    shop_id = shop['id']
                    good_pic = dao.get_goodpic(shop_id)
                    food_data['shop_id'] = shop_id
                    food_data['shop_name'] = shop['shop_name']
                    food_data['shop_img'] = shop['img_url']
                    food_data['good_img'] = good_pic
                    food_data['app_delivery_tip'] = shop['app_delivery_tip']
                    foodlists.append(food_data)
                # goodfood = dao.youxuan_goods()
                goodfood = dao.youxuan_goods()
                for good in goodfood:
                    good['shop_name'] = dao.get_shopname(good['g_shop_id'])
                    good['shop_img'] = dao.get_shop_head_pic(good['g_shop_id'])
                shoplists = dao.shoplists()
                nearbylists = dao.shop_nearby(lat,lon)
                shop_discounts2 = []
                for shop in shops:
                    shop_id = shop['id']
                    shop_discounts2.append(ShopDao().get_discounts2(shop_id))
                result = {
                    "code": 200,
                    "msg": "ok",
                    "data": {
                        "wheel": wheel,
                        "main_type_img": main_type_img,
                        "main_small_img": main_small_img,
                        "foodlist": foodlists,
                        "goodfood": goodfood,
                        "shoplists": shoplists,
                        "nerbylists":nearbylists,
                        "shop_discounts2":shop_discounts2
                    }
                }
                api_logger.info("主页面显示成功")
                return jsonify(result)
        except Exception as e:
            api_logger.error("参数错误%s" % e)
            return jsonify({'code':207,'msg':'请传入正确的参数lat和lon'})
    else:
        api_logger.error("请求方式错误")
        return jsonify({
            "code": 203,
            "msg": "请求参数错误"
        })



# @main_blue.route('/api/search/', methods=("POST",))
# def search_view():
#     try:
#         search = eval(request.get_data())['keyword']
#         data = dao.search(search.lower())
#         if not data:
#             api_logger.error("相关商品不存在")
#             data = "没有找到相关商品"
#         api_logger.info("查询到商品")
#         return jsonify({
#             "code": 200,
#             "msg": "ok",
#             "data": data
#         })
#     except Exception as e:
#         api_logger.error("未接收到参数%s"% e)
#     return jsonify({"code":203,"msg":"未接收到参数keyword"})

"""获取商品全部分类"""

@main_blue.route("/api/home/all/", methods=("GET", ))
def all_type():
    all = dao.all_type()
    api_logger.info("获取到全部分类")
    return jsonify({
        "code": 200,
        "msg": "ok",
        "all": all
    })

