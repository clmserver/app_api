from libs import r

def check_sms(u_phone, msg_code):
    res = None
    try:
        r_msg_code = r.get('MT' + u_phone).decode()
        print(r_msg_code,'xxxxxxxxxxxxxxxx')
        if not r_msg_code:
            res = {'code': 207, 'msg': '短信验证码已过期'}
        if r_msg_code != msg_code:
            res = {'code': 207, 'msg': '短信验证码输入错误'}
    except Exception as e:
        res = {'code': 380, 'msg': '数据库查询失败 %s' % e}

    return res


if __name__ == '__main__':
    print(check_sms('18309182914','111111'))
