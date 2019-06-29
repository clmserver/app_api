import uuid

from flask import Blueprint
from flask import request, jsonify

from libs.cache import save_token, check_token, get_token_user_id
from libs.crypt import make_password, check_password
from libs.sms import send_msg
from dao.user_dao import UserDao
from services.check_sms import check_sms
from services.create_password import GetPassword

blue = Blueprint('user_api', __name__)

# 请求验证码
@blue.route('/user/check_code/',methods=['GET'])
def check_code():
    r_data = request.get_json()
    phone = r_data['phone']       #获取手机号
    if phone:
        res = eval(send_msg(phone))    #发送验证码
        print(type(res))
        if res['Code'] == 'OK':
            return jsonify({'code':200,'msg':'验证码发送成功'})
        else:
            return jsonify({'code':207,'msg':'手机号错误请填写正确的手机号'})
    return jsonify({'code':207,'msg':'请填写正确的手机号'})


# 验证码登录
@blue.route('/user/code_login/', methods=['POST'])
def user_regist():
    r_data = request.get_json()
    phone = r_data['phone']
    code = r_data['code']
    #判断接受的数据是否为空
    print(phone)
    if all((phone,code)):
        res = check_sms(phone,code)
        if not res:
            data = {
                'u_username' : "KMP" + phone,
                'u_tel' : phone,
                'u_headpic' : "https://m.jianbihua.com/sites/default/files/styles/photo640x425/public/images/2018-03/5_81.jpg?itok=49FkgVAV",
                'u_nickname' : "Nk" + phone,
                'u_email':phone+"@tel.com",
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
                'data':data
            })
    return jsonify({
                "code": 207,
                "msg": "手机号或者验证码错误"
            })


# 密码登录
@blue.route('/user/pwd_login/',methods=['POST'])
def code_login():
    r_data = request.get_json()
    phone = r_data['phone']
    pwd = r_data['pwd']
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
@blue.route('/user/forget_password/',methods=['POST'])
def forget_password():
    r_data = request.get_json()
    phone = r_data['phone']       #获取手机号
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
@blue.route('/user/find_password/',methods=['POST'])
def find_password():
    r_data = request.get_json()
    phone = r_data['phone']
    code = r_data['code']
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
@blue.route('/user/change_username/', methods=('POST',))
def change_user():
    r_data = request.get_json()
    user_id = r_data['user_id']
    user_name = r_data['user_name']
    if UserDao().check_username('user_name'):
        if UserDao().set_userinfo('u_username', user_name, 'id', user_id):
            return jsonify({'code': 200, 'msg': '用户名修改成功', 'u_username': user_name})
        return jsonify({'code': 207, 'msg': '用户名修改失败'})
    return jsonify({'code': 207, 'msg': '用户名已存在'})


# 修改用户密码
@blue.route('/user/change_password/', methods=('POST',))
def change_password():
    r_data = request.get_json()
    user_id = r_data['user_id']
    u_password = r_data['U_password']
    u_password = make_password(u_password)
    if UserDao().set_userinfo('u_password', u_password, 'id', user_id):
        return jsonify({'code': 200, 'msg': '用户密码修改成功'})
    return jsonify({'code': 207, 'msg': '用户名已存在'})

# 更改手机号
@blue.route('/user/change_tel/',methods=['POST'])
def change_tel():
    r_data = request.get_json()
    user_id = r_data['user_id']
    phone = r_data['phone']
    if len(phone)== 11:
        if UserDao().check_phone(phone):
            if UserDao().set_userinfo('u_tel',phone,'id',user_id):
                return jsonify({'code':200,'msg':'手机号修改成功','u_tel':phone})
    return jsonify({'code':207,'msg':'手机号认证失败，请重新输入！'})

# 注销账户
@blue.route('/user/kill_id/',methods=['POST'])
def kill_id():
    r_data = request.get_json()
    user_id = r_data['user_id']
    if UserDao().del_userinfo(user_id):
        return jsonify({'code':200,'msg':'账户注销成功'})

# 退出当前用户
@blue.route('/user/logout/',methods=['POST'])
def logout():
    r_data = request.get_json()
    user_id = r_data['user_id']
    if UserDao().set_userinfo('is_active',False,'id',user_id):
        return jsonify({'code':200,'msg':'当前用户已经退出登录'})

# 切换到我的模块
@blue.route('/user/',methods=['GET'])
def user():
    r_data = request.get_json()
    if r_data:
        token = r_data['token']
        if check_token(token):
            user_id = get_token_user_id(token)
            print(user_id)
            s_data = UserDao().get_profile(user_id)
            return jsonify({'code':200,'msg':'OK','data':s_data})
    return jsonify({'code':207,'msg':'未登录，请前去登录'})