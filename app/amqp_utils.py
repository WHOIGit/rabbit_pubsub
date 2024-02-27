import pika

def callback(ch, method, properties, body):
    print(f"Received message: {body.decode()}")


def listen_to_rabbitmq_channel(host, queue_name, callback=callback):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name)

    print(f"Listening to the '{queue_name}' queue. Press Ctrl+C to exit.")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Listening stopped.")
        
        
def publish_to_rabbitmq_channel(host, queue_name, message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name)

    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=message)

    print(f"Message sent to '{queue_name}': {message}")

    connection.close()
