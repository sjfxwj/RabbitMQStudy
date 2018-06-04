#!/usr/bin/python
# -*- coding:utf-8 -*-

import pika
import os,sys
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',port=5672))
channel = connection.channel()

channel.queue_declare(queue='rpc_queue',durable=True,exclusive=False)  #声明一个队列,持久化+唯一


def fib(n):  #定义一个主逻辑:斐波那契数列.===>程序的处理逻辑在这里写.
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)


def on_request(channel,method,properties,body): #整个RPC服务器的核心
    n = int(body)
    time.sleep(3)
    print('################################################')
    print('n is %s,对应的斐波那契数值信息是:%s'%(str(n),fib(int(n))))
    print('\033[42m接收到的消息附带的属性信息:\033[0m')
    print(properties)

    #TODO 接受消息的同时将消息进行返回.
    channel.basic_publish(exchange='',
                          routing_key=properties.reply_to,
                          body=str(fib(int(n))),
                          properties=pika.BasicProperties(
                              correlation_id=properties.correlation_id,  #从客户端收到的correlation_id
                              reply_to=properties.reply_to,  #服务器端执行完命令之后,将结果返回到这个queue里面.
                          ))
    channel.basic_ack(delivery_tag=method.delivery_tag)  #防止消费者挂掉.


#开始消费消息
channel.basic_qos(prefetch_count=2)  #每次最多只能干2个活.
channel.basic_consume(consumer_callback=on_request,
                      queue='rpc_queue',
                      no_ack=False)   #防止消费者挂掉


print('[x] Awaiting RPC requests.')
channel.start_consuming()










