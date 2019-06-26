from libs import r
import uuid

def new_token():
    return uuid.uuid4().hex


def save_token(token, user_id):
    # 保存token
    r.set(token, user_id)
    r.expire(token, 12*3600)  # 有效时间： 12小时

def check_token(token):
    # 验证token
    return r.exists(token)


def get_token_user_id(token):
    # 通过token获取user_id
    if check_token(token):
        return r.get(token).decode()

