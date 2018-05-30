#!/usr/bin/python
# -*- coding:utf-8 -*-

import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='queue_2')

def callback(ch,method,properties,body):
    print('[x] 消费者接受到的消息是:%r'%body)
    time.sleep(len(body))
    print('[x] 处理消息完毕.')
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(consumer_callback=callback,
                      queue='queue_2',
                      no_ack=False)

print('消费者开始等待消息..')

channel.start_consuming()
