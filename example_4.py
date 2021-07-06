"""This program demonstrates a asynchronous approach 
to accomplishing tasks. In this version there is a 
second worker created, and the workers can delegate 
back to the control loop to cooperate with each other.
In this version the tasks are asynchronous, so the
workers run concurrently.
"""
import asyncio
from codetiming import Timer


async def task(delay: float=0):
    """This is a little task that takes some time to complete

    Args:
        delay (int): The delay the task takes
    """
    with Timer(text="Task elapsed time: {:.2f} seconds"):
        await asyncio.sleep(delay)
        return delay


async def worker(name: str, task_queue: asyncio.Queue):
    """This is our worker that pulls tasks from
    the queue and performs them

    Args:
        name (str): The string name of the task
        task_queue (asyncio.Queue): The queue the tasks are pulled from
    """
    # pull tasks from the queue until the queue is empty
    print(f"Worker {name} starting to run tasks")
    while not task_queue.empty():
        fn, kwargs = await task_queue.get()
        result = await fn(**kwargs)
        print(f"Worker {name} completed task: result = {result}\n")

    print(f"Worker {name} finished as there are no more tasks\n")


async def main():
    """
    This is the main entry point for the program
    """
    # Create the queue for tasks
    task_queue = asyncio.Queue()

    # Put some tasks in the queue
    list(map(task_queue.put_nowait, [
        (task, {"delay": 4.0}), 
        (task, {"delay": 3.0}), 
        (task, {"delay": 2.0}),
        (task, {"delay": 1.0}),
    ]))

    with Timer(text="Total elapsed time: {:.2f}"):
        await asyncio.gather(
            asyncio.create_task(worker("One", task_queue)),
            asyncio.create_task(worker("Two", task_queue))
        )


if __name__ == "__main__":
    print()
    asyncio.run(main())
    print()
