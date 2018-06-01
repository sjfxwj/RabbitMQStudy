#!/usr/bin/python
# -*- coding:utf-8 -*-

import pika
import os,sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',port=5672))
channel = connection.channel()

channel.exchange_declare(exchange='cold_data_exchange',exchange_type='fanout',durable=True)

message = ''.join(sys.argv[1:]) or 'Hello World!'

channel.basic_publish(exchange='cold_data_exchange',
                      routing_key='',  #因为类型为fanout,所以routing_key没有什么实际意义.
                      body=message,
                      properties=pika.BasicProperties(delivery_mode=2))    #为了防止RabbitMq宕机,我们将消息进行持久化.

print('消息发送...')

connection.close()






























