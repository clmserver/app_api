import uuid

from flask import Blueprint
from flask import request, jsonify

from libs.cache import save_token
from libs.sms import send_msg
from dao.user_dao import UserDao
from services.check_sms import check_sms

blue = Blueprint('user_api', __name__)

from datetime import datetime
from libs import cache, r

@blue.route('/check_code/',methods=('GET',))
def check_code():
    # 前端请求验证码
    phone = request.args.get('phone',None)
    if phone:
        if UserDao().check_phone(phone):
            send_msg(phone).decode()
            return jsonify({'code':200,'msg':'验证码发送成功'})
    return jsonify({'code':300,'msg':'请填写正确的手机号或者验证码'})


@blue.route('/regist/', methods=('POST',))
def user_regist():
    phone = request.form.get('phone')
    code = request.form.get('code')
    #判断输入的手机号是否已经被注册
    if not UserDao().check_phone(phone):
        return jsonify({
            "code": 300,
            "msg": "手机号已被注册"
        })
    #判断接受的数据是否为空
    if all((phone,code)):
        r_code = r.get("MT" + phone)
        if r_code is not None:
            if r_code.decode() == code:
                date = {
                    'u_username' : "KMP" + phone,
                    'u_tel' : phone,
                    'u_headpic' : "imgs/a1.jpg",
                    'u_nickname' : "Nk" + phone,
                    'u_email':'xxxxxx'
                }
                UserDao().save(**date)
                user_id = UserDao().get_id(phone)
                print(user_id)
                token = uuid.uuid4().hex
                save_token(token, user_id)
                return jsonify({
                    'code':200,
                    'msg':'注册成功',
                    'token':token
                })
    return jsonify({
                "code": 300,
                "msg": "手机号或者验证码错误"
            })
