#!/usr/bin/python
# -*- coding:utf-8 -*-

import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='queue_2')

message = ''.join(sys.argv[1:]) or 'Hello World!'
channel.basic_publish(exchange='',
                      routing_key='queue_2',
                      body=message)

print('生产者发送的消息是:%s...'%message)

connection.close()