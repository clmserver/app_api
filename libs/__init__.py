from redis import Redis

r = Redis(host='localhost',
           port=6379, db=3)
r2 = Redis(host='localhost',
           port=6379, db=1)
