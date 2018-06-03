#!/usr/bin/python
# -*- coding:utf-8 -*-

import pika
import sys,os
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='rpc_queue')   #声明一个队列

def fib(n):  #定义一个主逻辑:斐波那契数列.
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

def on_request(channel,method,properties,body):  #这个东西实际上就是我们以前的回调函数.
    """
    basic_consume的回调函数,是整个RPC服务器的核心.
    在收到请求时执行,在完成工作候将响应发回。
    """
    n = int(body)  #客户端传过来的数值.
    print('[.] fib(%s)'%n)
    response = fib(n)  #计算完数值.

    channel.basic_publish(exchange='',
                          routing_key=properties.reply_to,  #路由标签,在原路径发送回去.
                          body=str(response),
                          properties=pika.BasicProperties(
                              correlation_id = properties.correlation_id)  #拿过来什么标签,就在给发回去.
                          )

    channel.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1) #告诉老大,我每次最多消费一个(为了在多台服务器上平均分配负载,我们设置相应的数值.)
channel.basic_consume(consumer_callback=on_request,
                      queue='rpc_queue',
                      no_ack=False)   #消息确认.


print('[x] Awaiting RPC requests')
channel.start_consuming() #消费者开始进行消费。