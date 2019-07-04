import unittest, requests


class TestHome(unittest.TestCase):
    def test_getwheel(self):
        url = 'http://10.35.162.147:8002/api/home/'
        data = {
            "lat": "34",
            "lon": "108"
        }
        headers = {
            'Content-Type': 'application/json',
        }
        resp = requests.post(url, json=data, headers=headers)
        # print(resp.json())
        code = resp.json().get('code')
        self.assertEqual(code, 200)

    def test_homeall(self):
        url = 'http://10.35.162.147:8002/api/home/all/'
        resp = requests.get(url)
        code = resp.json().get('code')
        self.assertEqual(code, 200)


suite = unittest.TestLoader().loadTestsFromTestCase(TestHome)
unittest.TextTestRunner(verbosity=2).run(suite)