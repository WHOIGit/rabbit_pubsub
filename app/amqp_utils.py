import json
import pika


class Client:
    def __init__(self, host, user, password, exchange_name, exchange_type='direct'):
        self.host = host
        self.user = user
        self.exchange_name = exchange_name
        assert exchange_type in list(pika.exchange_type.ExchangeType), f'"Invalid exchange type: "{exchange_type}" not in {list(pika.exchange_type.ExchangeType)}'
        self.exchange_type = exchange_type

        credentials = pika.PlainCredentials(self.user, password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.host, credentials=credentials))

        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange_name,
                                      exchange_type=self.exchange_type,
                                      durable=False,)

    def publish(self, message, routing_key=''):
        self.channel.basic_publish(exchange=self.exchange_name,
                                   routing_key=routing_key,
                                   body=json.dumps(message))

    def subscribe(self, callback, routing_key='', queue=''):
        def on_message(ch, method, properties, body):
            callback(json.loads(body.decode()))
        result = self.channel.queue_declare(queue=queue, exclusive=True)
        queue_name = result.method.queue
        self.channel.queue_bind(exchange=self.exchange_name,
                                queue=queue_name,
                                routing_key=routing_key)
        self.channel.basic_consume(queue=queue_name,
                                  on_message_callback=on_message,
                                  auto_ack=True)
        self.channel.start_consuming()

    def close(self):
        self.connection.close()


def publish(message, host, user, password, exchange_name, exchange_type='fanout', routing_key=''):
    client = Client(host, user, password, exchange_name, exchange_type)
    client.publish(message, routing_key)
    client.close()
    

def subscribe(callback, host, user, password, exchange_name, exchange_type='fanout', routing_key='', queue_name=''):
    client = Client(host, user, password, exchange_name, exchange_type)
    client.subscribe(callback, routing_key, queue_name)  # blocking
    client.close()
    

