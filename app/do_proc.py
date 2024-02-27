import os

from amqp_utils import listen_to_rabbitmq_channel, publish_to_rabbitmq_channel


def callback(ch, method, properties, body):
    msg = body.decode()
    print(f"Received message: {msg}")

    #do a transform
    msg = msg.upper()
    
    rabbitmq_host = os.getenv('RABBITMQ_HOST', 'rabbitmq')
    rabbitmq_queue = "output_queue"
    publish_to_rabbitmq_channel(rabbitmq_host, rabbitmq_queue, message=msg)



if __name__ == '__main__':
    rabbitmq_host = os.getenv('RABBITMQ_HOST', 'rabbitmq')
    from_channel = 'newfile_queue' 
    listen_to_rabbitmq_channel(rabbitmq_host, from_channel, callback)

