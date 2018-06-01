#!/usr/bin/python
# -*- coding:utf-8 -*-

import pika
import sys
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',port=5672))
channel = connection.channel()

channel.exchange_declare(exchange='dbs_exchange',exchange_type='direct',durable=True)
channel.queue_declare(queue='dbs_queue',durable=True,exclusive=False)

routing_key_list = ['DBchange','DDL']
for routing_key in routing_key_list:
    channel.queue_bind(queue='dbs_queue',exchange='dbs_exchange',routing_key=routing_key)


def call_back(channel,method,properties,body):
    print('开始接受消息..')
    print('绑定键:',method.routing_key,'接收到的消息:',body)
    time.sleep(5)
    print('消息处理完毕..')
    channel.basic_ack(delivery_tag=method.delivery_tag)  #防止消费者挂掉.

channel.basic_qos(prefetch_count=2)  #告诉老大我每次最多只能干2个活.
channel.basic_consume(call_back,
                      queue='dbs_queue',
                      no_ack=False)   #防止消费者挂掉.

print('开始接受消息...')

channel.start_consuming()

