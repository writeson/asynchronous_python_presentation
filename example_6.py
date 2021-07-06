"""This program demonstrates a asynchronous approach 
to accomplishing tasks. In this version there is a 
second worker created, and the workers can delegate 
back to the control loop to cooperate with each other.
In this version the tasks are asynchronous, so the
workers run concurrently.

The tasks for this demo are getting the contents
of webpages.
"""
import asyncio
import aiohttp
from codetiming import Timer


async def task(url: str=""):
    """This is a little task that takes some time to complete

    Args:
        url (str): The url to get via http
    """
    with Timer(text="Task elapsed time: {:.2f} seconds"):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                text = await response.text()
                return url, text


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
        url, text = await fn(**kwargs)
        print(f"Worker {name} completed task: url = {url}, text = {text.strip()[:50]}\n")

    print(f"Worker {name} finished as there are no more tasks\n")


async def main():
    """
    This is the main entry point for the program
    """
    # Create the queue for tasks
    task_queue = asyncio.Queue()

    # Put some tasks in the queue
    list(map(task_queue.put_nowait, [
        (task, {"url": "https://weather.com/"}), 
        (task, {"url": "http://yahoo.com"}), 
        (task, {"url": "http://linkedin.com"}), 
        (task, {"url": "https://www.dropbox.com"}), 
        (task, {"url": "http://microsoft.com"}), 
        (task, {"url": "http://facebook.com"}),
        (task, {"url": "https://www.target.com/"}),
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
