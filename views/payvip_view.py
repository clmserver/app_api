from flask import Blueprint, request
from flask.json import jsonify

from dao.user_dao import UserDao
from libs import cache
from logger import api_logger

blue = Blueprint('bank_api', __name__)



# 充值会员和余额扣费
@blue.route('/api/card_num/', methods=('GET',))
# 用户的银行卡
def card_num():
    token = request.args.get('token', None)
    #接收user_id

    #判断接受的数据是否为空
    if token:
        user_id = cache.get_token_user_id(token)
        data = UserDao().get_wallet(user_id)
        if not data:
            api_logger.info("此用户无银行卡")
            return jsonify({
                "code":300,
                "msg":"你还未添加银行卡，请添加银行卡"
            })
        api_logger.info("显示所有银行卡")
        return jsonify({
                    "code": 200,
                    "msg": "银行卡号",
                    "data": data,
                })
    else:
        api_logger.info("user_id为空")
        return jsonify({"msg":'查无此用户',
                        "code":300})

@blue.route('/api/burse_balance/',methods=("GET",))
# 用户余额
def burse_balance():
    token = request.args.get('token', None)
    print(token)
    if token:
        user_id = cache.get_token_user_id(token)
        print(user_id)
        vip_fee = request.args.get('vip_fee')
        burse_balance = UserDao().get_burse(user_id)[0]['u_burse_balance']
        print(burse_balance)
        if burse_balance:
            if int(vip_fee) > int(burse_balance):
                api_logger.warning("余额不足")
                return jsonify({
                    "code":301,
                    'msg':'您的余额不足!'
                })
            else:
                burse_balance = int(burse_balance) - int(vip_fee)
                UserDao().burse_change(user_id,burse_balance)
                api_logger.info("充值成功")
                return jsonify({
                    'code':200,
                    'msg':'恭喜您，您已成功充值会员!'
                })
        else:
            api_logger.warning("余额为0")
            return jsonify("您还没有余额，请充值")
    else:
        api_logger.info("user_id为空")
        return jsonify('查无此用户')

