#!/usr/bin/python
# -*- coding:utf-8 -*-

import pika
import os,sys
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',port=5672))
channel = connection.channel()

channel.exchange_declare(exchange='top_exchange_dbs',exchange_type='topic',durable=True)  #声明一个交换机,并进行持久化.
queue_name = channel.queue_declare(queue='top_dbs_queue',durable=True,exclusive=False)  #防止服务器挂掉:同时保留queue

binding_keys = ['debug.*.info']
for binding_key in binding_keys:
    channel.queue_bind(queue='top_dbs_queue',exchange='top_exchange_dbs',routing_key=binding_key)  #将队列与exchange交换机进行绑定.


def call_back(channel,method,properties,body):
    print('正在接受消息...')
    print('绑定键:',method.routing_key,'消息:',body)
    time.sleep(5)
    channel.basic_ack(delivery_tag=method.delivery_tag)  #防止消费者挂掉.


channel.basic_qos(prefetch_count=2)   #告诉老大,我每次最多接2个活.
channel.basic_consume(consumer_callback=call_back,
                      queue='top_dbs_queue',
                      no_ack=False)                      #防止消费者挂掉.

print('等待接受消息...')

channel.start_consuming()