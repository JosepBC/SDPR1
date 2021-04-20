#!/usr/bin/env python3

from xmlrpc.server import SimpleXMLRPCServer
import redis

import urllib.request

import dill

from multiprocessing import Process

import logging

class Cluster:
    __instance = None
    def __new__(cls, *args):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args)
        return cls.__instance

    def __init__(self):
        self.redisCon = redis.Redis(host="localhost")
        self.workers = {}
        self.server = SimpleXMLRPCServer(
            ("localhost", 9000),
            logRequests=True,
        )

        logging.basicConfig(level=logging.INFO)
        self.server.register_function(self.addWorker)
        self.server.register_function(self.removeWorker)
        self.server.register_function(self.listWorkers)
        self.server.register_function(self.submitTask)
        self.server.register_function(self.submitTaskGroup)

        try:
            print("Control-C to exit")
            self.server.serve_forever()
        except KeyboardInterrupt:
            print("Stopping all workers")
            for elem in self.workers.values():
                elem.stop()
            print("Exiting")


    #Manage workers
    def addWorker(self, workerID = None):
        if workerID is None:
            workerID = len(self.workers)
        worker = Worker(workerID, self.redisCon)
        self.workers[workerID] = worker
        worker.start()
        return True

    def removeWorker(self, workerID):
        try:
            self.workers.pop(workerID).stop()
        except KeyError:
            print("Trying to remove an unexisting worker, id = ", workerID)
        return True

    def listWorkers(self):
        return list(self.workers.keys())
    
    #Tasks
    def submitTask(self, jobid, task, url):
        data = {
            'jobid': jobid, 
            'task': task.data,
            'url': url
        }

        self.redisCon.rpush("jobs", dill.dumps(data))
        return True

    def submitTaskGroup():
        return True

class Worker:
    def __init__(self, id, con):
        self.id = id
        self.redisCon = con
        self.proces = Process(target=self.__work)
    
    def __work(self, queue="jobs"):
        while True:
            print("Locking worker ", self.id)
            packed = self.redisCon.blpop([queue], timeout=0)
            print("Unlocked worker ", self.id)
            t = dill.loads(packed[1])
            func = dill.loads(t['task'])
            contents = urllib.request.urlopen(t['url']).read()
            res = func(contents)
            print(res)
            

    def start(self):
        self.proces.start()

    def stop(self):
        self.proces.terminate()



