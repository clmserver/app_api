from redis import Redis

r = Redis(host='localhost',
           port=6371, db=3)

if __name__ == '__main__':
    print(r.keys("*"))
    r.flushall()