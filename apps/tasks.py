"""
声明高并发下执行的任务
"""
import time

from  . import capp

@capp.task
def add_order(**order_info):
    print(order_info)
    time.sleep(5)
    return {'msg':'下单成功'}