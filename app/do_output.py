import os

from amqp_utils import subscribe #listen_to_rabbitmq_channel


def callback22(body):
    msg = body
    print(f"Received message: {msg}")

    with open('/output/names.txt', 'a') as f:
        f.write(msg)
        f.write('\n')
    


if __name__ == '__main__':
    rabbitmq_host = os.getenv('RABBITMQ_HOST', 'rabbitmq')
    from_channel = 'output_queue' 
    
    subscribe(callback22, host=rabbitmq_host, user='guest', password='guest', exchange_name='egg', exchange_type='direct', routing_key=from_channel, queue_name='')
    #listen_to_rabbitmq_channel(rabbitmq_host, from_channel, callback)
    
