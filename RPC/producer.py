#!/usr/bin/python
# -*- coding:utf-8 -*-

import pika
import os,sys
import uuid
import time

class FibonaciRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',port=5672))
        self.channel = self.connection.channel()

        #为回复声明一个唯一的回调队列.
        result = self.channel.queue_declare(exclusive=True)  #队列的持久化,防止服务器挂掉
        self.callback_queue = result.method.queue  #创建一个回调队列,命名随机

        #订阅回调队列,以便我们接受RPC相应
        self.channel.basic_consume(consumer_callback=self.on_response,
                                   queue=self.callback_queue,
                                   no_ack=True)   #确认消息接受

    def on_response(self,channel,method,properties,body):  #等待服务端返回的结果.
        if  self.corr_id == properties.correlation_id:
            self.response = body  #对于每个响应消息检查correlation_id是否是我们正在寻找的

    def call(self,n):          #希望远程服务器执行的操作.(这个方法将执行实际的RPC请求.)
        self.response = None   #初始化返回值
        self.corr_id = str(uuid.uuid4())  #f9d87831-6e1d-4a2f-b8fd-7e99b348a564
        self.channel.basic_publish(exchange='',  #默认的exchange交换机. AMQP default
                                   routing_key='rpc_queue', #消息的路由键
                                   body=str(n),
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id,
                                   ))  #发布的消息具有两个属性: reply_to和correlation_id。

        while self.response is None:
            time.sleep(5)
            print('\033[42m....\033[0m')
            self.connection.process_data_events()  #等待正确的相应结果.

        return int(self.response)


fibonacci_rpc = FibonaciRpcClient()   #貌似是消费者的角色

print('[x] Requeusting fib(30)...')
response = fibonacci_rpc.call(30)     #向服务端请求数据
print('等待结果...%s'%(response))


"""
待思考的问题:
如果没有服务器在运行，客户应该如何应对？
客户端是否应该对RPC有某种超时？
如果服务器发生故障并引发异常，是否应将其转发给客户端？
在处理之前防止无效的传入消息（例如检查边界）
"""

