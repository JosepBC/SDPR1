#!/usr/bin/env python3

from xmlrpc.server import SimpleXMLRPCServer
import redis

import urllib.request
import random

import dill

from multiprocessing import Process

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

        self.server.register_function(self.addWorker)
        self.server.register_function(self.removeWorker)
        self.server.register_function(self.listWorkers)
        self.server.register_function(self.submitTask)
        self.server.register_function(self.submitTaskGroup)
        self.server.register_function(self.getTaskResult)
    
    def run(self):
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
    def getTaskResult(self, jobID):
        code, res = self.redisCon.blpop(jobID, timeout=0)
        return code.decode("ascii"), dill.loads(res)

    def submitTask(self, jobid, task, url):
        data = {
            'jobid': jobid, 
            'task': task.data,
            'url': url
        }

        task = (mapTask, data)
        self.redisCon.rpush("jobs", dill.dumps(task))
        return True

    def submitTaskGroup(self, jobID, task, urls, reduceFunc):
        for url in urls:
            self.submitTask(jobID, task, url)

        finalQ = str(random.random())

        data = {
            'jobid': jobID,
            'finalQ': finalQ,
            'nElem': len(urls),
            'reduceFunc': reduceFunc.data
        }

        task = (reduceTask, data)
        self.redisCon.rpush("jobs", dill.dumps(task))
        return finalQ


def mapTask(redisCon, data):
    func = dill.loads(data['task'])
    contents = urllib.request.urlopen(data['url']).read().decode("utf-8")
    res = func(contents)
    serializedRes = dill.dumps(res)
    redisCon.rpush(data['jobid'], serializedRes)

def reduceTask(redisCon, data):
    l = list()
    #Wait until all elems have been processed, map applyed to all inputs and store them into a list
    for i in range(data['nElem']):
        q, popped = redisCon.blpop(data['jobid'], timeout=0)
        l.append(dill.loads(popped))

    reduceFoo = dill.loads(data['reduceFunc'])
    reduced = reduceFoo(l)

    serReduced = dill.dumps(reduced)
    redisCon.rpush(data['finalQ'], serReduced)

class Worker:
    def __init__(self, id, con):
        self.id = id
        self.redisCon = con
        self.proces = Process(target=self.__work)
    
    def __work(self):
        while True:
            print("Locking worker ", self.id)
            q, data = self.redisCon.blpop('jobs', timeout=0)
            print("Unlocked worker ", self.id)
            f, args = dill.loads(data)
            f(self.redisCon, args)

    def start(self):
        self.proces.start()

    def stop(self):
        self.proces.terminate()



