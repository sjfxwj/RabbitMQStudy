#!/usr/bin/python
# -*- coding:utf-8 -*-

import pika
import sys,os
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='cold_data_exchange',exchange_type='fanout',durable=True)  #exchange也可以进行持久化.
# result = channel.queue_declare(exclusive=False)       #一旦消费者连接关闭，队列被删除:exclusive=True
# queue_name = result.method.queue   #随机生成一个队列.    #隐患2
# channel.queue_bind(queue=queue_name,exchange='cold_data_exchange')   #将队列与exchange进行绑定.
channel.queue_declare(queue='cold_data_queue',durable=True)  #为了防止RabbitMq服务宕机,我们将队列进行持久化.
channel.queue_bind(queue='cold_data_queue',exchange='cold_data_exchange')

def call_back(channel,method,properties,body):
    print('正在处理消息中....')
    print(body)
    time.sleep(8)
    print('消息处理完毕...')
    channel.basic_ack(delivery_tag=method.delivery_tag)   #消费者进行消息确认。

channel.basic_qos(prefetch_count=2)   #告诉你们:我每次最多只能接两个活,并且活必须是我的.
channel.basic_consume(call_back,
                      queue='cold_data_queue',
                      no_ack=False)   #防止消费者死亡.

print('消费者开始消费数据...')

channel.start_consuming()