"""This program demonstrates a asynchronous approach 
to accomplishing tasks. In this version there is a 
second worker created, and the workers can delegate 
back to the control loop to cooperate with each other.
In this version the tasks are asynchronous, so the
workers run concurrently.
"""
import asyncio
from codetiming import Timer


async def factorial(number: int):
    async def inner_factorial(number):
        if number <= 1:
            return 1
        if number % 10 == 0:
            print("Context switch to event loop")
            await asyncio.sleep(0)
        return number * await inner_factorial(number - 1)
    return await inner_factorial(number)        


async def io_task(delay: float=0):
    """This is a little task that takes some time to complete

    Args:
        delay (int): The delay the task takes
    """
    with Timer(text="IO Task elapsed time: {:.2f} seconds"):
        await asyncio.sleep(delay)
        return delay


async def cpu_task(number: int):
    """This is a cpu bound task that takes some time to complete

    Args:
        number (int): The number to get calculate a factorial for
    """
    with Timer(text="CPU Task elapsed time: {:.2f} seconds"):
        result = await factorial(number)
        return result


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
        print(f"Worker {name} completed task: {result=}\n")

    print(f"Worker {name} finished as there are no more tasks\n")


async def main():
    """
    This is the main entry point for the program
    """
    # Create the queue for tasks
    task_queue = asyncio.Queue()

    # Put some tasks in the queue
    list(map(task_queue.put_nowait, [
        (io_task, {"delay": 4.0}),
        (cpu_task, {"number": 40}),
        (io_task, {"delay": 3.0}), 
        (io_task, {"delay": 2.0}),
        (cpu_task, {"number": 50}),
        (io_task, {"delay": 1.0}),
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
