#!/usr/bin/python
# -*- coding:utf-8 -*-

import pika

"""
生产者将消息发送到'queue_1'队列。消费者接收来自该队列的消息。
"""

#有数据,就直接拿过来,没有数据,就直接夯住.
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='queue_1')  #如果队列在RabbitMQ当中已经存在,可以不用二次声明.


def callback(ch,method,properties,body):
    print('回调函数当中的三个参数是:')
    print(ch)
    print(method)
    print('[x] Received %r'%body)

channel.basic_consume(callback,
                      queue='queue_1', #指定从哪个队列里面消费数据.
                      no_ack=True)     #默认数值为False  Tell the broker to not expect a response

print('等待消息中...')
channel.start_consuming()