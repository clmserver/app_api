from redis import Redis

r = Redis(host='localhost',
           port=6371, db=3)
r2 = Redis(host='localhost',
           port=6371, db=1)
# r = Redis(host='localhost',
#            port=6379, db=3)
# r2 = Redis(host='localhost',
#            port=6379, db=1)



if __name__ == '__main__':
    print(r.keys("*"))
    r.flushall()

