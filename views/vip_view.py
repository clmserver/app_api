# -*- coding: utf-8 -*- 
# @Time : 2019/6/27 13:56

from flask import Blueprint
from flask import request, jsonify

from dao.vip_dao import VipDao
from libs import cache

blue = Blueprint('vip_api', __name__)


@blue.route('/api/vip/', methods=('GET',))
def vip_view():
    # 验证用户是否已登录
    token = request.args.get('token', None)
    if token is None:
        return jsonify({
            'code': 202,
            'msg': '未登录,请登录'
        })
    if cache.check_token(token):
        user_id = cache.get_token_user_id(token)
        print(user_id)
        # 显示vip界面
        dt = VipDao()
        data = dt.get_shop()
        name = dt.get_username(user_id)
        return jsonify({
            'code': 200,
            'msg': '显示成功',
            'data': {
                "user_id": user_id,
                "shop_data":data,   # 商品信息
                "username":name,  # 用户姓名
            }
        })
