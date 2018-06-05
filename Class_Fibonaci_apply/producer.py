#!/usr/bin/python
# -*- coding:utf-8 -*-

import pika
import sys,os
import time
import uuid

class FibonaciClient(object):
    def __init__(self):
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',port=5672))
        self.channel = self.conn.channel()

        self.channel.queue_declare(queue='rpc_queue',durable=True,exclusive=False)


    def call(self,num):
        print('发送的消息为:%s'%str(num))
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   body=str(num),
                                   properties=pika.BasicProperties(
                                       delivery_mode=2,
                                       correlation_id= self.corr_id,
                                   ))

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    fibonaci = FibonaciClient()
    fibonaci.call(10)
    print('消息发送SuccessFul...')