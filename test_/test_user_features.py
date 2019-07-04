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