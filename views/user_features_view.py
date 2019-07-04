# -*- coding: utf-8 -*- 
# @Time : 2019/7/2 10:08

from flask import Blueprint
from flask import request, jsonify

from libs.cache import check_token, get_token_user_id
from dao.user_features_dao import User_Featuare_Dao
from logger import api_logger

blue = Blueprint('user_feature', __name__)


# 进去我的地址，新增地址
@blue.route('/user/add_address/',methods= ['POST'])
def user_add():
    token = request.args.get('token', None)
    user_id = get_token_user_id(token)
    if user_id:
        r_data = request.get_json()
        print(r_data)
        phone = r_data['phone']
        address = r_data['address']
        linkman = r_data['name']
        num = r_data['bottom']
        sex = r_data['sex']
        tag = r_data['tag']

        # user_id = r_data['user_id
        data = {
            'address':address,# 地址
            'addr_housenum':num,   # 门牌号
            'addr_linkman':linkman,  # 联系人
            'addr_tel' : phone,   # 手机
            'user_id':user_id,

        }
        User_Featuare_Dao().saves(**data)
        api_logger.info("地址成功添加")
        return jsonify({
            'code':200,
            'msg':'地址添加成功',
            'data':data
        })
    return jsonify({'code':207,'msg':'你还未登录请登录'})


# 我的地址
@blue.route('/user/address/',methods=['GET'])
def user_address():

    # 验证登录
    token = request.args.get('token', None)
    if token is None:
        api_logger.warning("未登录")
        return jsonify({
            'code': 202,
            'msg': '未登录,请登录'
        })
    if check_token(token):
        user_id = get_token_user_id(token)
        # user_id = request.get_json()['user_id']   # 获取user_id
        data = User_Featuare_Dao().se_address(user_id)
        api_logger.info("显示所有地址")
        return jsonify({
            'code':200,
            'msg':'显示地址',
            'data':data,
        })
    api_logger.warning("未查找到token")
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
    gender = r_data['gender']
    user_id = get_token_user_id(token)
    # user_id = r_data['user_id']     # 传递user_id
    id = r_data['id']     # 传递id
    data = {
        'address':address,
        'addr_housenum':num,
        'addr_linkman':linkman,
        'addr_tel':phone,
        "gender":gender
    }
    User_Featuare_Dao().up_address(address,num,linkman,phone,user_id,id)
    api_logger.info("更改地址成功")
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
    api_logger.info("地址删除成功")
    return jsonify({
        "code":200,
        "msg":"删除成功！"
    })

# 用户评论
@blue.route('/user/comment/',methods=['GET'])
def user_comment():
    token = request.args.get('token', None)
    if token is None:
        api_logger.warning("未登录")
        return jsonify({
            'code': 202,
            'msg': '未登录,请登录'
        })
    if check_token(token):
        user_id = get_token_user_id(token)
        data = User_Featuare_Dao().user_comment(user_id)
        api_logger.info("评论显示成功")
        return jsonify({
            "code":200,
            "data":data,
            "msg":"查询成功"
        })

@blue.route('/shop/pl/',methods=['GET'])
def shop_pl():
    v_shop_id = request.args.get('v_shop_id')
    data = User_Featuare_Dao().shop_pl(v_shop_id)
    api_logger.info("显示所有评论")
    return jsonify({
        'code':200,
        'data':data,
    })

@blue.route('/user/burrse/',methods=['GET'])
def user_hurse():
    token = request.args.get('token',None)
    if token is None:
        return jsonify({
            'code': 207,
            'msg': '用户未登录'
        })
    if check_token(token):
        user_id = get_token_user_id(token)
        balance = User_Featuare_Dao().user_balance(user_id)
        card_num = User_Featuare_Dao().user_cards(user_id)
        return jsonify({
            "code":200,
            "data":{
                "burse_balance":balance,
                "card_num":card_num
            },
            "msg":"我的钱包显示成功"
        })
    else:
        return jsonify({
            "code":303,
            "msg":"token验证失败"
        })