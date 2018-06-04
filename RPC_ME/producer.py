#!/usr/bin/python
# -*- coding:utf-8 -*-

import pika
import os,sys
import time
import uuid


class FibonaciRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',port=5672))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue='rpc_queue', durable=True, exclusive=False)  # 声明一个队列,持久化+唯一
        #声明一个回调队列,名字随意取.
        result = self.channel.queue_declare(durable=True,exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(consumer_callback=self.on_response,
                                   queue=self.callback_queue,
                                   no_ack=False) #确认消息被接受.

    def on_response(self,channel,method,properties,body):   #等待服务端返回结果.
        """
        :param channel: 
        :param method: 
        :param properties: correlation_id===>接受到的消息就是我们想要的.
        :param body: 
        :return: 
        """
        print('--------------------------------------')
        print('\033[42m接收到的消息附带的属性信息:\033[0m')
        print(properties)
        print('---------------------------------------')
        if self.corr_id == properties.correlation_id:  #将这句话话废掉不行吗???==>貌似也可以.==>但这样是精确的.
            self.response = body
        #self.response = body
        channel.basic_ack(delivery_tag=method.delivery_tag)  # 防止消费者挂掉.

    def call(self,n):         #执行实际的RPC请求操作.
        self.response = None  #返回结果.
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   body=str(n),
                                   properties=pika.BasicProperties(
                                       delivery_mode=2,
                                       correlation_id= self.corr_id,
                                       reply_to=self.callback_queue,   #约定好的返回结果的队列.
                                   ))  #发布的消息带有的三个属性信息.

        while self.response is None:
            time.sleep(1)
            # 相当于非阻塞式的consuming===> self.channel.consuming()====>这里也可以发送消息.
            self.connection.process_data_events()

        return int(self.response)



if __name__ == '__main__':
    fibonacci_rpc = FibonaciRpcClient()
    print('[x] 发送消息 call(30)...')   #发送完消息之后我们等待消息的结果.
    result = fibonacci_rpc.call(30)
    print('返回的结果是:%s'%str(result))