import threading
import time

class SharedQueue:
    def __init__(self):
        self.queue = []
        self.write_semaphore = threading.Semaphore(1)
        self.read_semaphore = threading.Semaphore(0)
        self.mutex = threading.Lock()

    # Method to add messages to the queue
    def write(self, message):
        with self.write_semaphore:
            with self.mutex:
                self.queue.append(message)
            self.read_semaphore.release()

    # Method for consumes to consume messages from the queue
    def read(self):
        self.read_semaphore.acquire()
        with self.mutex:
            message = self.queue.pop(0)
        return message

 # 5 messages per second
def writer_thread(shared_queue):
    messages = ["Message 1", "Message 2", "Message 3", "Message 4", "Message 5"]
    while True:
        for message in messages:
            shared_queue.write(message)
            time.sleep(1)  # Add a message every second

# Function for consumes to consume messages from the queue
def consume_thread(thread_id, shared_queue):
    while True:
        message = shared_queue.read()
        print(f"consume {thread_id} received: {message}")

# Main function to start the threads
if __name__ == '__main__':
    shared_queue = SharedQueue()

    writer = threading.Thread(target=writer_thread, args=(shared_queue,))
    consumes = [threading.Thread(target=consume_thread, args=(i, shared_queue)) for i in range(5)]

    writer.start()
    for consume in consumes:
        consume.start()

    # Wait for all consume threads to finish
    writer.join()
    for consume in consumes:
        consume.join()