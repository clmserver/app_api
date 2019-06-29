import uuid

from flask import Blueprint, json, redirect, url_for
from flask import request, jsonify

from libs.cache import save_token
from libs.crypt import make_password, check_password
from libs.sms import send_msg
from dao.user_dao import UserDao
from services.check_sms import check_sms
from services.create_password import GetPassword

blue = Blueprint('user_api', __name__)

# 请求验证码
@blue.route('/check_code/',methods=['GET'])
def check_code():
    phone = request.args.get('phone')       #获取手机号
    if phone:
        res = eval(send_msg(phone).decode())    #发送验证码
        if res['Code'] == 'OK':
            return jsonify({'code':200,'msg':'验证码发送成功'})
        else:
            return jsonify({'code':207,'msg':'手机号错误请填写正确的手机号'})
    return jsonify({'code':207,'msg':'请填写正确的手机号'})


# 验证码登录
@blue.route('/code_login/', methods=['POST'])
def user_regist():
    phone = request.form.get('phone')
    code = request.form.get('code')
    #判断接受的数据是否为空
    print(phone)
    if all((phone,code)):
        res = check_sms(phone,code)
        if not res:
            data = {
                'u_username' : "KMP" + phone,
                'u_tel' : phone,
                'u_headpic' : "imgs/a1.jpg",
                'u_nickname' : "Nk" + phone,
                'u_email':'xxxxxx',
                'is_vip':False,
                'is_active':True,
            }
            UserDao().save(**data)
            user_id = UserDao().get_id('u_tel',phone)
            print(user_id)
            token = uuid.uuid4().hex
            save_token(token, user_id)
            return jsonify({
                'code':200,
                'msg':'登录成功，欢迎使用MT外卖品台',
                'token':token,
                'data':""
            })
    return jsonify({
                "code": 300,
                "msg": "手机号或者验证码错误"
            })


# 密码登录
@blue.route('/pwd_login/',methods=['POST'])
def code_login():
    phone = request.form.get('phone')
    pwd = request.form.get('pwd')
    #判断接受的数据是否为空
    if all((phone, pwd)):
        u_password = UserDao().get_pwd('u_tel',phone)
        if check_password(pwd,u_password):
            user_id = UserDao().get_id('u_tel',phone)
            print(user_id)
            if user_id is not None:
                token = uuid.uuid4().hex
                save_token(token, user_id)
                return jsonify({
                    'code': 200,
                    'msg': '登录成功，欢迎使用MT外卖品台',
                    'token': token,
                    'data': "用户信息数据"
                })
    return jsonify({
        "code": 300,
        "msg": "手机号或者密码错误,请重新输入"
    })


# 忘记密码
@blue.route('/forget_password/',methods=['POST'])
def forget_password():
    phone = request.form.get('phone')       #获取手机号
    print(phone)
    if phone:
        if not UserDao().check_phone(phone):
            res = eval(send_msg(phone).decode())    #发送验证码
            if res['Code'] == 'OK':
                return jsonify({'code':200,'msg':'验证码发送成功'})
            else:
                return jsonify({'code':207,'msg':'手机号错误请填写正确的手机号'})
        else:
            return jsonify({'code':207,'msg':'该手机号还没有注册，请前去注册'})
    return jsonify({'code':207,'msg':'请填写正确的手机号'})


# 忘记密码之后初始化生成密码并返回
@blue.route('/find_password/',methods=['POST'])
def find_password():
    phone = request.form.get('phone')
    code = request.form.get('code')
    print(phone,code)
    # 判断接受的数据是否为空
    if all((phone, code)):
        res = check_sms(phone, code)
        print(res)
        if not res:
            # 随机生成密码保存到数据库
            pwd = GetPassword(10)
            u_password = make_password(pwd)

            if UserDao().set_userinfo('u_password',u_password,'u_tel',phone):
                return jsonify({'code':200,'msg':'验证成功，初始化密码为：'+pwd})

        else:
            return jsonify({'code':207,'msg':'验证码输入错误、请重新输入!'})
    else:
        return jsonify({'code':207,'msg':'请输入正确的参数'})

# 上传头像


#  修改用户名
@blue.route('/change_username/', methods=('POST',))
def change_user():
    user_id = request.form.get('user_id')
    user_name = request.form.get('user_name')
    if UserDao().check_username('user_name'):
        if UserDao().set_userinfo('u_username', user_name, 'id', user_id):
            return jsonify({'code': 200, 'msag': '用户名修改成功', 'u_username': user_name})
        return jsonify({'code': 207, 'msg': '用户名修改失败'})
    return jsonify({'code': 207, 'msg': '用户名已存在'})


# 修改用户密码
@blue.route('/change_password/', methods=('POST',))
def change_password():
    user_id = request.form.get('user_id')
    u_password = request.form.get('u_password')
    u_password = make_password(u_password)
    if UserDao().set_userinfo('u_password', u_password, 'id', user_id):
        return jsonify({'code': 200, 'msg': '用户密码修改成功'})
    return jsonify({'code': 207, 'msg': '用户名已存在'})

# 更改手机号
@blue.route('/change_tel/',methods=['POST'])
def change_tel():
    user_id = request.form.get('user_id')
    phone = request.form.get('phone')
    if len(phone)== 11:
        if UserDao().check_phone(phone):
            if UserDao().set_userinfo('u_tel',phone,'id',user_id):
                return jsonify({'code':200,'msg':'手机号修改成功','u_tel':phone})
    return jsonify({'code':207,'msg':'手机号认证失败，请重新输入！'})

# 注销账户
@blue.route('/kill_id/',methods=['POST'])
def kill_id():
    user_id = request.form.get('user_id')
    if UserDao().del_userinfo(user_id):
        return jsonify({'code':200,'msg':'账户注销成功'})

# 退出当前用户
@blue.route('/logout/',methods=['POST'])
def logout():
    user_id = request.form.get('user_id')
    if UserDao().set_userinfo('is_active',False,'id',user_id):
        return jsonify({'code':200,'msg':'当前用户已经退出登录'})