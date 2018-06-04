#!/usr/bin/python
# -*- coding:utf-8 -*-

import pika
import os,sys
import time
import uuid


class FibonaciRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',port=5672))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue='rpc_queue',durable=True,exclusive=False)  #队列的持久化

    def send_msg(self,n):
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   body=str(n),
                                   properties=pika.BasicProperties(
                                       delivery_mode=2,
                                       correlation_id=str(uuid.uuid4())
                                   ))  #将消息进行持久化:防止RabbitMq服务挂掉

    def close(self):
        self.connection.close()


if __name__ == '__main__':
    fibonacci_rpc = FibonaciRpcClient()
    print('[x] 发送消息 call(30)...')
    fibonacci_rpc.send_msg(30)





