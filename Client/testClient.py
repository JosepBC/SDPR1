#!/usr/bin/env python3
from xmlrpc.client import Binary
import xmlrpc.client
import base64
import dill
import functools

def CountingWords(text):
    return len(text.split())

def reduceCounting(listText):
    mapped = map(lambda string: int(string), listText)
    reduced = 0
    for elem in list(mapped):
        reduced += elem
    return reduced

def WordCount(text):
    myMap = {}
    for word in text.split():
        if word in myMap:
            myMap[word] += 1
        else:
            myMap[word] = 1
    return myMap

def reduceWordCount(listText):
    myMap = {}
    for elem in listText:
        for key, value in elem.items():
            if key in myMap:
                myMap[key] += value
            else:
                myMap[key] = value
    return myMap

def main():
    quijote = "http://x.com/"
    proxy = xmlrpc.client.ServerProxy("http://localhost:9000")
    
    proxy.addWorker()
    proxy.addWorker()
    proxy.addWorker("P")

    l = proxy.listWorkers()
    print("Workers: ", l)
    
    serCountingWords = dill.dumps(CountingWords)
    proxy.submitTask("ex", serCountingWords, quijote)
    jobid, res = proxy.getTaskResult("ex")
    print("Task:", jobid, "=", res)
    
    serReduceCounting = dill.dumps(reduceCounting)
    urls = ["http://x.com/", "http://x.com/"]
    taskID = proxy.submitTaskGroup(10, serCountingWords, urls, serReduceCounting)
    jobid, res = proxy.getTaskResult(taskID)
    print("Gruped task:", jobid, "=", res)


    serWordCount = dill.dumps(WordCount)
    serReduceWordCount = dill.dumps(reduceWordCount)
    proxy.submitTask("t", serWordCount, quijote)
    jobid, res = proxy.getTaskResult("t")
    print("Task:", jobid, "=", res)

    taskID = proxy.submitTaskGroup(111, serWordCount, urls, serReduceWordCount)
    jobid, res = proxy.getTaskResult(taskID)
    print("Gruped task:", jobid, "=", res)
    return True

if __name__ == '__main__':
    main()