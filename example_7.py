"""This program demonstrates a asynchronous approach 
to accomplishing tasks. In this version there is a 
second worker created, and the workers can delegate 
back to the control loop to cooperate with each other.
In this version the tasks are asynchronous, so the
workers run concurrently.

The tasks for this demo are getting the contents
of webpages and reading files
"""
import asyncio
import aiohttp
import aiofiles
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


async def io_task_get_web_pages(url: str=""):
    """This is a little task that takes some time to complete

    Args:
        url (str): The url to get via http
    """
    with Timer(text="Task elapsed time: {:.2f} seconds"):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                text = await response.text()
                return url, text


async def io_task_read_file(filename: str=""):
    """This is a little task that takes some time to complete

    Args:
        filename (str): The file to read
    """
    with Timer(text="Task elapsed time: {:.2f} seconds"):
        async with aiofiles.open(filename, "r") as fh:
            line_counter = 0
            async for line in fh:
                line_counter += 1
            return filename, line_counter


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
        if fn.__name__ == "io_task_get_web_pages":
            url, text = await fn(**kwargs)
            print(f"Worker {name} completed task: url = {url}, text = {text.strip()[:50]}\n")
        elif fn.__name__ == "io_task_read_file":
            filename, line_counter = await fn(**kwargs)
            print(f"Worker {name} completed task: filename = {filename}, line_counter = {line_counter}")
        elif fn.__name__ == "cpu_task":
            factorial = await fn(**kwargs)
            print(f"Worker {name} completed task: {factorial=}")

    print(f"Worker {name} finished as there are no more tasks\n")


async def main():
    """
    This is the main entry point for the program
    """
    # Create the queue for tasks
    task_queue = asyncio.Queue()

    # Put some tasks in the queue
    list(map(task_queue.put_nowait, [
        (io_task_get_web_pages, {"url": "https://weather.com/"}), 
        (io_task_read_file, {"filename": "textfile1.txt"}),
        (cpu_task, {"number": 40}),
        (io_task_get_web_pages, {"url": "http://yahoo.com"}), 
        (io_task_get_web_pages, {"url": "http://linkedin.com"}), 
        (io_task_get_web_pages, {"url": "https://www.dropbox.com"}), 
        (io_task_get_web_pages, {"url": "http://microsoft.com"}), 
        (cpu_task, {"number": 50}),
        (io_task_get_web_pages, {"url": "http://facebook.com"}),
        (io_task_read_file, {"filename": "textfile2.txt"}),
        (io_task_get_web_pages, {"url": "https://www.target.com/"}),
    ]))

    with Timer(text="Total elapsed time: {:.2f}"):
        await asyncio.gather(
            asyncio.create_task(worker("One", task_queue)),
            asyncio.create_task(worker("Two", task_queue)),
        )


if __name__ == "__main__":
    print()
    asyncio.run(main())
    print()
