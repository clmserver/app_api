from flask import Blueprint, request, jsonify

from dao.main_dao import MainDao

main_blue = Blueprint("mainblue", __name__)
dao = MainDao()


"""主页面显示"""


@main_blue.route("/api/home/", methods=["GET", "POST"])
def main_view():
    if request.method == "POST":
        wheel = dao.wheel()
        main_type_img = dao.main_type()
        main_small_img = dao.main_small_img()
        result = {
            "code": 200,
            "msg": "ok",
            "data": {
                "wheel": wheel,
                "main_type_img": main_type_img,
                "main_small_img": main_small_img
            }
        }
        return jsonify(result)
    else:
        return {
            "code": 203,
            "msg": "请求参数错误"
        }


@main_blue.route('/api/search/', methods=("POST",))
def search_view():
    search = request.form.get("keyword")
    data = dao.search(search)
    if not data:
        data = "没有找到相关商品"
    return jsonify({
        "code": 200,
        "msg": "ok",
        "data": data
    })