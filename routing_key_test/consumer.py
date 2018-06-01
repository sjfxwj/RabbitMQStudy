#!/usr/bin/python
# -*- coding:utf-8 -*-

import pika
import sys,os
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',port=5672))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs',exchange_type='direct',durable=True)

result = channel.queue_declare(durable=True,exclusive=False)   #随机产生一个队列,并进行消息的持久化.
queue_name = result.method.queue

severities = sys.argv[1:]
if not severities:
    sys.stderr.write('Usage:%s [info] [warning] [error]\n'%sys.argv[0])
    sys.exit(1)


for severity in severities:
    channel.queue_bind(exchange='direct_logs',   #将队列与exchange进行绑定.
                       queue=queue_name,
                       routing_key=severity)  #队列的绑定键.

print('[*] 等待消息中...')

def callback(channel,method,properties,body):
    print('正在处理消息..')
    time.sleep(5)
    print('绑定键:',method.routing_key,'消息的内容:',body)
    channel.basic_ack(delivery_tag=method.delivery_tag)  #防止消费者死掉.

channel.basic_qos(prefetch_count=2)  #告诉老板:我一次最多干几个活.
channel.basic_consume(callback,
                      queue=queue_name,  #从队列当中获取消息。
                      no_ack=False)  #防止消费者死掉.

channel.start_consuming()

















