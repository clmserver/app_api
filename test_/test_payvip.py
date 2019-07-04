import unittest,requests

class TestPayvip(unittest.TestCase):
    # 没卡
    def test_card_num(self):
        url = 'http://10.35.162.147:8002/api/card_num/'
        data = {
            'token':'398a77e896f8498f8cade1323c5d2ad9'
        }
        resp = requests.get(url,params=data)
        code = resp.json().get('code')
        self.assertEqual(code,200)

    # 无用户
    def test_card_num1(self):
        url = 'http://10.35.162.147:8002/api/card_num/'
        data = {
            'token':'9f67af4761a245d0b7fd1c6d91a593da'
        }
        resp = requests.get(url,params=data)
        code = resp.json().get('code')
        self.assertEqual(code,200)

    # 有卡
    def test_card_num2(self):
        url = 'http://10.35.162.147:8002/api/card_num/'
        data = {
            'token':'bea0216f14f2493f848b41b5afc2613d'
        }
        resp = requests.get(url,params=data)
        code = resp.json().get('code')
        self.assertEqual(code,200)


    def test_burse_balance(self):
        url = 'http://10.35.162.147:8002/api/burse_balance/'
        data = {
            "token":'bea0216f14f2493f848b41b5afc2613d',
            "vip_fee":'200'
        }
        resp = requests.get(url,params=data)
        code = resp.json().get('code')
        self.assertEqual(code,200)




suite = unittest.TestLoader().loadTestsFromTestCase(TestPayvip)

unittest.TextTestRunner(verbosity=2).run(suite)