#!/usr/bin/python
# -*- coding:utf-8 -*-

import pika
import sys,os
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',port=5672))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs',exchange_type='topic',durable=True)

result = channel.queue_declare(exclusive=False,durable=True)   #防止服务器挂掉:队列持久化.exclusive=False(不然一旦停止就停止了.)
queue_name = result.method.queue #随机生成一个队列.

binding_keys = sys.argv[1:]  #队列的绑定值

if not binding_keys:
    sys.stderr.write('Usage: %s [bingding_key]...\n'%sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:   #将队列与消息通过绑定键进行绑定
    channel.queue_bind(exchange='topic_logs',queue=queue_name,routing_key=binding_key)

def call_back(channel,method,properties,body):
    print('开始消费消息。。。')
    print('绑定值:%s 消息:%s'%(method.routing_key,body))
    time.sleep(5)
    channel.basic_ack(delivery_tag=method.delivery_tag)    #防止消费者挂掉

channel.basic_qos(prefetch_count=2)   #告诉老大,我每次最多只能干2个活,并且这个活必须是我的.
channel.basic_consume(call_back,
                      queue=queue_name,
                      no_ack=False)  #防止消费者挂掉.

print('等待消息的到来...')
channel.start_consuming()