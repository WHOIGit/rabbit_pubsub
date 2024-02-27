
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from amqp_utils import publish_to_rabbitmq_channel


class Watcher:
    DIRECTORY_TO_WATCH = "/input"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=False)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except Exception as e:
            self.observer.stop()
            print(type(e),e)

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_created(event):
        if os.path.basename(event.src_path).startswith('.'): 
            return
        if event.is_directory:
            return 

        print('EVENT_TYPE:',event.event_type)


        print(f"Received created event - {event.src_path}")
        rabbitmq_host = os.getenv('RABBITMQ_HOST', 'rabbitmq')
        rabbitmq_queue = "newfile_queue"
        publish_to_rabbitmq_channel(rabbitmq_host, rabbitmq_queue, message=event.src_path)



if __name__ == '__main__':
    w = Watcher()
    w.run()
    
    
