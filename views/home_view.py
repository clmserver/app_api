from flask import Blueprint, request, jsonify, logging

from apps import tasks
from dao.main_dao import MainDao
from libs.dsq import wheels
from logger import api_logger

main_blue = Blueprint("mainblue", __name__)
dao = MainDao()


"""主页面显示"""


@main_blue.route("/api/home/", methods=["GET", "POST"])
def main_view():
    if request.method == "POST":
        r_data = eval(request.get_data())
        lat = r_data['lat']
        lon = r_data['lon']
        if all((lat,lon)):
            wheel = dao.wheel()
            main_type_img = dao.main_type()
            main_small_img = dao.main_small_img()
            foodlist = dao.youxuan_shops()
            goodfood = dao.youxuan_goods()
            shoplists = dao.shoplists()
            nearbylists = dao.shop_nearby(lat,lon)
            result = {
                "code": 200,
                "msg": "ok",
                "data": {
                    "wheel": wheel,
                    "main_type_img": main_type_img,
                    "main_small_img": main_small_img,
                    "foodlist": foodlist,
                    "goodfood": goodfood,
                    "shoplists": shoplists,
                    "nerbylists":nearbylists
                }
            }
            return jsonify(result)
        return jsonify({'code':207,'msg':'请传入正确的参数lat和lon'})
    else:
        return jsonify({
            "code": 203,
            "msg": "请求参数错误"
        })



@main_blue.route('/api/search/', methods=("POST",))
def search_view():
    try:
        search = eval(request.get_data())['keyword']
        data = dao.search(search.lower())
        if not data:
            data = "没有找到相关商品"
        return jsonify({
            "code": 200,
            "msg": "ok",
            "data": data
        })
    except Exception as e:
        api_logger.info(e)

"""获取商品全部分类"""

@main_blue.route("/api/home/all/", methods=("POST", ))
def all_type():
    if request.method == "POST":
        all = dao.all_type()
        return jsonify({
            "code": 200,
            "msg": "ok",
            "all": all
        })
    return jsonify({
        "code": 300,
        "msg": "请求参数错误"
    })
