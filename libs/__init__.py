from redis import Redis

r = Redis(host='121.199.63.71',
           port=6371, db=3)

if __name__ == '__main__':
    print(r.keys("*"))
    r.flushall()