from celery import Celery
from flask import Flask


app = Flask(__name__)


# 配置celery的消息中间件和结构存储位置
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/2'
app.config['CELERY_RESULT_BROKER'] = 'redis://localhost:6379/2'

# 创建celery的客户端对象
capp = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
capp.conf.update(app.config)
capp.autodiscover_tasks(('apps',))
# 创建异步执行的任务
# @capp.task
# def add_order(**order_info):
#     pass



# 实现任务


