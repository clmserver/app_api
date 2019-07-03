import requests

from unittest import TestCase

def test_upload_avator():
    url = 'http://10.35.162.152:9001/upload_avator/'
    data = {
        'token':123
    }
    files = (
        ('img',open('https://m.jianbihua.com/sites/default/files/styles/photo640x425/public/images/2018-03/5_81.jpg?itok=49FkgVAV','rb'),'image/jpeg'),
    )
    resp = requests.post(url,data,files=files)
    resp_data = resp.json()
    print(resp_data)
    assert resp_data.get('code')==200
    print('ok')

if __name__ == '__main__':
    test_upload_avator()