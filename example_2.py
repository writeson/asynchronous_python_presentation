"""This program demonstrates a synchronous approach 
to accomplishing tasks. The worker can't delegate
any tasks and completes them all one after another.
In this version there is a second worker created,
but the two workers aren't cooperating with each
other.
"""
from time import sleep
from queue import Queue
from codetiming import Timer


def factorial(number: int):
    def inner_factorial(number):
        if number <= 1:
            return 1
        return number * inner_factorial(number - 1)
    return inner_factorial(number)        


def io_task(delay: float=0):
    """This is a little task that takes some time to complete

    Args:
        delay (int): The delay the task takes
    """
    with Timer(text="IO Task elapsed time: {:.2f} seconds"):
        sleep(delay)
        return delay


def cpu_task(number: int):
    """This is a cpu bound task that takes some time to complete

    Args:
        number (int): The number to get calculate a factorial for
    """
    with Timer(text="CPU Task elapsed time: {:.2f} seconds"):
        return factorial(number)


def worker(name: str, task_queue: Queue):
    """This is our worker that pulls tasks from
    the queue and performs them

    Args:
        name (str): The string name of the task
        work_queue (Queue): The queue the tasks are pulled from
    """
    # pull tasks from the queue until the queue is empty
    print(f"Worker {name} starting to run tasks")
    while not task_queue.empty():
        fn, kwargs = task_queue.get()
        result = fn(**kwargs)
        print(f"Worker {name} completed task: result = {result}\n")

    print(f"Worker {name} finished as there are no more tasks\n")


def main():
    """
    This is the main entry point for the program
    """
    # Create the queue for tasks
    task_queue = Queue()

    # Put some tasks in the queue
    list(map(task_queue.put, [
        (io_task, {"delay": 4.0}),
        (cpu_task, {"number": 40}),
        (io_task, {"delay": 3.0}), 
        (io_task, {"delay": 2.0}),
        (cpu_task, {"number": 50}),
        (io_task, {"delay": 1.0}),
    ]))

    # Create two workers
    workers = [
        (worker, "One", task_queue),
        (worker, "Two", task_queue)
    ]

    # Run the workers
    with Timer(text="Total elapsed time: {:.2f}"):
        while workers:
            for worker_ in workers:
                worker_fn, name, queue = worker_
                worker_fn(name, queue)
                workers.remove(worker_)


if __name__ == "__main__":
    print()
    main()
    print()
