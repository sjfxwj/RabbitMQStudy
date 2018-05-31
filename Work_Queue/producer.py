#!/usr/bin/python
# -*- coding:utf-8 -*-

import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='queue_4',durable=True)   #队列持久化

message = ''.join(sys.argv[1:]) or 'HHH'
channel.basic_publish(exchange='',
                      routing_key='queue_4',
                      body=message,
                      properties=pika.BasicProperties(delivery_mode=2))  #消息持久化.


print('生产者发送的消息是:%s...'%message)

connection.close()