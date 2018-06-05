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

        #TODO 定义回调队列:用于接收RPC返回结果.
        result = self.channel.queue_declare(durable=True,exclusive=False)
        self.call_queue = result.method.queue

        #TODO 从RPC队列当中接受消息
        self.channel.basic_consume(consumer_callback=self.on_response,
                                   queue=self.call_queue,
                                   no_ack=False)

    def on_response(self,channel,method,properties,body):
        if self.corr_id == str(properties.correlation_id):
            self.response = str(body)
            time.sleep(10)
        print('=====================>接收到的消息为:%s'%body)
        self.channel.basic_ack(delivery_tag=method.delivery_tag)


    def call(self,num):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        print('发送的消息为:%s'%str(num))
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   body=str(num),
                                   properties=pika.BasicProperties(
                                       delivery_mode=2,
                                       correlation_id= self.corr_id,
                                       reply_to = self.call_queue,
                                   ))
        #TODO 消息处理机制
        while self.response is None:
            self.conn.process_data_events()  #相当于self.channel.start_consuming()

        return self.response


    def close(self):
        self.conn.close()


if __name__ == "__main__":
    fibonaci = FibonaciClient()
    value = fibonaci.call(10)
    print('value is %s'%value)
    print('消息发送SuccessFul...')