#!/usr/bin/python
# -*- coding:utf-8 -*-

import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#-channel.queue_declare(queue='queue1')
channel.exchange_declare(exchange='logs',exchange_type='fanout')   #声明一个交换机,类型为广播.

message = ''.join(sys.argv[1:]) or 'info:Hello World!'
channel.basic_publish(exchange='logs',
                      routing_key='',  #我们提供一个routing_key的数值，但是由于交换机的类型为fanout,作用可忽略.
                      body = message)

print('发送的消息为:%s'%message)
connection.close()





