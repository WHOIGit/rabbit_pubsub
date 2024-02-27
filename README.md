# rabbit_pubsub
A containerized demo of RabbitMQ, an AMQP pub/sub messaging system. 

This rudamentary demo has one rabbitmq broker, two queues, and three python scripts

 - `app/do_input.py` listens for files created in `vols/input` and sends the filepath string to `newfile_queue` queue. This command is executed by the `pyinput` container.
 - `app/do_proc.py` listens to `newfile_queue`, converts the string to all-uppercase, then forwards the modified message to `output_queue`. This command is executed by the `pyproc` container. 
 - `app/do_output` listents to `output_queue` and appends the uppercase'd filename path to `vols/output/names.txt`. This command is executed by the `pyoutput` container.
 
This demo isn't flashy but it's a start!

Try it yourself by running 
```
docker-compose build
docker-compose up
```

One neat feature is that, you can individually take down the `pyproc` container, continute to add files in `vols/input`, and when you bring `pyproc` back online, the messages that were queued up by `pyinput` will be read and passed on to `pyproc` and `pyoutput` containers automagically. `rabbitmq` can be set up with a volume aswell, such that if the broker goes down too any unprocessed messages will be persisted to disk until the broker container comes back up.

