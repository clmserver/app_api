import datetime

from dao.main_dao import MainDao


def youxuan_shops():
    dao = MainDao()
    time = datetime.datetime.now()
    hour = time.hour
    # if hour in range(5,10):  #早餐
    #     return dao.youxuan_shops(where='id',args='178')
    # elif hour in range(10,18):  #正餐
    #     return dao.youxuan_shops(where='id', args='')
    # elif hour in range(18,22):  #晚餐
    #
    # elif hour in range(22,5):   #夜宵

if __name__ == '__main__':
    youxuan_shops()