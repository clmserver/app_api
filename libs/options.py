import requests
"""
-- curlat当前纬度
-- curlng当前经度

"""

def getcode(site):
    parameters = {'address': site, 'key': 'c95a5bc62fa2d66fcea48b3273e5d3ed'}

    base = 'http://restapi.amap.com/v3/geocode/geo'
    response = requests.get(base, parameters)
    info_site = response.json()
    curlat = info_site['geocodes'][0]['location'].split(',')[0]
    curlng = info_site['geocodes'][0]['location'].split(',')[1]
    print(curlat,curlng)

if __name__ == '__main__':
    address = '西安建筑科技大学'
    print(getcode(address))


