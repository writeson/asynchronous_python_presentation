"""This program demonstrates a synchronous approach 
to accomplishing tasks. In this version there is a 
second worker created, and the workers can delegate 
back to the control loop to cooperate with each other,
but there isn't any net benefit because the tasks
are still running synchronously. 

The tasks for this demo are getting the contents
of webpages.
"""
import requests
from queue import Queue
from codetiming import Timer


def task(url: str=""):
    """This is a little task that takes some time to complete

    Args:
        url (str): The url to get via http
    """
    with Timer(text="Task elapsed time: {:.2f} seconds"):
        with requests.Session() as session:
            response = session.get(url)
            return url, response.text


def worker(name: str, task_queue: Queue):
    """This is our worker that pulls tasks from
    the queue and performs them

    Args:
        name (str): The string name of the task
        task_queue (Queue): The queue the tasks are pulled from
    """
    # pull tasks from the queue until the queue is empty
    print(f"Worker {name} starting to run tasks")
    while not task_queue.empty():
        fn, kwargs = task_queue.get()
        yield
        url, text = fn(**kwargs)
        print(f"Worker {name} completed task: url = {url}, text = {text.strip()[:50]}\n")

    print(f"Worker {name} finished as there are no more tasks\n")


def main():
    """
    This is the main entry point for the program
    """
    # Create the queue for tasks
    task_queue = Queue()

    list(map(task_queue.put_nowait, [
        (task, {"url": "https://weather.com/"}), 
        (task, {"url": "http://yahoo.com"}), 
        (task, {"url": "http://linkedin.com"}), 
        (task, {"url": "https://www.dropbox.com"}), 
        (task, {"url": "http://microsoft.com"}), 
        (task, {"url": "http://facebook.com"}),
        (task, {"url": "https://www.target.com/"}),
    ]))

    # Create two workers
    workers = [
        worker("One", task_queue),
        worker("Two", task_queue)
    ]

    # Run the workers
    with Timer(text="Task elapsed time: {:.2f} seconds"):
        while len(workers):
            for worker_ in workers:
                try:
                    next(worker_)
                except StopIteration:
                    workers.remove(worker_)


if __name__ == "__main__":
    print()
    main()
    print()
