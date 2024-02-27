import os

from amqp_utils import listen_to_rabbitmq_channel


def callback(ch, method, properties, body):
    msg = body.decode()
    print(f"Received message: {msg}")

    with open('/output/names.txt', 'a') as f:
        f.write(msg)
        f.write('\n')
    


if __name__ == '__main__':
    rabbitmq_host = os.getenv('RABBITMQ_HOST', 'rabbitmq')
    from_channel = 'output_queue' 
    listen_to_rabbitmq_channel(rabbitmq_host, from_channel, callback)
    
