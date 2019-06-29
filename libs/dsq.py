import threading

from dao.main_dao import MainDao

wheels = None
"""定时器"""
def sayhello():
    global t, wheels        #Notice: use global variable!
    wheels = MainDao().wheel()
    t = threading.Timer(6000, sayhello)
    #t.start()


t = threading.Timer(6000, sayhello)
#t.start()
