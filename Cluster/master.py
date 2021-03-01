#!/usr/bin/env python3
from xmlrpc.server import SimpleXMLRPCServer

from multiprocessing import Process

from redis import Redis
from rq import Queue

import logging
import os

import requests

WORKERS = list()
redisQueue = None

def start_worker(id):
    logging.info("Starting worker with id (%s)", id)

def add_worker():
    global WORKERS
    proc = Process(target=start_worker, args=(len(WORKERS),))
    proc.start()
    WORKERS.append(proc)

def remove_worker(id):
    global WORKERS
    WORKERS[id].terminate()
    WORKERS.remove(WORKERS[id])

def worker_list():
    global WORKERS
    return WORKERS

def submit_task(task):
    global redisQueue
    redisQueue.enqueue(task)

def subit_group_tasks(tasks):


def CountingWords(url):
    resp = requests.get(url)
    return len(resp.text.split())

def main():
    global redisQueue

    logging.basicConfig(level=logging.INFO)
    server = SimpleXMLRPCServer(
        ("localhost", 9000),
        logRequests=True,
    )

    server.register_function(add_worker)
    server.register_function(remove_worker)
    server.register_function(worker_list)
    server.register_function(submit_task)
    server.register_function(subit_group_tasks)

    redisQueue = Queue(connection=Redis())

    try:
        print("Control-C to exit")
        server.serve_forever()
    except KeyboardInterrupt:
        print("Exiting")

if __name__ == '__main__':
    main()
