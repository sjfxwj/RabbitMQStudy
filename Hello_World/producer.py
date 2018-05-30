#!/usr/bin/python
# -*- coding:utf-8 -*-

import pika


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost')) #与RabbitMQ服务器建立连接
channel = connection.channel()  #创建一个频道

channel.queue_declare(queue='queue_1')  #创建一个传递消息的队列

channel.basic_publish(exchange='',          #通过修改exchange可以改变Rabbitmq的执行模式
                      routing_key='queue_1',#指定向哪个队列里面发送数据
                      body='Hello World!')  #向队列当中发送数据的内容

print('[x] 发送 "Hello World!"')

connection.close()  #关闭连接

"""
在退出程序之前，我们需要确保网络缓冲区被刷新，并且我们的消息被实际传送到RabbitMQ。
可以通过轻轻关闭连接来完成。
"""
