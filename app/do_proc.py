import os

from amqp_utils import publish, subscribe #listen_to_rabbitmq_channel, publish_to_rabbitmq_channel


def callback33(body):
    msg = body
    print(f"Received message: {msg}")

    #do a transform
    msg = msg.upper()
    
    rabbitmq_host = os.getenv('RABBITMQ_HOST', 'rabbitmq')
    rabbitmq_queue = "output_queue"
    publish(message=msg, host=rabbitmq_host, user='guest', password='guest', exchange_name='egg', exchange_type='direct', routing_key=rabbitmq_queue)
    #publish_to_rabbitmq_channel(rabbitmq_host, rabbitmq_queue, message=msg)



if __name__ == '__main__':
    rabbitmq_host = os.getenv('RABBITMQ_HOST', 'rabbitmq')
    from_channel = 'newfile_queue' 
    subscribe(callback33, host=rabbitmq_host, user='guest', password='guest', exchange_name='egg', exchange_type='direct', routing_key=from_channel, queue_name='')
    #listen_to_rabbitmq_channel(rabbitmq_host, from_channel, callback)

