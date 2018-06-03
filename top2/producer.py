#!/usr/bin/python
# -*- coding:utf-8 -*-

import pika
import sys,os

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',port=5672))
channel = connection.channel()

channel.exchange_declare(exchange='top_exchange_dbs',exchange_type='topic',durable=True)  #声明一个交换机,并进行持久化.

message = ''.join(sys.argv[1:]) or 'anonymous.info'   #通过命令传入消息
print(message)


channel.basic_publish(exchange='top_exchange_dbs',
                      routing_key='debug.message.info',    #消息的路由键(给消息贴的标签)
                      body=message,
                      properties=pika.BasicProperties(delivery_mode=2))   #防止rabbitmq服务器挂掉:消息的持久化


print('开始发送消息....')  #消息一旦没有接受,则直接废掉.

connection.close()