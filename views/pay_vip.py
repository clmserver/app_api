from flask import Blueprint, request
from flask.json import jsonify

from dao.user_dao import UserDao

blue = Blueprint('bank_api', __name__)


# 充值会员和余额扣费
@blue.route('/card_num/', methods=('GET',))
def card_num():
    user_id = request.form.get('user_id')
    vip_fee = request.form.get('vip_fee')
    #接收user_id和会员费

    #判断接受的数据是否为空
    if user_id:
        data = UserDao().get_wallet(user_id)
        return jsonify({
                    "code": 300,
                    "msg": "银行卡号",
                    "data": data,
                })
    else:
        return ('user_id为空')


@blue.route('/burse_balance/',methods=("GET",))
def burse_balance():
    user_id = request.form.get('user_id')
    vip_fee = request.form.get('vip_fee')
    burse_balance = UserDao().get_burse(user_id)[0]['u_burse_balance']
    print(burse_balance)
    if burse_balance:
        if int(vip_fee) > int(burse_balance):
            return jsonify({
                "code":301,
                'msg':'您的余额不足!'
            })
        else:
            burse_balance = int(burse_balance) - int(vip_fee)
            UserDao().burse_change(user_id,burse_balance)
            return jsonify({
                'code':300,
                'msg':'恭喜您，您已成功充值会员!'
            })
    else:
        return ("您的余额不足")

