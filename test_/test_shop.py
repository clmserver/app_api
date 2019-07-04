'''
@shop_blue.route("/api/shop/", methods=["POST", ])
@shop_blue.route("/api/shop/",methods=["GET",])
@shop_blue.route("/api/shop/goods/",methods=["GET",])
@shop_blue.route("/api/shop/store/",methods=["GET",])
@shop_blue.route("/api/good/")

'''

import unittest,requests

class TestShop(unittest.TestCase):
    def test_get_shop_type(self):
        url = 'http://10.35.162.147:8002/api/shoptype/'
        data = {
            "type_id":'139'
        }
        header = {
            'Content-Type': 'application/json',
        }
        reps = requests.post(url,json=data,headers=header)
        code = reps.json().get('code')
        self.assertEqual(code,200)

    def test_get_shopinfo(self):
        url = 'http://10.35.162.147:8002/api/shop/'
        data = {
            "shop_id": '1'
        }

        reps = requests.get(url,params=data)
        code = reps.json().get('code')
        self.assertEqual(code,200)


    def test_get_shop_goodsinfo(self):
        url = 'http://10.35.162.147:8002/api/shop/goods/'
        data = {
            'shop_id':'1'
        }
        reps = requests.get(url,params=data)
        code = reps.json().get('code')
        self.assertEqual(code,200)


    def test_get_shop_storeinfo(self):
        url = 'http://10.35.162.147:8002/api/shop/store/'
        data = {
            'shop_id':1
        }
        reps = requests.get(url,params=data)
        code = reps.json().get('code')
        self.assertEqual(code, 200)

    
    def test_get_good_info(self):
        url = 'http://10.35.162.147:8002/api/good/'
        data = {
            'shop_id':1
        }
        reps = requests.get(url,params=data)
        code = reps.json().get('code')
        self.assertEqual(code, 200)




suite = unittest.TestLoader().loadTestsFromTestCase(TestShop)
unittest.TextTestRunner(verbosity=2).run(suite)