#!/usr/bin/python
# -*- coding:utf-8 -*-

import pika
import sys,os

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs',exchange_type='fanout')  #如果已经存在,可以不用再次声明.
result = channel.queue_declare(exclusive=True)   #一旦消费者连接关闭，队列被删除:exclusive=True
queue_name = result.method.queue  #生成一个随机队列.
channel.queue_bind(queue=queue_name,exchange='logs')  #交换机和队列之间进行绑定.

def call_back(channel,method,properties,body):
    print(body)

channel.basic_consume(call_back,
                      queue=queue_name,
                      no_ack=True)

print('消费者开始消费消息')

channel.start_consuming()