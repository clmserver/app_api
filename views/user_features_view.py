# -*- coding: utf-8 -*- 
# @Time : 2019/7/2 10:08

from flask import Blueprint
from flask import request, jsonify

from libs.cache import check_token, get_token_user_id
from dao.user_features_dao import User_Featuare_Dao
from logger import api_logger

blue = Blueprint('user_feature', __name__)


# 进去我的地址，新增地址
@blue.route('/user/address/add/',methods= ['GET'])
def user_add():
    token = request.args.get('token', None)
    r_data = request.get_json()
    phone = r_data['phone']
    address = r_data['address']
    linkman = r_data['linkman']
    num = r_data['num']
    user_id = get_token_user_id(token)
    # user_id = r_data['user_id']
    data = {
        'address':address,# 地址
        'addr_housenum':num,   # 门牌号
        'addr_linkman':linkman,  # 联系人
        'addr_tel' : phone,   # 手机
        'user_id':user_id,

    }
    User_Featuare_Dao().saves(**data)
    return jsonify({
        'code':200,
        'msg':'地址添加成功',
        'data':data
    })


# 我的地址
@blue.route('/user/address/',methods=['GET'])
def user_address():

    # 验证登录
    token = request.args.get('token', None)
    if token is None:
        return jsonify({
            'code': 202,
            'msg': '未登录,请登录'
        })
    if check_token(token):
        user_id = get_token_user_id(token)
        # user_id = request.get_json()['user_id']   # 获取user_id
        data = User_Featuare_Dao().se_address(user_id)
        return jsonify({
            'code':200,
            'msg':'显示地址',
            'data':data,
        })
    return jsonify({'code':1111})


# 修改地址
@blue.route('/user/address/up_address/',methods=['GET'])
def user_upaddress():
    token = request.args.get('token', None)
    r_data = request.get_json()
    phone = r_data['phone']
    address = r_data['address']
    linkman = r_data['linkman']
    num = r_data['num']
    user_id = get_token_user_id(token)
    # user_id = r_data['user_id']     # 传递user_id
    id = r_data['id']     # 传递id
    data = {
        'address':address,
        'addr_housenum':num,
        'addr_linkman':linkman,
        'addr_tel':phone,
    }
    User_Featuare_Dao().up_address(address,num,linkman,phone,user_id,id)
    return jsonify({
        'code': 200,
        'user_id':user_id,
        'msg': '更改成功',
        'data': data
    })


# 删除我的地址
@blue.route('/user/address/del/',methods=['GET'])
def del_address():
    token = request.args.get('token', None)
    r_data = request.get_json()
    sid = r_data['id']
    user_id = get_token_user_id(token)
    # user_id = r_data['user_id']
    User_Featuare_Dao().del_address(sid,user_id)

    return jsonify({
        "code":200,
        "msg":"删除成功！"
    })

# 用户评论
@blue.route('/user/comment/',methods=['GET'])
def user_comment():
    token = request.args.get('token', None)
    if token is None:
        return jsonify({
            'code': 202,
            'msg': '未登录,请登录'
        })
    if check_token(token):
        user_id = get_token_user_id(token)
        data = User_Featuare_Dao().user_comment(user_id)
        return jsonify({
            "code":200,
            "data":data,
            "msg":"查询成功"
        })

@blue.route('/shop/pl/',methods=['GET'])
def shop_pl():
    v_shop_id = request.args.get('v_shop_id')
    data = User_Featuare_Dao().shop_pl(v_shop_id)
    api_logger
    return jsonify({
        'code':200,
        'data':data,
    })