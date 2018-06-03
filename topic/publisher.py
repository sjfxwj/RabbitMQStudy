#!/usr/bin/python
# -*- coding:utf-8 -*-

import pika
import sys,os


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs',exchange_type='topic',durable=True)

routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'

message = ''.join(sys.argv[2:]) or 'Hello World!'

channel.basic_publish(exchange='topic_logs',
                      routing_key=routing_key,  #给消息打上一个标签.anonymous.info
                      body=message,
                      properties=pika.BasicProperties(delivery_mode=2))   #防止服务器挂掉:消息持久化.

print('开始发送消息...路由关键字:%s,消息为:%s'%(routing_key,message))

connection.close()