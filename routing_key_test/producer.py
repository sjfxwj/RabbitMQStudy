#!/usr/bin/python
# -*- coding:utf-8 -*-

import pika
import sys,os

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',port=5672))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs',exchange_type='direct',durable=True)

severity = sys.argv[1] if len(sys.argv) > 2 else 'info'

message = ''.join(sys.argv[2:]) or 'info'

channel.basic_publish(exchange='direct_logs',
                      routing_key=severity,    #消息的路由秘钥.
                      body=message,
                      properties=pika.BasicProperties(delivery_mode=2))  #消息的持久化:防止RabbitMQ挂掉.

print('消息发送中...')

connection.close()