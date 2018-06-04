#!/usr/bin/python
# -*- coding:utf-8 -*-

import pika
import os,sys
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',port=5672))
channel = connection.channel()

channel.queue_declare(queue='rpc_queue',durable=True,exclusive=False)  #声明一个队列,持久化+唯一

def fib(n):  #定义一个主逻辑:斐波那契数列.
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

def call_back(channel,method,properties,body):
    n = int(body)
    time.sleep(3)
    print('n is %s'%str(n))
    print('\033[42m接收到的消息附带的属性信息:\033[0m')
    print('delivery_mode is %s'%properties.delivery_mode)
    print('correlation_id is %s'%properties.correlation_id)
    channel.basic_ack(delivery_tag = method.delivery_tag)   #防止消费者挂掉.


#开始消费消息
channel.basic_qos(prefetch_count=2)  #每次最多只能干2个活.
channel.basic_consume(consumer_callback=call_back,
                      queue='rpc_queue',
                      no_ack=False)   #防止消费者挂掉


print('[x] Awaiting RPC requests.')
channel.start_consuming()










