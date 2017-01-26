from flask import Flask
from flask_sockets import Sockets
import time
# import redis
# import pickle
import os
import thread
# from util import verify_socket_session

'''
CACHE_REDIS = {'host': '127.0.0.1', 'port': 6379, 'max_connections': 100}
cache_redis_pool = redis.ConnectionPool(**CACHE_REDIS)
cache_redis = redis.Redis(cache_redis_pool)
'''

app = Flask(__name__)
sockets = Sockets(app)

@sockets.route('/echo')
# @verify_socket_session
def echo_socket(ws):
    while not ws.closed:
        try:
            message = ws.receive()
        except Exception, e:
            print e

        ws.send(message, binary=True)
    print "client disconnect!"
