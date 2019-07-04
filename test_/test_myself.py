import unittest,requests

class TestMyself(unittest.TestCase):
    def test_getcode(self):
        url = 'http://10.35.162.147:8002/user/check_code/'
        data = {
            'phone':18309182914,
        }
        resp = requests.get(url,params=data)
        code = resp.json().get('code')
        self.assertEqual(code,200)




suite = unittest.TestLoader().loadTestsFromTestCase(TestMyself)
unittest.TextTestRunner(verbosity=2).run(suite)