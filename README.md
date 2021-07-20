# Introduction To Asynchronous Programming With Python

The slide deck for this presentation is accessible [here](docs/Intro-to-Async-Python.pdf).

This repository contains the code examples that go along with the
Google slide deck for the presentation. The examples progress one after
the other from a simple synchronous app that just runs a time delayed
task to an asynchronous one that gets web pages using two workers
to get web pages concurrently.

## Installation

It's recommended to use a Python virtual environment to install the
necessary modules and run the example programs. I use [pyenv](https://github.com/pyenv/pyenv) to make a version of Python available in the project directory. The examples were built using Python version 3.9.5.

Here's the commands using pyenv to get the examples running in Mac or Linux:

```console
$ pyenv local 3.9.5
$ python -m venv .venv
$ source .venv/bin/activate
$ (.venv) pip install --upgrade pip
$ (.venv) pip install -r requirements.txt
```

## Example Programs

- example_1.py - This program demonstrates a synchronous approach
  to accomplishing tasks. The worker can't delegate
  any tasks and completes them all one after another.
- example_2.py - This program demonstrates a synchronous approach
  to accomplishing tasks. The worker can't delegate
  any tasks and completes them all one after another.
  In this version there is a second worker created,
  but the two workers aren't cooperating with each
  other.
- example_3.py - This program demonstrates a synchronous approach
  to accomplishing tasks. In this version there is a
  second worker created, and the workers can delegate
  back to the control loop to cooperate with each other,
  but there isn't any net benefit because the tasks
  are still running synchronously.
- example_4.py - This program demonstrates a asynchronous approach
  to accomplishing tasks. In this version there is a
  second worker created, and the workers can delegate
  back to the control loop to cooperate with each other.
  In this version the tasks are asynchronous, so the
  workers run concurrently.
- example_5.py - This program demonstrates a synchronous approach
  to accomplishing tasks. In this version there is a
  second worker created, and the workers can delegate
  back to the control loop to cooperate with each other,
  but there isn't any net benefit because the tasks
  are still running synchronously. The tasks for this demo are getting the contents of webpages.
- example_6.py - This program demonstrates a asynchronous approach
  to accomplishing tasks. In this version there is a
  second worker created, and the workers can delegate
  back to the control loop to cooperate with each other.
  In this version the tasks are asynchronous, so the
  workers run concurrently. The tasks for this demo are getting the contents of webpages.
- example_7.py - This is a bonus example program demonstrating a asynchronous approach to accomplishing tasks. In this version there is a second worker created, and the workers can delegate
  back to the control loop to cooperate with each other.
  In this version the tasks are asynchronous, so the
  workers run concurrently. The tasks for this demo are getting the contents of webpages and reading files
