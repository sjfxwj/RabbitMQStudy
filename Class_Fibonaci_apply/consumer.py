#!/usr/bin/python
# -*- coding:utf-8 -*-

import pika
import os,sys
import time
import uuid



class FibonaciServer(object):
    def __init__(self):
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',port=5672))
        self.channel = self.conn.channel()

        self.channel.queue_declare(queue='rpc_queue', durable=True, exclusive=False)


    def fib(self,n):  # 定义一个主逻辑:斐波那契数列.
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return self.fib(n - 1) + self.fib(n - 2)


    def call_back(self,channel,method,properties,body):
        print('接收的消息为:%s'%str(body))
        value = self.fib(int(body))
        print('数值:',body,'对应的斐波那契数值是:',value)
        time.sleep(5)
        self.channel.basic_ack(delivery_tag=method.delivery_tag)


    def on_response(self):
        self.uuid = str(uuid.uuid4())
        self.channel.basic_qos(prefetch_count=2)
        self.channel.basic_consume(consumer_callback=self.call_back,
                                   queue='rpc_queue',
                                   no_ack=False,
                                   consumer_tag=self.uuid)

    def start_consume(self):
        self.channel.start_consuming()


if __name__ == '__main__':
    fibonaci = FibonaciServer()
    print('正在消费消息....')
    fibonaci.on_response()
    fibonaci.start_consume()

