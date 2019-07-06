import unittest,requests

class TestUserFeatures(unittest.TestCase):
    def test_user_address(self):
        url = 'http://10.35.162.147:8002/user/address/'
        data = {
            "token":'bea0216f14f2493f848b41b5afc2613d'
        }

        reps = requests.get(url,params=data)
        code = reps.json().get('code')
        self.assertEqual(code,200)


    def test_user_add(self):
        url = 'http://10.35.162.147:8002/user/add_address/'
        data = {
            "token": 'bea0216f14f2493f848b41b5afc2613d'
        }
        headers = {
            'Content-Type': 'application/json',
        }

        reps = requests.post(url, heandes=headers ,jsion=data)
        code = reps.json().get('code')
        self.assertEqual(code, 200)



    #
    def test_user_upaddress(self):
        url = 'http://10.35.162.147:8002/user/address/up_address/'
        data = {
            "token": 'bea0216f14f2493f848b41b5afc2613d'
        }

        reps = requests.get(url ,params=data)
        code = reps.json().get('code')
        self.assertEqual(code, 200)



    def test_user_add(self):
        url = 'http://10.35.162.147:8002/user/add_address/'
        data = {
            "token": 'bea0216f14f2493f848b41b5afc2613d'
        }
        headers = {
            'Content-Type': 'application/json',
        }

        reps = requests.post(url, heandes=headers ,jsion=data)
        code = reps.json().get('code')
        self.assertEqual(code, 200)



    def test_user_add(self):
        url = 'http://10.35.162.147:8002/user/add_address/'
        data = {
            "token": 'bea0216f14f2493f848b41b5afc2613d'
        }
        headers = {
            'Content-Type': 'application/json',
        }

        reps = requests.post(url, heandes=headers ,jsion=data)
        code = reps.json().get('code')
        self.assertEqual(code, 200)


suite = unittest.TestLoader().loadTestsFromTestCase(TestUserFeatures)
unittest.TextTestRunner(verbosity=2).run(suite)