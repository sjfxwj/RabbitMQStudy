#!/usr/bin/python
# -*- coding:utf-8 -*-

import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',port=5672))
channel = connection.channel()

channel.exchange_declare(exchange='dbs_exchange',exchange_type='direct',durable=True)  #exchange持久化

message = ''.join(sys.argv[1:]) or 'DBS Hello ME'
channel.basic_publish(exchange='dbs_exchange',
                      routing_key='DBchange',
                      body=message,
                      properties=pika.BasicProperties(delivery_mode=2))  #消息持久化

print('send the message。。')

connection.close()

