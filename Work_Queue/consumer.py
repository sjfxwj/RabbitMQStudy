#!/usr/bin/python
# -*- coding:utf-8 -*-

import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='queue_4',durable=True)  #队列持久化.

def callback(ch,method,properties,body):
    print('[x] 消费者接受到的消息是:%r'%body)
    time.sleep(len(body))
    print('[x] 处理消息完毕.')
    ch.basic_ack(delivery_tag=method.delivery_tag)   #防止消费者挂掉

channel.basic_qos(prefetch_count=1)   #不要向工作人员发送新的消息，直到它处理并确认了前一个消息.
channel.basic_consume(consumer_callback=callback,
                      queue='queue_4',
                      no_ack=False)    #防止消费者挂掉.

print('消费者开始等待消息..')

channel.start_consuming()
